#!/usr/bin/env sh
# Opens Zelda Maps in its own app window (Chromium/Chrome/Edge if installed), fully offline.
DIR="$(cd "$(dirname "$0")" && pwd)"
URL="file://$DIR/web/index.html"
for b in chromium chromium-browser google-chrome google-chrome-stable microsoft-edge brave-browser; do
  if command -v "$b" >/dev/null 2>&1; then exec "$b" --app="$URL"; fi
done
exec xdg-open "$URL"
