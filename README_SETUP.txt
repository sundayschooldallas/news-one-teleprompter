NEWS ONE PRODUCTION — vMix + Tablet Teleprompter Sync + LIVE MOUSE-WHEEL SPEED

WHAT THIS PACKAGE DOES
- Keeps your v18 teleprompter, story library, editor, orientation, countdown, mirror, font-size controls, and saved settings.
- Adds live mouse-wheel speed control to the teleprompter.
- Mouse wheel UP while reading = +1 px/sec.
- Mouse wheel DOWN while reading = -1 px/sec.
- SHIFT + mouse wheel = +/-5 px/sec.
- The page will not scroll from the mouse wheel while the teleprompter is running.
- Keeps your News One Production vMix Recording Control Center.
- When START COUNTDOWN & RECORD is clicked on the Windows PC, the tablet receives the same target start time.
- The tablet displays a synchronized countdown and starts scrolling at the target time.
- STOP RECORDING and CANCEL COUNTDOWN are also sent to the tablet.
- The tablet has a VMIX MONITOR button for vMix LiveLAN on the same network.

FILES
- index.html = synced v18 teleprompter with mouse-wheel speed control
- control.html = synced vMix Recording Control Center
- sync_server.py = small local LAN synchronization/web server
- start_news_one_sync.bat = one-click Windows launcher
- manifest.webmanifest / service-worker.js / icons = teleprompter PWA files

SETUP ON WINDOWS vMix COMPUTER
1. Unzip this whole folder somewhere permanent, for example:
   C:\NewsOneProductionSync
2. Make sure Python 3 is installed.
3. Double-click start_news_one_sync.bat.
4. Leave that black command window running while recording.
5. It will display a URL such as:
   http://192.168.1.25:8090/index.html

OPEN THE CONTROL CENTER ON WINDOWS
Open:
   http://127.0.0.1:8090/control.html

OPEN THE TELEPROMPTER ON THE ANDROID TABLET
Make sure the tablet is on the SAME Wi-Fi/LAN as the Windows vMix computer.
Open the tablet URL shown by sync_server.py, for example:
   http://192.168.1.25:8090/index.html

You can then use Chrome's menu -> Add to Home screen to make a tablet shortcut.

LIVE SPEED CONTROL
- While the teleprompter is actively scrolling, move the mouse wheel UP or DOWN.
- UP increases speed by exactly 1 px/sec.
- DOWN decreases speed by exactly 1 px/sec.
- Hold SHIFT while using the wheel for +/-5 px/sec.
- The current speed number beside SPEED updates and is saved.
- The same precise speed can still be adjusted with the on-screen speed control or keyboard arrows.

VMIX
- Keep vMix Web Controller enabled on port 8088.
- The control center keeps using 127.0.0.1:8088 on the Windows PC.
- The tablet's VMIX MONITOR button uses the Windows PC's IP and port 8088.
- For the monitor, vMix LiveLAN must be enabled/started.

FIREWALL
If the tablet cannot connect to port 8090, allow Python (or TCP port 8090) through Windows Firewall on your Private network.
Do NOT expose port 8090 to the public Internet.

SYNC DESIGN
The Windows control center is the master clock. It sends an absolute target timestamp to the sync server. The tablet estimates the PC/server clock offset and uses that target timestamp instead of starting a separate timer. This minimizes countdown drift between the two devices.

IMPORTANT
This integrated version is designed for the tablet and vMix PC to be on the same local network. It does not require a cloud account or Internet relay for synchronization.
