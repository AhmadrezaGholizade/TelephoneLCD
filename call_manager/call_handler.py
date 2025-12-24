import time
import json

class Call_handler:
    def __init__(self, callEngineClient):
        self.callEngineClient = callEngineClient

    def main_handler(self, changes, number):
        if not changes:
            return

        # answer
        if changes.get("ANSWER", False):
            self._answer()

        # hangUp
        if changes.get("HANGUP", False):
            self._hangUp()

        # call
        if number and changes.get("CALL", False):
            self._call(number)

        # reject
        if changes.get("REJECT", False):
            self._reject()
        
    def _reject(self):
        msg = {
            "action": "reject"
        }
        self.callEngineClient.send(json.dumps(msg))

    def _answer(self):
        msg = {
            "action": "answer"
        }
        self.callEngineClient.send(json.dumps(msg))

    def _hangUp(self):
        msg = {
            "action": "hangup"
        }
        self.callEngineClient.send(json.dumps(msg))
                
    def _call(self, number):
        msg = {
            "action": "call",
            "number": number
        }
        self.callEngineClient.send(json.dumps(msg))

    def send_ping(self):
        ts = int(time.time() * 1000)
        msg = {
            "action": "ping",
            "ts": ts
        }
        self.callEngineClient.send(json.dumps(msg))
