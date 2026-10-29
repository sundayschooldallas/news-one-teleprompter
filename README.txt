NEWS ONE PRODUCTION v34

CRITICAL FIX:
v33 referenced a non-existent monitorLoading element when the countdown tried
to show the vMix preview. That JavaScript error stopped the polling loop,
which made the tablet show SYNC SERVER OFFLINE and made the countdown appear
only briefly. v34 removes that bad reference.

v34:
- Port 8093 only for News One sync.
- Countdown remains visible.
- vMix LAN preview appears during countdown above the teleprompter.
- At 5 seconds, the preview is handed off to the teleprompter paused.
- At 0, server calls vMix StartRecording.
- Scrolling starts only after the server confirms vMix recording.
- STOP cancels countdown and stops recording if active.
- Does not manage pipeline ports.

Tablet:
http://192.168.254.149:8093/index.html?v=34

Control:
http://127.0.0.1:8093/control.html
