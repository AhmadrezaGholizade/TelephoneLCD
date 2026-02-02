from flask import Flask, request, jsonify
import subprocess
import threading
import os

app = Flask(__name__)

# Path configuration
WAV_DIRS = {
    "call": "./wavs/call",
    "ringtone": "./wavs/ringtone"
}

# Global process to track current playback
current_process = None
should_stop = False
lock = threading.Lock()

def play_loop(file_path):
    global current_process, should_stop
    while True:
        with lock:
            # If we should stop, exit loop
            if should_stop:
                current_process = None
                break
        
        # Play outside the lock
        process = subprocess.Popen(["aplay", file_path])
        
        with lock:
            current_process = process
        
        process.wait()

@app.route("/play/<category>/<filename>", methods=["GET"])
def play(category, filename):
    global current_process, should_stop
    
    # Validate category
    if category not in WAV_DIRS:
        return jsonify({"error": "Invalid category"}), 400
    
    file_path = os.path.join(WAV_DIRS[category], filename)
    
    if not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404
    
    with lock:
        should_stop = True
        # Immediately kill current playback
        if current_process is not None:
            try:
                current_process.terminate()
                current_process.kill()  # Force kill immediately
            except:
                pass
        # Kill all aplay processes to be sure
        subprocess.run(["pkill", "-9", "-f", "aplay"])
    
    # Small delay to let old thread stop
    threading.Event().wait(0.1)
    
    with lock:
        should_stop = False
        current_process = None
    
    # Start new playback in a separate thread
    thread = threading.Thread(target=play_loop, args=(file_path,), daemon=True)
    thread.start()
    
    return jsonify({"status": f"Started playing {filename} in loop"})

@app.route("/stop", methods=["GET"])
def stop():
    global current_process, should_stop
    
    with lock:
        should_stop = True
        if current_process is not None:
            try:
                current_process.terminate()
            except:
                pass
            current_process = None
            # Kill all aplay instances as backup
            subprocess.run(["pkill", "-f", "aplay"])
            return jsonify({"status": "Stopped playback"})
    
    return jsonify({"status": "Nothing is playing"})

@app.route("/setVolume/<int:level>", methods=["GET"])
def set_volume(level):
    # Validate volume level (0-100)
    if level < 0 or level > 100:
        return jsonify({"error": "Volume must be between 0 and 100"}), 400
    
    # Set the volume
    subprocess.run(["amixer", "set", "'Speaker Analog'", f"{level}%"])
    
    return jsonify({"status": f"Volume set to {level}%"})

if __name__ == "__main__":
    # Run on all interfaces, port 5000
    app.run(host="0.0.0.0", port=5000)