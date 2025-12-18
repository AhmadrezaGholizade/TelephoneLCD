import socket
import json
import time

class EventHandler:

    SOCKET_PATH = "/tmp/phone_monitor.sock"

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
        if pressed_button:
            # print(pressed_button)
            pass
        else:
            return None
        
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
            if pressed_button == 'Hist':
                changes['STATUS'] = "main_page"
                return changes
            if pressed_button == 'Ok':
                changes['STATUS'] = STATUS
                changes['OK'] = True
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


        
