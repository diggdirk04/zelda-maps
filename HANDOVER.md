# Handover

The original author has stopped working on Zelda Maps and is leaving it to the public. Nobody is reviewing issues or pull requests here. The way forward is a fork: take the code, make it yours and release it under your own name.

## Status at handover (v1.15)

Everything in the 1.15 release works as far as it was tested: the web page and all overworld and dungeon maps, the layers and progress tracking, deep zoom on 28 maps, cross-game blends with label flip, dual-screen mode on the AYN Thor, and gamepad controls.

Things that were never done or never verified:

- **macOS builds were never run on a Mac.** GitHub's Mac build machines weren't available to this account, so the release workflow assembles the .app on Linux from Electron's official macOS build and ad-hoc signs it with rcodesign. If you have Mac runners, switching back to electron-builder on `macos-latest` is simpler and gives a .dmg.
- **The Windows builds were never launched**, and no build is code-signed.
- **Missing content:** Echoes of Wisdom dungeons, Tri Force Heroes layers, BotW shrine interiors and Skyward Sword sky markers.
- **No high-resolution source exists** for TotK Sky, the ALBW maps (2048 px), Four Swords, Four Swords Adventures or Tri Force Heroes.
- **Zoom smoothness was tuned blind:** the 1.13–1.14 deep-zoom changes were never measured on a real phone. If zooming judders, look at `HD_MAXT` and the `.zooming` rules in `gamepage.js` and `gamepage.css`.

## Picking it up

1. **Fork the repository**, or copy it into a new one if you'd rather start fresh.
2. **Check the licenses first** (`THIRD_PARTY_NOTICES.md`). The code is MIT, but the map images are Nintendo's, and several data sources state no license. Before publishing widely, ask those authors or drop their data. Some data is GPL-3/AGPL-3 and must stay under those terms.
3. **Build:** `python3 build.py` makes `site/index.html`, and `python3 build_app.py` makes the offline package. The README explains the full layout.
4. **Release:** in your fork, enable Actions and either push a tag like `v1.16` or open Actions → Release → Run workflow. One run builds and publishes every download.

## The Android signing key

Every APK so far is signed with the public debug key that ships inside uber-apk-signer 1.3.0. The workflow stops if that ever changes, and that's what lets new versions install over old ones. It also means anyone can sign an APK that installs over this one. If you take the project over seriously:

- Switch to your own release key: generate a keystore, store it as a repository secret, and pass `--ks` to uber-apk-signer in `.github/workflows/release.yml`.
- Change the package name in `build/apk/AndroidManifest.xml` (and the smali paths) so your app installs alongside this one instead of on top of it.
- Tell users they'll need to reinstall once.

## Things to know before you start

- **Committed build output:** the deep-zoom tiles in `site/maps/dg/` and the extracted data (`xldata.js`, `dungeons.js`, `totkdata.js`) are committed. The scripts that regenerate them (`hd/*.py`, `extract_*.py`) need the original source images and tracker packs. Those aren't in the repository, and the scripts still contain the original machine's paths (`/home/claude/...`, `/mnt/user-data/uploads/...`). To regenerate, fetch the sources listed in `THIRD_PARTY_NOTICES.md` and point the scripts at them.
- **One-off scripts:** many root-level `*test.py`, `shot*.py` and `add*.py` files were one-off development scripts. The ones worth keeping are `androidtest.py`, `hdtest.py`, `blendtest.py` and `bugtest.py`.
- **Progress sync:** `gpsync.js` only works when the page is hosted as a claude.ai artifact. Everywhere else it stays off, and progress moves between devices with Export and Import. A successor could swap in their own backend or remove it.

## Where things live

- **Viewer:** `gamepage.js`, `gamepage.css` and `theme.css`, plus `gpdual.js` (dual screen), `gpad.js` (gamepad), `gpsync.js` (progress sync) and `lbzoom.js` (home-page lightbox).
- **Data:** `extract_xl.py` builds `xldata.js` (layers from tracker packs), `build_dungeons.py` builds `dungeons.js`, and `manual_layers.py` holds the hand-placed layers.
- **Deep zoom:** `hd/make_hd.py` (overworld tiles), `hd/make_xa_hd.py` (blend tiles), `hd/embed.py` (writes the tile table into `gamepage.js`).
- **Cross-game alignment:** `build_xa.py` (blend images) and `hd/xa_lbl.json` (label placement for the flip).
- **Apps:**
  - Android: `build/apk/` (apktool project).
  - Desktop: `app/desktop/` (Electron).
  - Offline package and PWA files: `app/`.
- **Tests:** `*test.py` (Playwright). `androidtest.py` emulates the Thor, `hdtest.py` covers deep zoom and `blendtest.py` covers blends.

Thanks for picking it up.
