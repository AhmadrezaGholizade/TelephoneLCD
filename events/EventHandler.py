import socket
import json
import time
from collections import deque


class EventHandler:
    KEY_SOCKET_PATH = "/run/phone_monitor.sock"

    def __init__(self):
        # queue of (button, timestamp)
        self.last_page_history = None
        self.button_queue = deque(maxlen=2)
        self.last_action_time = time.monotonic()
        self.screen_light_status = True
        self.last_phone_status = None
        self.phone_status_changed = False

    def _push(self, button, timestamp):
        self.button_queue.append((button, timestamp))

    def _all_same(self, button):
        if len(list(self.button_queue))<2:
            return False
        b1, b2 = list(self.button_queue)
        if b1[0]==b2[0] and b1[0] == button:
            return True
        else: 
            return False

    def get_phone_state(self):
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(self.KEY_SOCKET_PATH)
            client.sendall(b"GET_STATUS")
            data = client.recv(1024)
            client.close()
            if data:
                return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Could not connect to monitor: {e}")
        return None

    def check_light_timeout(self, fb, timeout = 10000):
        if (time.monotonic() - self.last_action_time) > timeout:
            self.screen_light_status = False
            fb.screen_off()
        else: 
            self.screen_light_status = True
            fb.screen_on()    

    def _call(self):
        return {
            'CALL': True
        }
    def _answer(self):
        return {
            'ANSWER': True
        }
    def _hangUp(self):
        return {
            'HANGUP': True
        }
    def _reject(self):
        return {
            'REJECT': True
        }

    def handle_key(self, STATUS):
        state = self.get_phone_state()
        
        # Check for picking UP or DOWN the phone
        if state["phone_status"] != self.last_phone_status:
            self.phone_status_changed = True
        else:
            self.phone_status_changed = False
        self.last_phone_status = state["phone_status"]
        
        # Get phone and button value
        pressed_button = state["pressed_button"]
        phone_status = state["phone_status"]

        # NOW
        now = time.monotonic()

        # If nothing's changed return None
        if not pressed_button and not self.phone_status_changed:
            return None
        else:
            # Update last action tine
            self.last_action_time = now

        # the Fist pressing button on light off state of screen does nithing
        if not self.screen_light_status and not self.phone_status_changed:
            return None
            

        changes = dict()

        if STATUS == 'login':
            if pressed_button == 'Hist':
                changes['STATUS'] = "menu"
                return changes
            if pressed_button == 'Redial':
                changes['STATUS'] = 'main_page'
                changes['LOGIN'] = True
                return changes
            else:
                changes['STATUS'] = STATUS
                changes['pressed_button'] = pressed_button
                return changes  

        # Handle repitition of keys
        if len(self.button_queue) != 0:
            last_button, last_time = self.button_queue[-1]
            if now - last_time > 1:
                self.button_queue = deque(maxlen=2)
            else:
                if pressed_button == last_button:
                    if not self._all_same(pressed_button):
                        if now - last_time <= 0.6:
                            return None
        self._push(pressed_button, now)

        # Phone state changes
        if STATUS == 'type_number':
            if self.phone_status_changed and phone_status == "UP":
                return self._call()

        if STATUS == 'ringing':
            if self.phone_status_changed and phone_status == "UP":
                return self._answer()

        if STATUS == 'incall':
            if self.phone_status_changed and phone_status == "DOWN":
                return self._hangUp()

        if STATUS == 'calling':
            if self.phone_status_changed and phone_status == "DOWN":
                return self._hangUp()
        

        if self.phone_status_changed and phone_status == "UP":
            changes['STATUS'] = "type_number"
            if STATUS != 'type_number':
                changes['FIRST_CHAR'] = ""
            return changes
        if self.phone_status_changed and phone_status == "DOWN":
            changes['STATUS'] = "main_page"
            return changes

        # Key Events
        if STATUS == 'contacts':
            if pressed_button == 'Down':
                changes['STATUS'] = STATUS
                changes['CONTACT_INDEX'] = +1
                return changes
            if pressed_button == 'Up':
                changes['STATUS'] = STATUS
                changes['CONTACT_INDEX'] = -1
                return changes
            if pressed_button in set(['Ok', 'Redial']):
                changes['STATUS'] = "contact_info"
                return changes
            if pressed_button == 'Hist':
                changes['STATUS'] = "menu"
                changes['INDEX_RESET'] = True
                return changes
            if pressed_button == 'DND':
                changes['STATUS'] = "type_number"
                changes['CALL_ITEM'] = True
                return changes

        if STATUS == 'menu':
            if pressed_button == 'Down':
                changes['STATUS'] = STATUS
                changes['MENU_ITEM_INDEX'] = +1
                return changes
            if pressed_button == 'Up':
                changes['STATUS'] = STATUS
                changes['MENU_ITEM_INDEX'] = -1
                return changes
            if pressed_button == 'Left':
                changes['STATUS'] = STATUS
                changes['MENU_ITEM_INDEX'] = -3
                return changes
            if pressed_button == 'Right':
                changes['STATUS'] = STATUS
                changes['MENU_ITEM_INDEX'] = +3
                return changes
            if pressed_button == 'Hist':
                changes['STATUS'] = "main_page"
                return changes
            # if pressed_button in set(['Ok', '1', '2', '3', '4', '5', '6']):
            if pressed_button in set(['Ok', '1', '2', '6']): # TEMP
                changes['STATUS'] = STATUS
                changes['key'] = pressed_button
                self.last_page_history = 'menu'
                return changes

        if STATUS == 'contact_info':
            if pressed_button == 'Hist':
                changes['STATUS'] = "contacts"
                return changes
            if pressed_button == 'Redial':
                changes['STATUS'] = "type_number"
                changes['CALL_ITEM'] = True
                return changes
        
        if STATUS == 'main_page':
            if pressed_button == 'Menu':
                changes['STATUS'] = "menu"
                changes['INDEX_RESET'] = True
                return changes
            if pressed_button == 'Hist':
                changes['STATUS'] = "history"
                self.last_page_history = 'main_page'
                changes['INDEX_RESET'] = True
                return changes
            if pressed_button in set(['1', '2', '3', '4', '5', '6', '7', '8', '9','*', '0', '#']):
                changes['STATUS'] = "type_number"
                changes['FIRST_CHAR'] = pressed_button
                return changes


        if STATUS == 'history':
            if pressed_button == 'Hist':
                changes['STATUS'] = self.last_page_history
                changes['INDEX_SET'] = 1
                return changes
            if pressed_button == 'Down':
                changes['STATUS'] = STATUS
                changes['HISTORY_INDEX'] = +1
                return changes
            if pressed_button == 'Up':
                changes['STATUS'] = STATUS
                changes['HISTORY_INDEX'] = -1
                return changes
            if pressed_button in set(['Ok', 'Redial']):
                changes['STATUS'] = "history_info"
                return changes
            
        if STATUS == 'history_info':
            if pressed_button == 'Hist':
                changes['STATUS'] = 'history'
                return changes
            if pressed_button == 'Redial':
                changes['STATUS'] = "type_number"
                changes['CALL_HISTORY_ITEM'] = True
                return changes

        if STATUS == 'type_number':
            if pressed_button == 'Hist':
                changes['STATUS'] = 'main_page'
                return changes
            if pressed_button == 'Redial':
                return self._call()
            if pressed_button == 'DND':
                changes['STATUS'] = STATUS
                changes['ERASE'] = True
                return changes
            if pressed_button in set(['1', '2', '3', '4', '5', '6', '7', '8', '9','*', '0', '#']):
                changes['STATUS'] = "type_number"
                changes['ADD_CHAR'] = pressed_button
                return changes

        if STATUS == 'ringing':
            if pressed_button == 'Hist':
                return self._answer()
            if pressed_button == 'Redial':
                return self._reject()
            
        if STATUS in ['calling', 'incall']:
            if pressed_button == 'Hist':
                return self._hangUp()
            
        
        if STATUS == 'logout':
            if pressed_button == 'Hist': 
                changes['STATUS'] = "menu"
                return changes
            if pressed_button == 'Redial':
                changes['STATUS'] = "main_page"
                changes['LOGOUT'] = True
                return changes



        

            






        
