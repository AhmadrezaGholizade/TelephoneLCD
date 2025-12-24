import socket
import threading
import json
import time

class CallEngineClient:
    def __init__(self, fb, tools, socket_path="/run/call_engine.sock", buffer_size=4096):
        self.socket_path = socket_path
        self.buffer_size = buffer_size
        self.sock = None
        self.listener_thread = None
        self.running = False
        self.lock = threading.Lock()
        self.fb = fb
        self.tools = tools
        self.reconnect_delay = 1  # Start with 1 second
        self.max_reconnect_delay = 30  # Max 30 seconds between attempts
        self.on_event_callback = None
        self.connected = False

    # ---------- connection with retry ----------
    def connect(self):
        """Connect with exponential backoff retry"""
        # Only draw initialization on first connection attempt
        if not self.connected:
            self.tools.draw_initialization(self.fb)
        
        # If already connected, verify the connection is still alive
        if self.connected and self.sock:
            try:
                # Try to check socket status (non-blocking peek)
                self.sock.setblocking(False)
                try:
                    data = self.sock.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
                    if not data:
                        # Socket closed by peer
                        raise socket.error("Socket closed")
                except (socket.error, BlockingIOError):
                    # No data available, but socket is alive
                    pass
                finally:
                    self.sock.setblocking(True)
                
                print("Socket already connected and alive")
                return True
            except (socket.error, OSError):
                print("Existing socket is dead, reconnecting...")
                self.connected = False
        
        retry_delay = self.reconnect_delay
        while True:
            try:
                # Clean up old socket
                if self.sock:
                    try:
                        self.sock.close()
                    except:
                        pass
                    self.sock = None
                
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.connect(self.socket_path)
                self.sock.setblocking(True)
                self.connected = True
                print("Socket connected successfully")
                
                # Reset retry delay on successful connection
                return True
                
            except (socket.error, OSError) as e:
                print(f"Connection failed: {e}. Retrying in {retry_delay}s...")
                self.connected = False
                time.sleep(retry_delay)
                
                # Exponential backoff
                retry_delay = min(retry_delay * 2, self.max_reconnect_delay)

    # ---------- send with retry ----------
    def send(self, data):
        """
        Send data with automatic reconnection on failure
        data: str | dict
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        
        while True:
            try:
                if not self.sock or not self.connected:
                    print("Socket not connected, attempting to connect...")
                    self.connect()
                
                with self.lock:
                    self.sock.sendall(data.encode("utf-8"))
                return True  # Successfully sent
                
            except (socket.error, OSError, RuntimeError) as e:
                print(f"Send failed: {e}. Reconnecting...")
                self.connected = False
                self.connect()
                # Loop will retry sending after reconnection

    # ---------- listen with auto-reconnect ----------
    def _listen_loop(self, on_event):
        """Listen loop with automatic reconnection"""
        buffer = ""
        
        while self.running:
            try:
                # Ensure we're connected
                if not self.sock or not self.connected:
                    print("Listener: Not connected, attempting to connect...")
                    self.connect()
                    buffer = ""  # Clear buffer on reconnect
                
                data = self.sock.recv(self.buffer_size)
                
                if not data:
                    print("Socket closed by server, reconnecting...")
                    self.connected = False
                    self.connect()
                    continue
                
                buffer += data.decode("utf-8")
                
                # Process newline-delimited messages
                while "\n" in buffer:
                    raw, buffer = buffer.split("\n", 1)
                    if not raw.strip():
                        continue
                    
                    try:
                        event = json.loads(raw)
                    except json.JSONDecodeError:
                        event = raw
                    
                    on_event(event)
                    
            except (socket.error, OSError) as e:
                print(f"Listener error: {e}. Reconnecting...")
                self.connected = False
                time.sleep(1)  # Brief pause before reconnecting
                self.connect()
                buffer = ""  # Clear buffer on error
                
            except Exception as e:
                print(f"Unexpected listener error: {e}")
                time.sleep(1)

    # ---------- start ----------
    def start(self, on_event):
        """
        Start the client with event callback
        on_event: callback(event)
        """
        self.on_event_callback = on_event
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
        """Stop the client gracefully"""
        self.running = False
        self.connected = False
        self.close()
        
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=2)

    # ---------- cleanup ----------
    def close(self):
        """Close socket connection"""
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            self.connected = False
            print("Socket closed")
    
    # ---------- health check ----------
    def is_connected(self):
        """Check if socket is connected"""
        return self.connected and self.sock is not None