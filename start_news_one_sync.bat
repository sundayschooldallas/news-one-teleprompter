@echo off
title News One Production v32 Sync Server - PORT 8093
cd /d "%~dp0"
echo.
echo Starting News One Production v32 from:
echo %CD%
echo.
echo News One sync uses PORT 8093.
echo This does NOT use or manage pipeline ports 8000, 8002, 8010, 8011, 8012, or 5173.
echo.
py sync_server.py
pause
