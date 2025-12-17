import struct
import select
import time
import threading
import socket
import json
from collections import deque
import os

EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

event_queue = deque(maxlen=2)

BUTTONS = {
    24: "Hist", 22: "Redial", 23: "DND", 21: "Menu",
    18: "1", 17: "2", 16: "3",
    12: "4", 11: "5", 10: "6",
    5: "7", 4: "8", 3: "9",
    33: "*", 31: "0", 28: "#",
    14: "Speaker", 6: "Mute",
    13: "VolumeDown", 26: "VolumeUp",
    7: "Retry", 8: "Headphone",
    20: "L2", 9: "L1",
    0: "Mail", 15: "Book",
    25: "Stop", 29: "Next",
    32: "Team", 1: "Ok",
    2: "Up", 27: "Right",
    19: "Left", 30: "Down",
}

# Shared state (protected by lock for thread safety)
state_lock = threading.Lock()
PRESSED_BUTTON = None
PHONE_STATUS = "DOWN"

SOCKET_PATH = "/tmp/phone_monitor.sock"  # Path to the socket file

def monitor_device():
    global PRESSED_BUTTON, PHONE_STATUS

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
                if ev_type == 1 and code == 88:
                    new_status = "DOWN" if value else "UP"
                    with state_lock:
                        PHONE_STATUS = new_status
                    continue

                # Button label mapping
                if ev_type == 4 and code == 4:
                    value = BUTTONS.get(value, str(value))

                event = {"Type": ev_type, "Code": code, "Value": value}
                event_queue.append(event)

                events = list(event_queue)
                with state_lock:
                    if len(events) >= 1 and events[-1]["Type"] == 4:
                        if len(events) == 1 or events[-2]["Value"] == 0:
                            PRESSED_BUTTON = events[-1]["Value"]
                        elif events[-2]["Value"] == 1:
                            PRESSED_BUTTON = None

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