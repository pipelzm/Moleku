#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate platform icon files for the Moleku desktop app.

Source:
- Preferred: images/moleku_simple_icon.png  (new brand, simplified mark)
- Fallback: images/moleku_icon.png, moleku_logo.png, mini_logo.png, mcrg_logo.png

Output (placed alongside the source PNG so PyInstaller can pick them up):
- Windows: <stem>.ico   (multi-size: 16, 32, 48, 64, 128, 256)
- macOS:   <stem>.icns  (multi-size icon, via Pillow's ICNS writer)

Why Pillow's ICNS writer and not `iconutil`?
Recent macOS releases (≥ 14) ship an ``iconutil`` that rejects perfectly
valid iconsets with "Invalid Iconset.". Pillow can write a fully-spec
``.icns`` directly from a single high-resolution PNG, which is what every
modern Mac (Retina/Dock) actually needs.

Safe to run on any OS; it will generate what it can.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGES = REPO_ROOT / "images"

PNG_CANDIDATES = [
    IMAGES / "moleku_simple_icon.png",
    IMAGES / "moleku_icon.png",
    IMAGES / "moleku_logo.png",
    IMAGES / "mini_logo.png",
    IMAGES / "mcrg_logo.png",
]


def _pick_source_png() -> Path:
    for p in PNG_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError(
        "No source PNG found. Looked for: " + ", ".join(str(p) for p in PNG_CANDIDATES)
    )


def _make_ico(src_png: Path):
    try:
        from PIL import Image
    except Exception as e:
        print(f"[generate_icons] Pillow not available; skip .ico ({e})")
        return

    out = src_png.with_suffix(".ico")
    img = Image.open(src_png).convert("RGBA")
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="ICO", sizes=sizes)
    print(f"[generate_icons] wrote {out}")


def _make_icns(src_png: Path):
    try:
        from PIL import Image
    except Exception as e:
        print(f"[generate_icons] Pillow not available; skip .icns ({e})")
        return

    out = src_png.with_suffix(".icns")
    img = Image.open(src_png).convert("RGBA")
    # Pillow's ICNS writer picks the included sizes automatically. Feeding it a
    # high-res master image (≥1024×1024) yields a crisp Dock/Retina icon.
    img.save(out, format="ICNS")
    print(f"[generate_icons] wrote {out}")


def main():
    src = _pick_source_png()
    print(f"[generate_icons] source PNG: {src}")
    _make_ico(src)
    _make_icns(src)


if __name__ == "__main__":
    main()
