@echo off
title News One Production v37 Sync Server - PORT 8093
cd /d "%~dp0"
echo.
echo Starting News One Production v37 from:
echo %CD%
echo.
echo News One sync uses PORT 8093.
echo vMix remains on its normal Web Controller / LiveLAN port 8088.
echo This does NOT use or manage pipeline ports 8000, 8002, 8010, 8011, 8012, or 5173.
echo.
py sync_server.py
pause
