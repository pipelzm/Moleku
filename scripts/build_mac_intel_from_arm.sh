#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This script only runs on macOS."
  exit 1
fi

if [[ "$(uname -m)" != "arm64" ]]; then
  echo "This helper is intended for Apple Silicon Macs building an Intel bundle."
  echo "On an Intel Mac, run scripts/build_mac_app.sh directly."
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! arch -x86_64 /usr/bin/true >/dev/null 2>&1; then
  echo "Rosetta is required. Install it with:"
  echo "  softwareupdate --install-rosetta --agree-to-license"
  exit 1
fi

ENV_NAME="${MOLEKU_INTEL_ENV_NAME:-mcrg-build-intel}"
echo "Preparing Intel build environment: $ENV_NAME"

CONDA_SUBDIR=osx-64 conda create -y -n "$ENV_NAME" -c conda-forge \
  python=3.11 rdkit pandas pillow pyinstaller pytest matplotlib numpy reportlab

CONDA_SUBDIR=osx-64 conda run -n "$ENV_NAME" python -m pip install --upgrade pip
CONDA_SUBDIR=osx-64 conda run -n "$ENV_NAME" python -m pip install --upgrade \
  "setuptools<81" \
  "pyinstaller-hooks-contrib>=2026.4" \
  "torch==2.2.2" \
  "admet-ai==1.3.1" \
  py4j \
  customtkinter

echo "Building x86_64 app bundle under Rosetta..."
arch -x86_64 /bin/zsh -lc "
  cd \"$ROOT\" && \
  source /opt/anaconda3/etc/profile.d/conda.sh && \
  conda activate \"$ENV_NAME\" && \
  env \
    PYTHON=python \
    MOLEKU_TARGET_ARCH=x86_64 \
    MOLEKU_SKIP_BUNDLE=1 \
    bash \"scripts/build_mac_app.sh\"
"

echo "Assembling Intel .app bundle..."
python3 "$ROOT/scripts/assemble_mac_app_bundle.py" "dist/Moleku" "dist/Moleku-macOS-x86_64.app"

echo "Smoke testing Intel bundle..."
"$ROOT/scripts/smoke_test_mac_app.sh" "$ROOT/dist/Moleku-macOS-x86_64.app"

echo "Packaging Intel zip..."
rm -f "$ROOT/dist/Moleku-macOS-x86_64.zip"
(
  cd "$ROOT/dist"
  ditto -c -k --sequesterRsrc --keepParent "Moleku-macOS-x86_64.app" "Moleku-macOS-x86_64.zip"
)

echo ""
echo "Intel build ready:"
echo "  $ROOT/dist/Moleku-macOS-x86_64.app"
echo "  $ROOT/dist/Moleku-macOS-x86_64.zip"
