@echo off
rem Opens Zelda Maps in its own app window (Edge or Chrome), fully offline.
set "PAGE=%~dp0web\index.html"
set "URL=file:///%PAGE:\=/%"
where msedge >nul 2>nul && (start "" msedge --app="%URL%" & exit /b)
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app="%URL%" & exit /b)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app="%URL%" & exit /b)
start "" "%PAGE%"
