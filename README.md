# Zelda Maps

Interactive maps for every mainline Zelda game: overworlds, dungeons, item and place-name layers, progress tracking, cross-game blends (ALttP / ALBW / EoW), deep zoom, dual-screen support and gamepad controls. It runs as a single web page, an Android app and a Linux AppImage.

## Layout

| Path | What it is |
|---|---|
| `site/` | The built web app. `site/index.html` is self-contained apart from `site/maps/` and `site/icons/`. |
| `gamepage.js`, `gamepage.css`, `theme.css`, `gp*.js`, `lbzoom.js` | Viewer source; `build.py` inlines them into `site/index.html`. |
| `build.py` | Builds `site/index.html` (games, layers, dungeons, packs). |
| `extract_*.py`, `manual_layers.py`, `layers.py` → `xldata.js` | Marker and label data, extracted from open-source tracker packs. |
| `build_dungeons.py` → `dungeons.js` | Dungeon floor maps. |
| `build_xa.py` | Cross-game blend images (`site/maps/xa_*.webp`). |
| `hd/` | Deep-zoom tiles: `make_hd.py` (overworlds), `make_xa_hd.py` (blends), `embed.py` (writes the tile table into `gamepage.js`). |
| `pack_dg.py` | Bundles tiles into `_*pack.webp` files for hosts with a file-count limit (generated, not committed). |
| `build_app.py` → `dist/zelda-maps-app/web` | Offline app web root (used by the APK and AppImage). |
| `build/apk/` | Android app (apktool project: manifest, smali, resources). Web content is copied into `assets/web/` at build time. |
| `build/AppDir/` | Linux AppImage skeleton (Electron launcher: `AppRun`, `resources/app/main.js`). |
| `*test.py` | Playwright checks (desktop, Android WebView emulation, deep zoom, blends). |

## Building

```sh
python3 hd/embed.py          # after regenerating HD tiles
python3 build.py             # -> site/index.html (+ site/maps/dg/_*pack.webp)
python3 build_app.py         # -> dist/zelda-maps-app/web

# Android (apktool + uber-apk-signer)
cp -r dist/zelda-maps-app/web/{index.html,manifest.webmanifest,appicons,icons,maps} build/apk/assets/web/
java -jar apktool.jar b build/apk -o zelda-maps-unsigned.apk
java -jar uber-apk-signer.jar -a zelda-maps-unsigned.apk -o signed

# Linux AppImage (needs Electron unpacked into build/AppDir/usr/lib/zelda-maps/)
cp -r dist/zelda-maps-app/web build/AppDir/usr/lib/zelda-maps/resources/web
ARCH=x86_64 appimagetool build/AppDir Zelda_Maps-x86_64.AppImage
```

The APK and AppImage are over GitHub's 100 MB file limit, so they belong on the Releases page, not in the repository.

## License

The original code is MIT-licensed (see `LICENSE`). Nintendo's material and the third-party data and images listed in `THIRD_PARTY_NOTICES.md` are not covered by it and keep their own licenses.

## Credits

The marker data and some map images come from open-source projects, each under its own license. They're credited in the app's footer and in the source of each extractor. They include Zelda Dungeon maps, objmap, MrCheeze's BotW map, the Archipelago and PopTracker packs (ALBW, ALttP, MM, OoT, OoS/OoA, PH, ST, TMC, TP, WW), Piranhaplant and the DarkZant TP map. The Legend of Zelda and its maps are © Nintendo. This is an unofficial fan project.
