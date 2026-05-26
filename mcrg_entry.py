"""
PyInstaller entrypoint.

The GUI lives in `mcrg_desktop.py` (not `MCRG.py`): on macOS default APFS is
case-insensitive, so `import MCRG` can resolve to the `mcrg` package and break
`from MCRG import main` in the frozen app (double-click appears to do nothing).
"""

from mcrg_desktop import main


if __name__ == "__main__":
    main()

