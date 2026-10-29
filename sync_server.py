import json, os, time, threading, urllib.parse, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 8093
BASE = os.path.dirname(os.path.abspath(__file__))
STORIES_FILE = os.path.join(BASE, "stories.json")

state_lock = threading.Lock()
state = {
    "id": 0,
    "command": "idle",
    "targetAt": 0,
    "seconds": 0,
    "serverNow": int(time.time()*1000),
    "recording": False
}

def load_stories():
    try:
        with open(STORIES_FILE, "r", encoding="utf-8") as f:
            x = json.load(f)
        return x if isinstance(x, list) else []
    except Exception:
        return []

def save_stories(stories):
    tmp = STORIES_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STORIES_FILE)

def vmix(command):
    # vMix Web Controller API endpoint. This is intentionally server-side
    # so the tablet does not need to make cross-origin calls to vMix.
    url = "http://127.0.0.1:8088/api/?Function=" + urllib.parse.quote(command, safe="")
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return r.status == 200
    except Exception as e:
        print("vMix command failed:", command, e)
        return False

def set_state(command, seconds=0, target=0, recording=False):
    with state_lock:
        state["id"] += 1
        state["command"] = command
        state["seconds"] = seconds
        state["targetAt"] = target
        state["serverNow"] = int(time.time()*1000)
        state["recording"] = recording

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def end_json(self, obj, code=200):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/api/state":
            with state_lock:
                out = dict(state)
                out["serverNow"] = int(time.time()*1000)
            return self.end_json(out)

        if path == "/api/stories":
            return self.end_json({"ok": True, "stories": load_stories()})

        if path == "/api/health":
            return self.end_json({"ok": True, "serverNow": int(time.time()*1000)})

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        try:
            body = self.rfile.read(length) if length else b"{}"
            data = json.loads(body.decode("utf-8"))
        except Exception:
            return self.end_json({"ok": False, "error": "Invalid JSON"}, 400)

        if parsed.path == "/api/stories":
            stories = data.get("stories")
            if not isinstance(stories, list):
                return self.end_json({"ok": False, "error": "stories must be an array"}, 400)
            save_stories(stories)
            return self.end_json({"ok": True, "stories": stories})

        if parsed.path == "/api/story/save":
            story = data.get("story")
            if not isinstance(story, dict) or not story.get("id") or not story.get("title"):
                return self.end_json({"ok": False, "error": "Invalid story"}, 400)
            stories = load_stories()
            stories = [s for s in stories if s.get("id") != story["id"]]
            stories.append(story)
            stories.sort(key=lambda x: x.get("updatedAt",""), reverse=True)
            save_stories(stories)
            return self.end_json({"ok": True, "story": story, "stories": stories})

        if parsed.path == "/api/story/delete":
            sid = str(data.get("id",""))
            stories = [s for s in load_stories() if str(s.get("id")) != sid]
            save_stories(stories)
            return self.end_json({"ok": True, "stories": stories})

        if parsed.path == "/api/countdown":
            seconds = max(0, min(60, int(data.get("seconds", 10))))
            now = int(time.time()*1000)
            target = now + seconds*1000
            set_state("countdown", seconds, target, False)
            with state_lock:
                expected_id = state["id"]

            def worker(expected_id, target):
                while True:
                    with state_lock:
                        if state["id"] != expected_id or state["command"] != "countdown":
                            print("COUNTDOWN CANCELLED -> StartRecording was NOT sent")
                            return
                    remaining_ms = target - int(time.time()*1000)
                    if remaining_ms <= 0:
                        break
                    time.sleep(min(0.05, remaining_ms/1000))

                # At zero, call vMix while the state is still "countdown".
                # This avoids the race in v28/v27 where the worker changed
                # the state first and then failed its own state check.
                ok = vmix("StartRecording")

                with state_lock:
                    if state["id"] != expected_id or state["command"] != "countdown":
                        # STOP won the race. If vMix nevertheless started,
                        # immediately stop it so an aborted countdown cannot
                        # leave recording running.
                        if ok:
                            vmix("StopRecording")
                        print("COUNTDOWN CANCELLED DURING VMIX CALL")
                        return

                    state["id"] += 1
                    state["command"] = "recording"
                    state["seconds"] = 0
                    state["targetAt"] = target
                    state["serverNow"] = int(time.time()*1000)
                    state["recording"] = bool(ok)

                print("COUNTDOWN ZERO -> StartRecording:", ok)

            threading.Thread(target=worker, args=(expected_id, target), daemon=True).start()
            with state_lock:
                out = dict(state)
            return self.end_json({"ok": True, "state": out})

        if parsed.path == "/api/stop":
            # Increment the state id first. Any countdown worker holding the
            # previous id will see the mismatch and abort before StartRecording.
            with state_lock:
                state["id"] += 1
                state["command"] = "idle"
                state["seconds"] = 0
                state["targetAt"] = 0
                state["serverNow"] = int(time.time()*1000)
                was_recording = bool(state.get("recording"))
                state["recording"] = False
            ok = True
            if was_recording:
                ok = vmix("StopRecording")
            return self.end_json({"ok": True, "vmix": ok, "cancelled": True, "state": state})

        if parsed.path == "/api/cancel-countdown":
            # Cancel only. Do NOT touch vMix recording unless it is already
            # active. This lets the operator safely abort before zero.
            with state_lock:
                state["id"] += 1
                state["command"] = "idle"
                state["seconds"] = 0
                state["targetAt"] = 0
                state["serverNow"] = int(time.time()*1000)
                state["recording"] = False
            return self.end_json({"ok": True, "cancelled": True, "state": state})

        if parsed.path == "/api/ping-vmix":
            # A lightweight API check. Start/stop are not issued here.
            try:
                urllib.request.urlopen("http://127.0.0.1:8088/api/", timeout=2).read(100)
                return self.end_json({"ok": True, "vmix": True})
            except Exception as e:
                return self.end_json({"ok": True, "vmix": False, "error": str(e)})

        return self.end_json({"ok": False, "error": "Not found"}, 404)

if __name__ == "__main__":
    if not os.path.exists(STORIES_FILE):
        save_stories([])
    print("News One Production sync server v37 running on port 8093")
    print("Control Center: http://127.0.0.1:8093/control.html")
    print("Tablet Teleprompter: http://192.168.254.149:8093/index.html")
    print("Keep this window running while recording.")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
