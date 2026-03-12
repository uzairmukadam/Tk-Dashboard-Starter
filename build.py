"""
build.py — PyInstaller packaging script for Tk Dashboard Starter
-----------------------------------------------------------------
Usage:
    python build.py              # build with defaults from config
    python build.py --onedir     # build an unpacked folder instead
    python build.py --debug      # keep the console window for debugging

Output:  dist/<APP_NAME>.exe  (or dist/<APP_NAME>/ in --onedir mode)
"""

import os
import sys
import shutil
import subprocess
import argparse


# ── Read app metadata from config so this script stays in sync ─────────────
sys.path.insert(0, os.path.dirname(__file__))
from app.config import APP_NAME, APP_VERSION  # noqa: E402

EXE_NAME  = APP_NAME.replace(" ", "_")
ICON_PATH = os.path.join("app", "assets", "app.ico")
ASSETS_DIR = os.path.join("app", "assets")


def preflight() -> None:
    """Remove packages known to be incompatible with PyInstaller."""

    # The 'typing' PyPI package is an obsolete Python 2/3.4 backport.
    # On Python 3.5+ it conflicts with PyInstaller. Auto-remove it if present.
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "typing"],
        capture_output=True,
    )
    if result.returncode == 0:
        print("  [PRE-FLIGHT] Removing obsolete 'typing' backport (incompatible with PyInstaller)...")
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "typing", "-y"],
            check=True,
        )
        print("  [PRE-FLIGHT] Done.\n")


def build(onedir: bool = False, debug: bool = False) -> None:
    print(f"\n{'='*60}")
    print(f"  Building: {APP_NAME} v{APP_VERSION}")
    print(f"  Output:   dist/{EXE_NAME}{'/' if onedir else '.exe'}")
    print(f"{'='*60}\n")

    # Clean previous build artefacts
    for folder in ("build", "dist", "__pycache__"):
        if os.path.isdir(folder):
            print(f"  Cleaning {folder}/")
            shutil.rmtree(folder)

    spec_file = f"{EXE_NAME}.spec"
    if os.path.isfile(spec_file):
        os.remove(spec_file)

    # ── Compose PyInstaller command ────────────────────────────────────────
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "main.py",
        "--noconfirm",
        "--name", EXE_NAME,
        "--windowed" if not debug else "--console",
    ]

    if not onedir:
        cmd.append("--onefile")

    # Icon (skip gracefully if not present)
    if os.path.isfile(ICON_PATH):
        cmd += ["--icon", ICON_PATH]
    else:
        print(f"  [WARN] Icon not found at {ICON_PATH!r} — building without icon.\n")

    # Bundle assets folder if it exists
    if os.path.isdir(ASSETS_DIR):
        # Windows separator is ;  (Linux/Mac use :)
        sep = ";" if sys.platform.startswith("win") else ":"
        cmd += ["--add-data", f"{ASSETS_DIR}{sep}{ASSETS_DIR}"]

    # Ensure all page modules are bundled (pkgutil discovery is dynamic;
    # PyInstaller needs this hint to include them in the frozen executable)
    cmd += ["--collect-submodules", "app.pages"]

    # ── Run PyInstaller ────────────────────────────────────────────────────
    print("  Running PyInstaller...\n")
    result = subprocess.run(cmd, check=False)

    if result.returncode == 0:
        output = f"dist/{EXE_NAME}{'/' if onedir else '.exe'}"
        print(f"\n  ✅ Build succeeded → {output}")
    else:
        print(f"\n  ❌ Build FAILED (exit code {result.returncode})")
        sys.exit(result.returncode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package the app with PyInstaller.")
    parser.add_argument("--onedir",  action="store_true", help="Build a folder instead of single .exe")
    parser.add_argument("--debug",   action="store_true", help="Keep console window for debugging")
    args = parser.parse_args()

    # Ensure PyInstaller is available
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("  PyInstaller not found. Installing...\n")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    preflight()
    build(onedir=args.onedir, debug=args.debug)
