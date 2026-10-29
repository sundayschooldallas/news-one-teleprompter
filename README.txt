NEWS ONE PRODUCTION v24

FIXES:
- STOP now cancels an active countdown before zero and prevents StartRecording.
- STOP removes the countdown number immediately.
- Countdown number never remains over the teleprompter.
- At exactly 5 seconds remaining, the vMix preview cleanly hands off to the teleprompter.
- vMix LiveLAN preview uses the documented HLS stream URL as the primary method, with the LiveLAN web page as fallback.
- Separate vMix preview vertical flip retained.
- Teleprompter vertical flip keeps the text moving in the correct visible direction.
- Recording is still triggered server-side at countdown zero.
- Central story library retained.

START:
1. Stop old server with Ctrl+C.
2. Run start_news_one_sync.bat from this folder.
3. Windows control: http://127.0.0.1:8091/control.html
4. Tablet: http://YOUR-PC-IP:8091/index.html

For vMix:
- LiveLAN must be enabled/running in vMix.
- vMix Web Controller must be on port 8088.
