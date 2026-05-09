import struct
import select
import time

EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

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

def decode_event(data):
    tv_sec, tv_usec, ev_type, code, value = struct.unpack(EVENT_FORMAT, data)
    ts = tv_sec + tv_usec / 1_000_000

    # Sync event
    if ev_type == 0 and code == 0 and value == 0:
        return ts, "[SYNC]", None

    # Handset lift
    if ev_type == 1 and code == 88:
        return ts, "HANDSET", "DOWN" if value else "UP"

    # Button scan code
    if ev_type == 4 and code == 4:
        label = BUTTONS.get(value, f"UNKNOWN({value})")
        return ts, "SCAN", label

    # Key press/release (ev_type==1)
    if ev_type == 1:
        action = {1: "PRESS", 0: "RELEASE", 2: "REPEAT"}.get(value, f"VAL={value}")
        return ts, f"KEY code={code}", action

    return ts, f"TYPE={ev_type} CODE={code}", f"VAL={value}"

def main():
    print(f"EVENT_SIZE = {EVENT_SIZE} bytes")
    print("Reading raw events from /dev/input/event1 and event2")
    print("=" * 60)
    print("لطفاً دکمه‌ها رو بزن — همه چیز لاگ میشه. Ctrl+C برای خروج.")
    print("=" * 60)

    fds = {
        "event1": open("/dev/input/event1", "rb"),
        "event2": open("/dev/input/event2", "rb"),
    }
    fd_names = {v: k for k, v in fds.items()}

    start = time.time()

    try:
        while True:
            readable, _, _ = select.select(fds.values(), [], [], 0.5)
            for fd in readable:
                data = fd.read(EVENT_SIZE)
                if len(data) != EVENT_SIZE:
                    print(f"[WARN] کوتاه‌تر از حد انتظار: {len(data)} bytes از {fd_names[fd]}")
                    continue

                ts, label, detail = decode_event(data)
                elapsed = ts - start if start else 0

                if label == "[SYNC]":
                    print(f"  [{fd_names[fd]}] +{elapsed:.4f}s  ─── SYNC ───")
                else:
                    print(f"  [{fd_names[fd]}] +{elapsed:.4f}s  {label:25s}  {detail}")

    except KeyboardInterrupt:
        print("\nتموم شد.")
    finally:
        for f in fds.values():
            f.close()

if __name__ == "__main__":
    main()
