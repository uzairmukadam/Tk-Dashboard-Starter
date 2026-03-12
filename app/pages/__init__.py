"""
Page auto-discovery for both development and PyInstaller frozen builds.

HOW IT WORKS
------------
Development:
    pkgutil.iter_modules() scans __path__ and finds every .py file in this
    package directory.

PyInstaller (frozen):
    pkgutil.iter_modules() returns nothing inside a frozen bundle, so we fall
    back to scanning sys.modules for submodules of this package that are
    already loaded.  The explicit imports at the top of this file are what
    guarantee those submodules are present in sys.modules at startup — they
    also act as static dependency hints that PyInstaller's analyser picks up
    automatically when building.

ADDING A NEW PAGE
-----------------
1. Create app/pages/my_page.py with a BasePage subclass.
2. Add an explicit import below (keeps the frozen build working).
3. Add the page to SIDEBAR_ITEMS in app/config.py.
"""

from __future__ import annotations

import sys
import pkgutil
import importlib
import inspect
from .base_page import BasePage

# ── Explicit imports — two purposes: ──────────────────────────────────────
#   1. PyInstaller's static analyser sees these and bundles the modules.
#   2. The modules are present in sys.modules for the frozen-mode fallback.
from . import home          # noqa: F401
from . import about         # noqa: F401
from . import settings      # noqa: F401
from . import data_table    # noqa: F401


def discover_pages() -> dict:
    """Return {ClassName: class} for every BasePage subclass in this package."""
    pages: dict = {}
    package = __name__

    # ── Collect module names from both sources ─────────────────────────────
    module_names: set[str] = set()

    # Source 1: pkgutil (works in development; may return nothing when frozen)
    for _, name, _ in pkgutil.iter_modules(__path__):
        if name != "base_page":
            module_names.add(name)

    # Source 2: sys.modules fallback (works in PyInstaller frozen bundles)
    prefix = package + "."
    for key in sys.modules:
        if key.startswith(prefix):
            part = key[len(prefix):]
            if "." not in part and part != "base_page":
                module_names.add(part)

    # ── Import and inspect each module ────────────────────────────────────
    for module_name in module_names:
        # Prefer already-imported module from sys.modules (no re-import cost)
        module = sys.modules.get(f"{package}.{module_name}")
        if module is None:
            try:
                module = importlib.import_module(f"{package}.{module_name}")
            except ImportError:
                continue

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, BasePage) and obj is not BasePage:
                pages[name] = obj

    return pages
