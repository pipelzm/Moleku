#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This smoke test only runs on macOS."
  exit 1
fi

APP_PATH="${1:-dist/Moleku.app}"
if [[ ! -d "$APP_PATH" ]]; then
  echo "App bundle not found: $APP_PATH"
  exit 1
fi

APP_NAME="$(basename "$APP_PATH" .app)"
INFO_PLIST="$APP_PATH/Contents/Info.plist"
if [[ -f "$INFO_PLIST" ]]; then
  APP_DISPLAY_NAME="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleDisplayName' "$INFO_PLIST" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Print :CFBundleName' "$INFO_PLIST" 2>/dev/null || true)"
  if [[ -n "${APP_DISPLAY_NAME:-}" ]]; then
    APP_NAME="$APP_DISPLAY_NAME"
  fi
fi

open -n "$APP_PATH"
sleep 5

if [[ "$(/usr/bin/osascript -e "tell application \"System Events\" to (name of processes) contains \"$APP_NAME\"")" != "true" ]]; then
  echo "Smoke test failed: $APP_NAME did not stay running after launch."
  exit 1
fi

/usr/bin/osascript -e "tell application \"$APP_NAME\" to quit"
sleep 2

if [[ "$(/usr/bin/osascript -e "tell application \"System Events\" to (name of processes) contains \"$APP_NAME\"")" != "false" ]]; then
  echo "Smoke test failed: $APP_NAME did not quit cleanly."
  exit 1
fi

echo "Smoke test OK: $APP_NAME launched and quit cleanly."
