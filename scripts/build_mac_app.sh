#!/usr/bin/env bash
# Build a double-clickable Moleku.app on macOS (PyInstaller + mcrg.spec).
# Use a dedicated conda env (see README / .github/workflows/release.yml) so the
# bundle does not pull optional heavy packages from "base" Anaconda.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY="${PYTHON:-python3}"
TARGET_ARCH="${MOLEKU_TARGET_ARCH:-$(uname -m)}"
DIST_SUFFIX="${MOLEKU_DIST_SUFFIX:-}"
APP_NAME="${MOLEKU_APP_NAME:-Moleku}"
SKIP_BUNDLE="${MOLEKU_SKIP_BUNDLE:-0}"
if ! "$PY" -c "import rdkit, PyInstaller" 2>/dev/null; then
  echo "Need Python with rdkit and pyinstaller on PATH (e.g. conda-forge env)."
  echo "Example:"
  echo "  mamba create -y -n moleku-build -c conda-forge python=3.11 rdkit pandas pillow pyinstaller"
  echo "  mamba activate moleku-build && pip install customtkinter matplotlib numpy"
  echo "  PYTHON=python scripts/build_mac_app.sh"
  exit 1
fi

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This script targets macOS (.app). On Windows/Linux use the same spec:"
  echo "  pyinstaller --clean --noconfirm mcrg.spec"
  exit 1
fi

ensure_admet_local_stack() {
  echo "Ensuring ADMET local build stack..."
  "$PY" -m pip install --upgrade \
    "setuptools<81" \
    "pyinstaller-hooks-contrib>=2026.4" \
    "torch==2.2.2" \
    "admet-ai==1.3.1" \
    py4j
}

copy_legal_files() {
  local target_dir="$1"
  [[ -d "$target_dir" ]] || return 0

  if [[ -f "$ROOT/LICENSE" ]]; then
    cp "$ROOT/LICENSE" "$target_dir/LICENSE"
  fi
  if [[ -f "$ROOT/NOTICE" ]]; then
    cp "$ROOT/NOTICE" "$target_dir/NOTICE"
  fi
}

echo "Building macOS app:"
echo "  python: $("$PY" -c 'import sys; print(sys.executable)')"
echo "  target_arch: $TARGET_ARCH"

# Keep ADMET local available inside the frozen app bundle with a
# cross-architecture-compatible stack that PyInstaller can package reliably.
ensure_admet_local_stack

rm -rf "dist/Moleku.app" "dist/Moleku" "build/mcrg"
"$PY" scripts/generate_icons.py
MOLEKU_TARGET_ARCH="$TARGET_ARCH" MOLEKU_SKIP_BUNDLE="$SKIP_BUNDLE" "$PY" -m PyInstaller --clean --noconfirm mcrg.spec

if [[ "$SKIP_BUNDLE" == "1" ]]; then
  APP_BUNDLE_PATH=""
elif [[ -n "$DIST_SUFFIX" ]]; then
  rm -rf "dist/${APP_NAME}-${DIST_SUFFIX}.app" "dist/${APP_NAME}-${DIST_SUFFIX}"
  mv "dist/Moleku.app" "dist/${APP_NAME}-${DIST_SUFFIX}.app"
  mv "dist/Moleku" "dist/${APP_NAME}-${DIST_SUFFIX}"
  APP_BUNDLE_PATH="$ROOT/dist/${APP_NAME}-${DIST_SUFFIX}.app"
else
  APP_BUNDLE_PATH="$ROOT/dist/Moleku.app"
fi

if [[ "$SKIP_BUNDLE" == "1" ]]; then
  copy_legal_files "$ROOT/dist/Moleku"
elif [[ -n "${APP_BUNDLE_PATH:-}" && -d "$APP_BUNDLE_PATH/Contents/Resources" ]]; then
  copy_legal_files "$APP_BUNDLE_PATH/Contents/Resources"
fi

echo ""
if [[ "$SKIP_BUNDLE" == "1" ]]; then
  echo "Build onedir listo:"
  echo "  $ROOT/dist/Moleku/"
elif [[ -n "$DIST_SUFFIX" ]]; then
  echo "Listo. Abre en Finder:"
  echo "  $APP_BUNDLE_PATH"
  echo "(También existe la carpeta onedir: $ROOT/dist/${APP_NAME}-${DIST_SUFFIX}/ )"
else
  echo "Listo. Abre en Finder:"
  echo "  $APP_BUNDLE_PATH"
  echo "(También existe la carpeta onedir: $ROOT/dist/Moleku/ )"
fi
