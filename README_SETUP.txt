NEWS ONE PRODUCTION v22 — CENTRAL STORIES + VMIX MONITOR + SYNCED RECORDING

WHAT CHANGED
- Stories are now stored centrally on the Windows News One sync server.
- The Windows computer and Android tablet use the same story library.
- Saving on one device makes the story available on the other device.
- Rename and Delete operate on the shared library.
- Existing browser-local stories are automatically migrated to the server when the server library is empty.
- Backup/Restore remains available.
- vMix recording is now started by the Windows sync server at the exact countdown target, avoiding browser/CORS failures.
- During a remote countdown, the tablet automatically shows a large vMix LiveLAN preview, then switches to the teleprompter at 5 seconds remaining.
- Speed and font size use +/- buttons with the current numeric value shown; mouse-wheel speed control remains.
- Vertical flip keeps the teleprompter scrolling in the correct visual direction and uses a centered transform origin so the text stays visible.

SETUP
1. Put this entire folder somewhere permanent, for example:
   C:\NewsOneProductionSync

2. Double-click:
   start_news_one_sync.bat

3. Keep the black Command Prompt window open. It should say:
   News One Production sync server running on port 8091

4. On the Windows computer open:
   http://127.0.0.1:8091/control.html

5. On the Android tablet open the LAN address printed by the server, for example:
   http://192.168.254.149:8091/index.html

IMPORTANT
For the shared story library, use the local 8091 address on both devices. Do not use the github.io copy for the live teleprompter. A GitHub-hosted HTTPS page cannot directly use the Windows PC's HTTP API without browser mixed-content restrictions.

STORY WORKFLOW
- On the Windows computer: STORIES -> NEW STORY -> enter title/script -> SAVE STORY.
- On the tablet: STORIES -> the saved story will appear.
- If a story is saved or renamed on the tablet, it is saved to the same central library.

FIREWALL
If the tablet cannot open port 8091, allow Python through Windows Firewall on the Private network, or allow TCP 8091. Do not expose this server to the public Internet.

FILES
- index.html = teleprompter with central story library, vMix monitor, and LAN countdown sync
- control.html = vMix recording control center and countdown master
- vMix API calls are made by sync_server.py directly to 127.0.0.1:8088 so StartRecording does not depend on browser CORS
- sync_server.py = LAN server, countdown sync, and central story API
- stories.json = shared story database created automatically
- start_news_one_sync.bat = one-click launcher
- manifest.webmanifest / service-worker.js / icons = app support files
