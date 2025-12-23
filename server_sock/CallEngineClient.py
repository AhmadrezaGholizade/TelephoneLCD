import socket
import threading
import json
import time


class CallEngineClient:
    def __init__(self, socket_path="/run/call_engine.sock", buffer_size=4096):
        self.socket_path = socket_path
        self.buffer_size = buffer_size

        self.sock = None
        self.listener_thread = None
        self.running = False
        self.lock = threading.Lock()

    # ---------- connection ----------
    def connect(self):
        if self.sock:
            return

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)
        self.sock.setblocking(True)

        print("Socket connected")

    # ---------- send ----------
    def send(self, data):
        """
        data: str | dict
        """
        if not self.sock:
            raise RuntimeError("Socket not connected")

        if isinstance(data, dict):
            data = json.dumps(data)

        with self.lock:
            self.sock.sendall(data.encode("utf-8"))

    # ---------- listen ----------
    def _listen_loop(self, on_event):
        buffer = ""

        try:
            while self.running:
                data = self.sock.recv(self.buffer_size)

                if not data:
                    print("Socket closed by server")
                    break

                buffer += data.decode("utf-8")

                # 🔹 newline-delimited protocol
                while "\n" in buffer:
                    raw, buffer = buffer.split("\n", 1)

                    if not raw.strip():
                        continue

                    try:
                        event = json.loads(raw)
                    except json.JSONDecodeError:
                        event = raw

                    on_event(event)

        except Exception as e:
            print("Listener error:", e)

        finally:
            self.running = False
            self.close()

    # ---------- start ----------
    def start(self, on_event):
        """
        on_event: callback(event)
        """
        self.connect()
        self.running = True

        self.listener_thread = threading.Thread(
            target=self._listen_loop,
            args=(on_event,),
            daemon=True
        )
        self.listener_thread.start()

        print("Listener thread started")

    # ---------- stop ----------
    def stop(self):
        self.running = False
        self.close()

    # ---------- cleanup ----------
    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            print("Socket closed")
