# Zelda Maps — offline app

Hyrule Across the Ages: the map comparison page, packaged three ways.
Everything runs locally. No account, server or internet connection is needed
(the page's web font loads from Google Fonts when you're online and falls back
to a system font when you're not).

## 1. Offline folder (quickest)

Unzip anywhere, then:

- **Windows:** double-click `run-windows.bat`. It opens the app in its own
  window using Edge or Chrome. If neither is found it opens in your default browser.
- **Linux:** run `./run-linux.sh` (or double-click it in your file manager and
  choose *Run*). It uses Chromium, Chrome, Edge or Brave if installed, otherwise
  your default browser.
- **Any system:** open `web/index.html` in a browser.

## 2. Installable web app (PWA)

A PWA gets its own icon in the Start menu / app launcher, opens in its own
window and works offline after the first load. Browsers only allow installing
from `http://localhost` or an `https://` site, so:

**Local (just you):**

- **Windows:** double-click `serve-pwa-windows.bat` (needs Python, from
  python.org or the Microsoft Store).
- **Linux:** run `./serve-pwa-linux.sh` (needs `python3`, installed on most distros).

Your browser opens `http://localhost:8765/`. In Chrome or Edge, click the
**Install** icon at the right end of the address bar (or menu → *Install Zelda Maps*).
After installing you can close the server window: the app is cached and keeps
working offline. The overworld maps are cached at install; each dungeon map is
cached the first time you open it, so open the ones you want before going offline.
(The offline folder and the desktop program always have every map.)

**Hosted (your other devices):** upload the contents of `web/` to any static
host that serves https (GitHub Pages, Netlify, Cloudflare Pages). Open the URL
on a phone or PC and choose *Install app* / *Add to Home Screen*. Keep the host
private if you can; see the note on artwork below.

## 3. Desktop program (Windows and Linux)

The `desktop/` folder is an Electron project that wraps `web/` in a native
window. You build it on your own computer (it downloads Electron, about 100 MB
once).

1. Install **Node.js 18 or newer** from nodejs.org.
2. Open a terminal in the `desktop` folder and run:

   ```
   npm install
   npm start              # try it without building
   ```

3. Build installers:

   ```
   npm run build:win      # on Windows → release/Zelda Maps Setup 1.0.0.exe + portable .exe
   npm run build:linux    # on Linux   → release/Zelda Maps-1.0.0.AppImage + .deb
   ```

   Build each platform on that platform. (Building Windows installers from
   Linux needs Wine; Linux builds from Windows need WSL.)

- **Windows:** run the Setup .exe to install (Start-menu entry and uninstaller), or
  run the portable .exe directly with no install. Windows SmartScreen may warn
  because the app isn't code-signed: click *More info → Run anyway*.
- **Linux:** `chmod +x "Zelda Maps-1.0.0.AppImage"` and run it, or
  `sudo apt install ./zelda-maps_1.0.0_amd64.deb` on Debian/Ubuntu.

Links to wikis and guides open in your normal browser, not inside the app.

## Updating

When the page changes, replace the `web/` folder with the new one (the build
script regenerates `sw.js`). For the PWA, `VERSION` at the top of `web/sw.js` changes automatically so installed copies pick up
the change. For the desktop app, rebuild.

## Note on artwork

Most map images and all map icons are Nintendo artwork or fan-made maps by
their credited creators. The extra layers and dungeon maps come from Zelda Dungeon's
map project and from randomizer tracker packs (MIT, GPL or no stated license);
each source is credited at the bottom of the page. This package is meant for personal use. Don't publish
it to an app store or a public site as-is. The Tears of the Kingdom location
data (shrines, Korok seeds and so on) is CC0 and free to reuse; it comes from
Alshival's Data Service TOTK map project and Phil, Aeon and SuperSpazzy's data
sheet.
