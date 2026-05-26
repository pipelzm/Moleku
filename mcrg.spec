#!/usr/bin/env python3
# -*- mode: python ; coding: utf-8 -*-

import os
import sys

from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None
_TARGET_ARCH = os.environ.get("MOLEKU_TARGET_ARCH") or None
_SKIP_BUNDLE = os.environ.get("MOLEKU_SKIP_BUNDLE") == "1"

datas = [("images", "images"), ("examples", "examples")]
binaries = []
hiddenimports = []
hiddenimports += collect_submodules("customtkinter")
# The GUI entrypoint lazily imports modules under `mcrg/` behind try/except.
# Make them explicit so the frozen app does not start without its UI modules.
hiddenimports += collect_submodules("mcrg")

# RDKit ships native libs; bundle it explicitly. (Avoid collect_all on pandas/numpy/matplotlib here:
# on full Anaconda that can pull torch/sphinx and make the build huge and slow.)
try:
    _rdkit_bundle = collect_all("rdkit")
    datas += _rdkit_bundle[0]
    binaries += _rdkit_bundle[1]
    hiddenimports += _rdkit_bundle[2]
except Exception:
    pass

# ADMET local is a first-class packaged feature. Bundle its package explicitly so
# the frozen app can run offline predictions instead of falling back to the
# runtime "missing library" message.
try:
    _admet_bundle = collect_all("admet_ai")
    datas += _admet_bundle[0]
    binaries += _admet_bundle[1]
    hiddenimports += _admet_bundle[2]
except Exception:
    pass

try:
    _py4j_bundle = collect_all("py4j")
    datas += _py4j_bundle[0]
    binaries += _py4j_bundle[1]
    hiddenimports += _py4j_bundle[2]
except Exception:
    pass

# When PyInstaller runs from a full Anaconda "base", hooks can pull huge optional stacks
# (torch, skimage, Qt, …) that Moleku never imports; that bloated graph can fail COLLECT
# (missing .so) or produce multi‑GB bundles. These excludes keep the app lean.
_EXCLUDE_BLOAT = [
    "torchvision",
    "torchaudio",
    "tensorboard",
    "jax",
    "jaxlib",
    "skimage",
    "keras",
    "tensorflow",
    "IPython",
    "jupyter",
    "notebook",
    "jupyterlab",
    "sphinx",
    "astropy",
    "PyQt5",
    "PyQt6",
    "PySide2",
    "PySide6",
    "black",
    "pytest",
]

a = Analysis(
    # Use the GUI module directly as the frozen entrypoint.
    # (On macOS, the previous wrapper `mcrg_entry.py` could not reliably import
    # the top-level module when packaged, resulting in a silent no-op on double click.)
    ["mcrg_desktop.py"],
    pathex=[os.path.abspath(".")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=_EXCLUDE_BLOAT,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


def _platform_icon_path():
    """Resolve a platform-appropriate executable icon, preferring the new
    Moleku assets and falling back to the legacy MCR-G icons (or PNG)."""
    # Preferred names (new Moleku brand).
    win_candidates = ["moleku_simple_icon.ico", "moleku_icon.ico", "moleku_logo.ico"]
    mac_candidates = ["moleku_simple_icon.icns", "moleku_icon.icns", "moleku_logo.icns"]
    png_candidates = ["moleku_simple_icon.png", "moleku_icon.png", "moleku_logo.png"]
    # Legacy fallbacks (older builds).
    legacy_win = ["mini_logo.ico", "mcrg_logo.ico"]
    legacy_mac = ["mini_logo.icns", "mcrg_logo.icns"]
    legacy_png = ["mini_logo.png", "mcrg_logo.png", "mcrg_logo_simple.png"]

    def _first_existing(names):
        for n in names:
            p = os.path.join("images", n)
            if os.path.exists(p):
                return p
        return None

    if sys.platform.startswith("win"):
        return _first_existing(win_candidates + legacy_win + png_candidates + legacy_png)
    if sys.platform == "darwin":
        return _first_existing(mac_candidates + legacy_mac + png_candidates + legacy_png)
    return _first_existing(png_candidates + legacy_png)


_APP_ICON = _platform_icon_path()

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Moleku",
    icon=_APP_ICON,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # windowed (no terminal)
    disable_windowed_traceback=False,
    # Do not enable argv emulation for the Tkinter GUI bundle on macOS.
    # PyInstaller documents conflicts with Tcl/Tk app startup events that can
    # manifest as menu-bar crashes on double-click launch.
    argv_emulation=False,
    target_arch=_TARGET_ARCH,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Moleku",
)

# macOS: real double-clickable .app (Finder). Other OSes: use dist/Moleku/Moleku(.exe).
if sys.platform == "darwin" and not _SKIP_BUNDLE:
    from PyInstaller.building.osx import BUNDLE

    _icns = None
    for _candidate in ("moleku_simple_icon.icns", "moleku_icon.icns", "moleku_logo.icns", "mini_logo.icns", "mcrg_logo.icns"):
        _p = os.path.join("images", _candidate)
        if os.path.exists(_p):
            _icns = _p
            break

    app = BUNDLE(
        coll,
        name="Moleku.app",
        icon=_icns,
        bundle_identifier="cl.ufro.moleku",
        version="1.0.0",
        info_plist={
            "CFBundleDisplayName": "Moleku",
            "CFBundleName": "Moleku",
            "NSHighResolutionCapable": True,
        },
    )
