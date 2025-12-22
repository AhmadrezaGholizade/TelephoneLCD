import socket
import json
import time

SOCKET_PATH = "/run/phone_monitor.sock"

def get_phone_state():
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.sendall(b"GET_STATUS")
        data = client.recv(1024)
        client.close()
        if data:
            return json.loads(data.decode('utf-8'))
    except Exception as e:
        print(f"Could not connect to monitor: {e}")
    return None

# Example usage: Poll every second
if __name__ == "__main__":
    while True:
        state = get_phone_state()
        if state:
            print(f"Button: {state['pressed_button']} | Phone: {state['phone_status']} | Timestamp: {state['timestamp']}")
        else:
            print("Service unavailable")
        time.sleep(1)