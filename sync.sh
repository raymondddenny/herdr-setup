#!/bin/sh
# Copy this Herdr app setup from the live app home into the repo.
# Run after changing anything in ~/.config/herdr-app, then commit.
set -eu
H="${HERDR_APP_HOME:-$HOME/.config/herdr-app}"
R="$(cd "$(dirname "$0")" && pwd)"
P="$R/pixel"
mkdir -p "$P/layouts" "$P/themes" "$P/mods" "$R/home"
cp "$H/layouts/pixel.json" "$P/layouts/"
cp "$H/themes/pixel.json" "$P/themes/"
for m in pixel-spaces pixel-agents; do
  # The .d.ts and jsconfig files are rewritten by the app on every start.
  rsync -a --delete --exclude gpui-kit.d.ts --exclude jsconfig.json --exclude __pycache__ "$H/mods/$m/" "$P/mods/$m/"
done
cp "$H/settings.json" "$H/keys.json" "$R/home/"
(cd "$P/mods/pixel-agents" && python3 sprites.py "$R/docs/sprites.svg" >/dev/null && rm -rf __pycache__)
echo "synced from $H"
