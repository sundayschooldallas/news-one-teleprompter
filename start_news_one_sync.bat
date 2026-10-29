@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py sync_server.py
  goto :eof
)
where python >nul 2>&1
if %errorlevel%==0 (
  python sync_server.py
  goto :eof
)
echo.
echo Python was not found on this PC.
echo Install Python 3, then run this file again.
pause
