NEWS ONE PRODUCTION v26
- START always resets the teleprompter to paused before countdown.
- vMix LiveLAN preview from 10 through 6 seconds.
- At 5 seconds the preview switches to teleprompter, but scrolling remains paused.
- At 0 the server starts vMix recording and then the tablet begins scrolling.
- STOP cancels countdown and prevents pending recording.
- Existing story library, speed/font buttons, mouse wheel, mirror, rotate, fullscreen and flips retained.


v26 HOTFIX: corrected a JavaScript duplicate-const syntax error that prevented the sync polling and vMix preview code from running. Added a visible vMix preview loading state and safer LiveLAN fallback.


v27 HOTFIX: corrected server version/banner and printed the actual PC LAN URL (192.168.254.149). Do not use the YOUR-PC-IP placeholder.


v28 HOTFIX: removed duplicate VMIX_PAGE JavaScript declaration that caused the entire teleprompter script to fail and left status at CONNECTING.
