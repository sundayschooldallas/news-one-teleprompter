NEWS ONE PRODUCTION v36

VISUAL FIX:
The countdown overlay previously used a 70% black background over the entire
vMix preview. That made the camera image look much darker.

v36 removes that black overlay. The countdown number remains large and readable
using a shadow, while the camera preview stays at its normal brightness.

All v35 sequence fixes are retained:
- vMix preview does not flicker.
- Countdown continues to zero.
- Preview is handed back at 5 seconds.
- Recording starts at zero.
- Scrolling starts only after recording is confirmed.
- News One sync uses port 8093.
- Other pipeline ports are not managed.

Tablet:
http://192.168.254.149:8093/index.html?v=36

Control:
http://127.0.0.1:8093/control.html
