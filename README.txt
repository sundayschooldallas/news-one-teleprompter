NEWS ONE PRODUCTION v29

This version fixes the vMix recording race and simplifies the tablet preview.

START SEQUENCE:
- Press START on tablet or Control Center.
- The server sets the countdown target immediately.
- While remaining time is > 5 seconds, tablet shows the vMix LiveLAN preview.
- At 5 seconds, tablet switches to the teleprompter and remains PAUSED.
- At 0, the server calls vMix StartRecording.
- Only after vMix responds does the tablet enter RECORDING and begin scrolling.

STOP:
- STOP increments the server state id immediately.
- The countdown worker sees the mismatch and aborts.
- If a simultaneous vMix StartRecording call already returned success, the server immediately sends StopRecording.
- STOP also clears the tablet countdown/preview.

PREVIEW:
- Uses the vMix LiveLAN browser page at http://PC-IP:8088/livelan.
- No external HLS library or CDN is required.

FILES:
- sync_server.py
- index.html
- control.html
- start_news_one_sync.bat
- stories.json

Tablet:
http://192.168.254.149:8091/index.html?v=29

Control Center:
http://127.0.0.1:8091/control.html
