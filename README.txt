NEWS ONE PRODUCTION v32

IMPORTANT: News One synchronization has been moved from port 8091 to PORT 8093
so it does not conflict with your existing pipeline services.

News One:
  Sync server: 8093
  Tablet: http://192.168.254.149:8093/index.html?v=32
  Control: http://127.0.0.1:8093/control.html

vMix:
  Web/API: 8088

This package does NOT manage or stop:
  8000, 8002, 5173, 8010, 8011, 8012

START:
1. Close the current v31 News One server window with Ctrl+C.
2. Extract v32 into a new folder.
3. Run start_news_one_sync.bat.
4. The black window must say:
   News One Production sync server v32 running on port 8093
5. On the tablet open:
   http://192.168.254.149:8093/index.html?v=32

Do not use the old 8091 URL.
