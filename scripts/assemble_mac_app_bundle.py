#!/usr/bin/env python3

from __future__ import annotations

import argparse
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble a macOS .app bundle from a PyInstaller onedir output.")
    parser.add_argument("source_dir", help="Path to the PyInstaller onedir folder (for example dist/Moleku).")
    parser.add_argument("output_app", help="Path to the output .app bundle.")
    parser.add_argument("--app-display-name", default="Moleku", help="User-visible app name.")
    parser.add_argument("--bundle-id", default="cl.ufro.moleku", help="macOS bundle identifier.")
    parser.add_argument("--version", default="1.0.0", help="Bundle version.")
    parser.add_argument("--icon", default="images/moleku_simple_icon.icns", help="Relative path to the .icns icon.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    source_dir = (root / args.source_dir).resolve() if not Path(args.source_dir).is_absolute() else Path(args.source_dir)
    output_app = (root / args.output_app).resolve() if not Path(args.output_app).is_absolute() else Path(args.output_app)

    exe_name = "Moleku"
    exe_path = source_dir / exe_name
    internal_dir = source_dir / "_internal"
    if not exe_path.exists():
        raise SystemExit(f"Executable not found: {exe_path}")
    if not internal_dir.exists():
        raise SystemExit(f"Internal payload not found: {internal_dir}")

    if output_app.exists():
        shutil.rmtree(output_app)

    contents_dir = output_app / "Contents"
    macos_dir = contents_dir / "MacOS"
    frameworks_dir = contents_dir / "Frameworks"
    resources_dir = contents_dir / "Resources"
    macos_dir.mkdir(parents=True, exist_ok=True)
    frameworks_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(exe_path, macos_dir / exe_name)
    shutil.copytree(internal_dir, frameworks_dir, dirs_exist_ok=True)

    # Python package metadata is not needed at runtime and can confuse codesign
    # when it appears under Frameworks in a manually assembled bundle.
    for pattern in ("*.dist-info", "*.egg-info"):
        for meta_dir in frameworks_dir.rglob(pattern):
            if meta_dir.is_dir():
                shutil.rmtree(meta_dir)
            elif meta_dir.exists():
                meta_dir.unlink()

    icon_path = (root / args.icon).resolve() if not Path(args.icon).is_absolute() else Path(args.icon)
    if icon_path.exists():
        shutil.copy2(icon_path, resources_dir / icon_path.name)
        icon_name = icon_path.name
    else:
        icon_name = None

    for legal_name in ("LICENSE", "NOTICE"):
        legal_path = root / legal_name
        if legal_path.exists():
            shutil.copy2(legal_path, resources_dir / legal_name)

    info_plist = {
        "CFBundleDisplayName": args.app_display_name,
        "CFBundleExecutable": exe_name,
        "CFBundleIdentifier": args.bundle_id,
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleName": args.app_display_name,
        "CFBundlePackageType": "APPL",
        "CFBundleShortVersionString": args.version,
        "NSHighResolutionCapable": True,
    }
    if icon_name:
        info_plist["CFBundleIconFile"] = icon_name

    with (contents_dir / "Info.plist").open("wb") as f:
        plistlib.dump(info_plist, f)

    def _is_macho(path: Path) -> bool:
        if not path.is_file():
            return False
        try:
            out = subprocess.check_output(["/usr/bin/file", str(path)], text=True, stderr=subprocess.DEVNULL)
        except Exception:
            return False
        return "Mach-O" in out

    code_paths: list[Path] = []
    for path in sorted(frameworks_dir.rglob("*")):
        if _is_macho(path):
            code_paths.append(path)

    for code_path in code_paths:
        subprocess.run(
            ["/usr/bin/codesign", "--force", "--sign", "-", str(code_path)],
            check=True,
        )

    try:
        subprocess.run(
            ["/usr/bin/codesign", "--force", "--sign", "-", str(output_app)],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(
            "Warning: ad-hoc bundle signing did not complete cleanly; "
            "continuing because the smoke test is the authoritative runtime check.",
            file=sys.stderr,
        )
        print(exc, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
