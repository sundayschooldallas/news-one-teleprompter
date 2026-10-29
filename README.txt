NEWS ONE PRODUCTION v37

STABLE VMIX PREVIEW:
v36 used the vMix LiveLAN webpage in an iframe. That webpage can flicker or
freeze when embedded.

v37 uses the documented vMix LiveLAN HLS stream directly:
http://<vMix-IP>:8088/livelan/stream.m3u8

The tablet uses an HTML5 video element with hls.js, rather than embedding the
whole vMix LiveLAN webpage. This removes the browser controls/page rendering
from the preview and prevents iframe reload/flicker.

SEQUENCE:
- START: countdown begins; vMix HLS preview is shown.
- Countdown remains visible.
- At 5 seconds: preview is hidden and teleprompter is shown paused.
- Countdown continues 5,4,3,2,1,0.
- At zero: vMix recording starts.
- Scrolling begins only after the server confirms recording=true.
- STOP cancels countdown/stops recording and releases the HLS player.
- Flip Vertical flips the video only.
- Speed/font buttons and mouse wheel remain.
- Stories remain centralized on port 8093.

PORTS:
News One sync: 8093
vMix: 8088
Pipeline ports untouched.

Tablet:
http://192.168.254.149:8093/index.html?v=37

Control:
http://127.0.0.1:8093/control.html

NOTE:
vMix LiveLAN is HLS and has typical browser latency. vMix documents the HLS
endpoint and notes that LiveLAN is intended for local-network viewing.
