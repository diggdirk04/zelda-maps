@echo off
rem Serves the app at http://localhost:8765 so it can be installed as an app (PWA). Needs Python.
cd /d "%~dp0web"
start "" http://localhost:8765/
python -m http.server 8765 || py -m http.server 8765
