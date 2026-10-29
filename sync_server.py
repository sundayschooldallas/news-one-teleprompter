#!/usr/bin/env python3
import json
import os
import threading
import time
import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8091

state_lock = threading.Lock()
state = {
    "id": 0,
    "command": "idle",
    "targetAt": 0,
    "seconds": 0,
    "serverNow": int(time.time() * 1000),
}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def _send_json(self, code, payload):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/state":
            with state_lock:
                payload = dict(state)
                payload["serverNow"] = int(time.time() * 1000)
            self._send_json(200, payload)
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/command":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception as exc:
            self._send_json(400, {"ok": False, "error": str(exc)})
            return

        command = str(data.get("command", "")).strip()
        if command not in {"countdown", "cancel", "stop"}:
            self._send_json(400, {"ok": False, "error": "Unknown command"})
            return

        with state_lock:
            state["id"] += 1
            state["command"] = command
            state["targetAt"] = int(data.get("targetAt") or 0)
            state["seconds"] = int(data.get("seconds") or 0)
            state["serverNow"] = int(time.time() * 1000)
            payload = dict(state)

        self._send_json(200, {"ok": True, **payload})

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"News One Production sync server running on port {PORT}")
    print(f"Control Center: http://127.0.0.1:{PORT}/control.html")
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = "<THIS-PC-IP>"
    print(f"Tablet Teleprompter: http://{host_ip}:{PORT}/index.html")
    print("Keep this window running while recording.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
