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
STORIES_FILE = os.path.join(ROOT, "stories.json")

state_lock = threading.Lock()
stories_lock = threading.Lock()
state = {
    "id": 0,
    "command": "idle",
    "targetAt": 0,
    "seconds": 0,
    "serverNow": int(time.time() * 1000),
}

def load_stories():
    try:
        with open(STORIES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

def save_stories(stories):
    tmp = STORIES_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STORIES_FILE)

def clean_story(s):
    if not isinstance(s, dict):
        return None
    sid = str(s.get("id", "")).strip()
    title = str(s.get("title", "")).strip()
    content = str(s.get("content", ""))
    if not sid or not title:
        return None
    return {
        "id": sid,
        "title": title,
        "content": content,
        "updatedAt": str(s.get("updatedAt") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
    }

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def _send_json(self, code, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
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
        if path == "/api/stories":
            with stories_lock:
                stories = load_stories()
            self._send_json(200, {"ok": True, "stories": stories})
            return
        super().do_GET()

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = self._read_json()
        except Exception as exc:
            self._send_json(400, {"ok": False, "error": str(exc)})
            return

        if path == "/api/stories":
            story = clean_story(data.get("story") if isinstance(data, dict) else data)
            if not story:
                self._send_json(400, {"ok": False, "error": "Invalid story"})
                return
            with stories_lock:
                stories = load_stories()
                replaced = False
                for i, old in enumerate(stories):
                    if old.get("id") == story["id"]:
                        stories[i] = story
                        replaced = True
                        break
                if not replaced:
                    stories.append(story)
                save_stories(stories)
            self._send_json(200, {"ok": True, "story": story, "stories": stories})
            return

        if path == "/api/stories/bulk":
            incoming = data.get("stories", []) if isinstance(data, dict) else []
            if not isinstance(incoming, list):
                self._send_json(400, {"ok": False, "error": "stories must be an array"})
                return
            with stories_lock:
                stories = load_stories()
                by_id = {s.get("id"): s for s in stories if s.get("id")}
                for raw in incoming:
                    story = clean_story(raw)
                    if story:
                        old = by_id.get(story["id"])
                        if not old or str(story.get("updatedAt", "")) >= str(old.get("updatedAt", "")):
                            by_id[story["id"]] = story
                stories = list(by_id.values())
                save_stories(stories)
            self._send_json(200, {"ok": True, "stories": stories})
            return

        if path == "/api/command":
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
            return

        self.send_error(404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/stories":
            self.send_error(404)
            return
        try:
            data = self._read_json()
        except Exception:
            data = {}
        sid = str(data.get("id", "")).strip()
        if not sid:
            self._send_json(400, {"ok": False, "error": "Missing story id"})
            return
        with stories_lock:
            stories = [s for s in load_stories() if s.get("id") != sid]
            save_stories(stories)
        self._send_json(200, {"ok": True, "stories": stories})

if __name__ == "__main__":
    if not os.path.exists(STORIES_FILE):
        save_stories([])
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"News One Production sync server running on port {PORT}")
    print(f"Control Center: http://127.0.0.1:{PORT}/control.html")
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = "<THIS-PC-IP>"
    print(f"Tablet Teleprompter: http://{host_ip}:{PORT}/index.html")
    print("Central story library: http://<THIS-PC-IP>:%d/api/stories" % PORT)
    print("Keep this window running while recording.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
