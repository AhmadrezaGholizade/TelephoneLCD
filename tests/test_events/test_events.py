import struct
import select
from collections import deque
import time

EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

# keep last 2 events
event_queue = deque(maxlen=2)

last_print_time = 0

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

PRESSED_BUTTUN = None
PHONE_STATUS = "DOWN"


def monitor_device():
    global PRESSED_BUTTUN, PHONE_STATUS, last_print_time

    print("Press Ctrl+C to stop\n")

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

                if ev_type == 1 and code == 88:
                    PHONE_STATUS = "DOWN" if value else "UP"
                    continue

                if ev_type == 4 and code == 4:
                    value = BUTTONS.get(value, value)

                event = {
                    "Type": ev_type,
                    "Code": code,
                    "Value": value
                }

                event_queue.append(event)

                events = list(event_queue)
                if len(events) >= 1 and events[-1]["Type"] == 4:
                    if len(events) == 1 or events[-2]["Value"] == 0:
                        PRESSED_BUTTUN = events[-1]["Value"]
                    elif events[-2]["Value"] == 1:
                        PRESSED_BUTTUN = None

            # ⏱ print every 1 second (outside event logic)
            now = time.time()
            if now - last_print_time >= 1:
                last_print_time = now
                print("===================")
                print("Pressed Button:", PRESSED_BUTTUN)
                print("Phone:", PHONE_STATUS)

    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        for f in fds.values():
            f.close()


if __name__ == "__main__":
    monitor_device()
