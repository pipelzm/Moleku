# Moleku macOS portable release

`Moleku.app` is distributed as a portable macOS app bundle: the user downloads a zip, expands it, and opens the app without installing Python, RDKit, or other libraries.

Two macOS variants can be produced:

- `Moleku-macOS.zip` for the native architecture of the build machine (for example Apple Silicon / `arm64`)
- `Moleku-macOS-x86_64.zip` for Intel Macs

## Local build

Use the dedicated build environment and PyInstaller spec:

```bash
conda run -n mcrg-build env PYTHON=python bash "scripts/build_mac_app.sh"
```

That produces:

- `dist/Moleku.app`
- `dist/Moleku/` (onedir folder used by the `.app` bundle)

## Intel build from Apple Silicon

If you are on an Apple Silicon Mac and want an Intel-compatible bundle for older Macs, use:

```bash
chmod +x scripts/build_mac_intel_from_arm.sh
scripts/build_mac_intel_from_arm.sh
```

That script:

- creates an `osx-64` conda environment under Rosetta
- builds the `x86_64` PyInstaller `onedir`
- assembles `dist/Moleku-macOS-x86_64.app`
- packages `dist/Moleku-macOS-x86_64.zip`

If you are already on an Intel Mac, use `scripts/build_mac_app.sh` directly.

## Smoke test

Validate the double-click path on macOS before packaging:

```bash
chmod +x scripts/smoke_test_mac_app.sh
scripts/smoke_test_mac_app.sh "dist/Moleku.app"
```

The smoke test launches the bundle through LaunchServices, checks that the `Moleku` process stays alive, then quits it cleanly.

## Zip packaging

Create the distributable artifact with:

```bash
cd dist
ditto -c -k --sequesterRsrc --keepParent "Moleku.app" "Moleku-macOS.zip"
```

For the Intel bundle:

```bash
cd dist
ditto -c -k --sequesterRsrc --keepParent "Moleku-macOS-x86_64.app" "Moleku-macOS-x86_64.zip"
```

## Security policy

- Default local builds are ad-hoc signed by PyInstaller and are suitable for internal testing or direct sharing.
- The Intel bundle assembled from `onedir` opens correctly via LaunchServices on Apple Silicon test machines, but `codesign --verify --strict` may still be less clean than a fully native PyInstaller-generated `.app`.
- Gatekeeper assessment (`spctl`) will reject the app until it is signed with a Developer ID certificate and notarized by Apple.
- For public distribution, enable the existing codesign/notarization block in `.github/workflows/release.yml` by configuring:
  - `MACOS_SIGN_IDENTITY`
  - `MACOS_CERT_P12`
  - `MACOS_CERT_PASSWORD`
  - `APPLE_ID`
  - `APPLE_APP_SPECIFIC_PASSWORD`
  - `APPLE_TEAM_ID`

Without notarization, users may need to use right click > Open the first time.
