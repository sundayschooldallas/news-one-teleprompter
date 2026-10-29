NEWS ONE PRODUCTION v35

FIXES FROM v34:
1. vMix preview no longer flickers/reloads every 250ms. The iframe is loaded
   once per run instead of changing its URL on every state poll.
2. Countdown now continues visibly all the way to 0. At 5 seconds the vMix
   preview is removed and the teleprompter is shown, but the countdown keeps
   running: 5, 4, 3, 2, 1, 0.
3. At zero, the server increments the state ID when it changes to RECORDING.
   This lets the tablet detect the transition and actually start scrolling.
4. Scrolling starts only when the server reports recording=true.
5. STOP resets the preview for the next run.

PORTS:
News One sync: 8093
vMix: 8088
No pipeline ports are managed.

Tablet:
http://192.168.254.149:8093/index.html?v=35

Control:
http://127.0.0.1:8093/control.html
