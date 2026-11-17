#!/usr/bin/env sh
# Serves the app at http://localhost:8765 so it can be installed as an app (PWA). Needs Python 3.
cd "$(dirname "$0")/web" || exit 1
( sleep 1; xdg-open http://localhost:8765/ >/dev/null 2>&1 ) &
exec python3 -m http.server 8765
