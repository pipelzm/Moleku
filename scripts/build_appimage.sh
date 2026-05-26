#!/usr/bin/env bash
set -euo pipefail

# Builds an AppImage from the PyInstaller dist/ output.
#
# Expected dist layout after `pyinstaller mcrg.spec`:
#   dist/Moleku/...
#
# Output:
#   dist/Moleku-Linux.AppImage

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"
APP_NAME="Moleku"
APPDIR="${DIST_DIR}/${APP_NAME}.AppDir"

if [[ ! -d "${DIST_DIR}/${APP_NAME}" ]]; then
  echo "Missing ${DIST_DIR}/${APP_NAME}. Run PyInstaller first." >&2
  exit 1
fi

rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/bin"

# Copy PyInstaller one-folder distribution into AppDir.
cp -R "${DIST_DIR}/${APP_NAME}/." "${APPDIR}/usr/bin/"

# Desktop file + icon
mkdir -p "${APPDIR}/usr/share/applications"
cp "${ROOT_DIR}/packaging/linux/Moleku.desktop" "${APPDIR}/${APP_NAME}.desktop"

# Use the new Moleku brand icon (with sensible fallbacks). Must be named .png so
# linuxdeploy picks it up. We keep the destination filename in sync with the
# Icon= entry in packaging/linux/Moleku.desktop.
ICON_DST="${APPDIR}/moleku_simple_icon.png"
if [[ -f "${ROOT_DIR}/images/moleku_simple_icon.png" ]]; then
  cp "${ROOT_DIR}/images/moleku_simple_icon.png" "${ICON_DST}"
elif [[ -f "${ROOT_DIR}/images/moleku_icon.png" ]]; then
  cp "${ROOT_DIR}/images/moleku_icon.png" "${ICON_DST}"
elif [[ -f "${ROOT_DIR}/images/moleku_logo.png" ]]; then
  cp "${ROOT_DIR}/images/moleku_logo.png" "${ICON_DST}"
elif [[ -f "${ROOT_DIR}/images/mcrg_logo.png" ]]; then
  cp "${ROOT_DIR}/images/mcrg_logo.png" "${ICON_DST}"
fi

# AppRun shim (simple launcher)
cat > "${APPDIR}/AppRun" <<'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/Moleku/Moleku" "$@"
EOF
chmod +x "${APPDIR}/AppRun"

# Download linuxdeploy + appimagetool (if not present)
TOOLS_DIR="${DIST_DIR}/.appimage-tools"
mkdir -p "${TOOLS_DIR}"

LINUXDEPLOY="${TOOLS_DIR}/linuxdeploy-x86_64.AppImage"
APPIMAGETOOL="${TOOLS_DIR}/appimagetool-x86_64.AppImage"

if [[ ! -f "${LINUXDEPLOY}" ]]; then
  curl -L -o "${LINUXDEPLOY}" "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
  chmod +x "${LINUXDEPLOY}"
fi
if [[ ! -f "${APPIMAGETOOL}" ]]; then
  curl -L -o "${APPIMAGETOOL}" "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
  chmod +x "${APPIMAGETOOL}"
fi

export ARCH=x86_64
"${LINUXDEPLOY}" --appdir "${APPDIR}" --output appimage --appimage-extract-and-run

# linuxdeploy outputs something like Moleku-x86_64.AppImage in current dir.
OUT="$(ls -1 "${DIST_DIR}"/*.AppImage 2>/dev/null | head -n 1 || true)"
if [[ -z "${OUT}" ]]; then
  OUT="$(ls -1 ./*.AppImage 2>/dev/null | head -n 1 || true)"
fi
if [[ -z "${OUT}" ]]; then
  echo "AppImage output not found." >&2
  exit 1
fi

mv -f "${OUT}" "${DIST_DIR}/Moleku-Linux.AppImage"
echo "Wrote ${DIST_DIR}/Moleku-Linux.AppImage"
