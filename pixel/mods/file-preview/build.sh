#!/bin/sh
# Turns one image or PDF ($1) into PNG pages in a cache folder ($2) that Herdr's
# image() can load, plus $2/manifest with "<file> <width> <height>" per page.
set -eu
src=$1 out=$2 here=$(cd "$(dirname "$0")" && pwd)
[ -f "$out/manifest" ] && exit 0
mkdir -p "$out"
dims() { sips -g pixelWidth -g pixelHeight "$1" | awk '/pixelWidth/ {w = $2} /pixelHeight/ {h = $2} END {print w, h}'; }
ext=$(printf '%s' "${src##*.}" | tr '[:upper:]' '[:lower:]')
case "$ext" in
  pdf)
    bin=$here/.cache/pdf2png
    [ -x "$bin" ] || { mkdir -p "$here/.cache" && swiftc -O "$here/pdf2png.swift" -o "$bin"; }
    "$bin" "$src" "$out" > "$out/manifest.tmp" ;;
  png|jpg|jpeg|gif|webp)
    cp "$src" "$out/page-1.$ext"
    echo "page-1.$ext $(dims "$src")" > "$out/manifest.tmp" ;;
  svg)
    cp "$src" "$out/page-1.svg"
    size=$(tr '\n' ' ' < "$src" | sed -n 's/.*viewBox="[-0-9.]*[ ,]*[-0-9.]*[ ,]*\([0-9.]*\)[ ,]*\([0-9.]*\)".*/\1 \2/p')
    echo "page-1.svg ${size:-1 1}" > "$out/manifest.tmp" ;;
  *)
    # HEIC, TIFF, BMP and the rest: let macOS convert them.
    sips -s format png "$src" --out "$out/page-1.png" > /dev/null
    echo "page-1.png $(dims "$out/page-1.png")" > "$out/manifest.tmp" ;;
esac
mv "$out/manifest.tmp" "$out/manifest"
