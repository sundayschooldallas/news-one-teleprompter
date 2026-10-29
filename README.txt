NEWS ONE PRODUCTION v33

FIXED:
The v32 index.html had an extra closing brace after poll(), which caused the
browser JavaScript to fail parsing. The tablet therefore remained on CONNECTING
and START/countdown did not run.

PORT:
News One sync server = 8093
vMix = 8088

Tablet:
http://192.168.254.149:8093/index.html?v=33

Control:
http://127.0.0.1:8093/control.html

Do not use 8091.
Do not touch the existing pipeline ports.
