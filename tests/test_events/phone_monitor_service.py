import struct
import select
import time
import threading
import socket
import json
from collections import deque
import os
import time

EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

event_queue = deque(maxlen=6)

BUTTONS = {
    0: "Mail", 1: "Ok", 2: "Up", 3: "9", 4: "8", 5: "7",
    6: "Mute", 7: "Retry", 8: "Headphone", 9: "L1", 10: "6",
    11: "5", 12: "4", 13: "VolumeDown", 14: "Speaker", 15: "Book",
    16: "3", 17: "2", 18: "1", 19: "Left", 20: "L2",
    21: "Menu", 22: "Redial", 23: "DND", 24: "Hist", 25: "Stop",
    26: "VolumeUp", 27: "Right", 28: "#", 29: "Next", 30: "Down",
    31: "0", 32: "Team", 33: "*"
}

# Shared state (protected by lock for thread safety)
state_lock = threading.Lock()
PRESSED_BUTTON = None
PHONE_STATUS = "DOWN"

SOCKET_PATH = "/run/phone_monitor.sock"  # Path to the socket file

last_event_time = 0
ignore_next = False

def monitor_device():
    global PRESSED_BUTTON, PHONE_STATUS, last_event_time, ignore_next

    print("Monitoring phone events... (Press Ctrl+C to stop)")

    fds = {
        "/dev/input/event1": open("/dev/input/event1", "rb"),
        "/dev/input/event2": open("/dev/input/event2", "rb"),
    }

    try:
        while True:
            readable, _, _ = select.select(fds.values(), [], [], 0.1)
            for fd in readable:
                data = fd.read(EVENT_SIZE)
                if len(data) != EVENT_SIZE:
                    continue

                tv_sec, tv_usec, ev_type, code, value = struct.unpack(EVENT_FORMAT, data)
                if not ev_type and not code and not value:
                    continue

                # Handset lift detection
                if code == 88 and ev_type == 1:  # KEY_HEADSETHOOK
                    new_status = "DOWN" if value else "UP"
                    with state_lock:
                        PHONE_STATUS = new_status
                        # print(f"Phone status changed: {PHONE_STATUS}")
                    continue

                event = {"Type": ev_type, "Code": code, "Value": value}
                # print(f"{time.time()} Event: {event} {(last_event_time - time.time()):.2f}s")

                if event["Type"] == 4 and event["Code"] == 4:
                    event["Button"] = BUTTONS.get(value, f"Unknown({value})")
                    if abs(last_event_time - time.time()) < 0.05:
                        ignore_next = True
                        # print("Ignoring next event due to rapid succession.")
                    elif (PRESSED_BUTTON is None) and (not ignore_next):
                        # print(f"ignore_next = {ignore_next}")
                        PRESSED_BUTTON = event.get("Button", None)
                        ignore_next = False
                    elif ignore_next:
                        ignore_next = False
                        if event["Button"] == PRESSED_BUTTON:
                            PRESSED_BUTTON = None
                            ignore_next = False
                    else:
                        if event["Button"] == PRESSED_BUTTON:
                            PRESSED_BUTTON = None
                            ignore_next = False 



                    # print("PRESSED_BUTTON:", PRESSED_BUTTON)

                    last_event_time = time.time()

                    
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
    except Exception as e:
        print(f"Error in monitor: {e}")
    finally:
        for f in fds.values():
            f.close()

def handle_client(conn):
    """Handle incoming client connections."""
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        if data == "GET_STATUS":
            with state_lock:
                status = {
                    "pressed_button": PRESSED_BUTTON,
                    "phone_status": PHONE_STATUS,
                    "timestamp": time.time()
                }
            conn.sendall(json.dumps(status).encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def run_socket_server():
    """Run the Unix socket server."""
    # Remove old socket if it exists
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)  # Allow up to 5 queued connections
    print(f"Unix socket server listening at {SOCKET_PATH}")

    try:
        while True:
            conn, _ = server.accept()
            # Handle each client in a new thread
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Socket server stopped.")
    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.unlink(SOCKET_PATH)

if __name__ == "__main__":
    # Start the socket server in a background thread
    server_thread = threading.Thread(target=run_socket_server, daemon=True)
    server_thread.start()

    # Run the device monitor in the main thread
    monitor_device()


