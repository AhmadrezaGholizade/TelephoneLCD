import socket
import json
import time
from collections import deque


class EventHandler:

    SOCKET_PATH = "/tmp/phone_monitor.sock"

    

    def __init__(self):
        # queue of (button, timestamp)
        self.last_page_history = None
        self.button_queue = deque(maxlen=2)
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
            client.connect(self.SOCKET_PATH)
            client.sendall(b"GET_STATUS")
            data = client.recv(1024)
            client.close()
            if data:
                return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Could not connect to monitor: {e}")
        return None

    def handle_key(self, STATUS):
        state = self.get_phone_state()
        pressed_button = state["pressed_button"]
        if not pressed_button:
            return None

        now = time.monotonic()
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

        changes = dict()

        if STATUS == 'contacts':
            if pressed_button == 'Down':
                changes['STATUS'] = STATUS
                changes['CONTACT_INDEX'] = +1
                return changes
            if pressed_button == 'Up':
                changes['STATUS'] = STATUS
                changes['CONTACT_INDEX'] = -1
                return changes
            if pressed_button == 'Ok':
                changes['STATUS'] = "contact_info"
                return changes
            if pressed_button == 'Hist':
                changes['STATUS'] = "menu"
                changes['INDEX_RESET'] = True
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
            if pressed_button in set(['Ok', '1', '2', '3', '4', '5', '6']):
                changes['STATUS'] = STATUS
                changes['key'] = pressed_button
                self.last_page_history = 'menu'
                return changes

        if STATUS == 'contact_info':
            if pressed_button == 'Hist':
                changes['STATUS'] = "contacts"
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
            if pressed_button == 'Ok':
                changes['STATUS'] = "history_info"
                return changes
            
        if STATUS == 'history_info':
            if pressed_button == 'Hist':
                changes['STATUS'] = 'history'
                return changes



        
