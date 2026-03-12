from __future__ import annotations
import os
import sys
from typing import Dict, Optional

import tkinter as tk
from tkinter import ttk

from app.config import APP_NAME, WINDOW_SIZE, MIN_WINDOW_SIZE, DEFAULT_THEME, SIDEBAR_ITEMS, APP_ICON_PATH
from app.pages import discover_pages
from .container import Container
from .event_bus import EventBus
from .page_manager import PageManager
from .theme_manager import ThemeManager


class DashboardApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title(APP_NAME)
        self._setup_window()

        self.bind_all("<Control-q>", lambda e: self.quit())
        self.bind_all("<Control-t>", lambda e: self._toggle_theme())

        if APP_ICON_PATH:
            try:
                self.iconbitmap(self._get_resource_path(APP_ICON_PATH))
            except Exception:
                pass

        # Dependency container
        self.container = Container()
        self._sidebar_buttons: Dict[str, ttk.Button] = {}

        # Core services
        self.event_bus = EventBus()
        self.theme_manager = ThemeManager(self)

        if DEFAULT_THEME == "dark":
            self.theme_manager.apply_theme("dark")

        self._create_menu()
        self._create_layout()

        # Page Manager
        self.page_manager = PageManager(self.container)

        # Register services
        self.container.register("app", self)
        self.container.register("event_bus", self.event_bus)
        self.container.register("theme_manager", self.theme_manager)
        self.container.register("page_manager", self.page_manager)
        self.container.register("content_frame", self.content)

        # Auto-register pages
        pages = discover_pages()
        self.page_manager.register_pages(pages)

        # Sidebar nav buttons
        for item in SIDEBAR_ITEMS:
            self.add_sidebar_button(item["label"], item["page"])

        if SIDEBAR_ITEMS:
            self.page_manager.show(SIDEBAR_ITEMS[0]["page"])

    # ── Window setup ───────────────────────────────────────────────────────
    def _setup_window(self) -> None:
        """Center the window and configure minimum dimensions."""
        width, height = map(int, WINDOW_SIZE.split("x"))
        min_w, min_h = map(int, MIN_WINDOW_SIZE.split("x"))
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(min_w, min_h)

    @staticmethod
    def _get_resource_path(relative_path: str) -> str:
        """Resolve an asset path that works both in dev and PyInstaller bundles."""
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # ── Menu bar ───────────────────────────────────────────────────────────
    def _create_menu(self) -> None:
        menubar = tk.Menu(self)

        # ── File ──────────────────────────────────────────────────────────
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # ── View ──────────────────────────────────────────────────────────
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(
            label="Toggle Light/Dark Mode",
            accelerator="Ctrl+T",
            command=self._toggle_theme,
        )
        menubar.add_cascade(label="View", menu=view_menu)

        # ── Navigate ──────────────────────────────────────────────────────
        # Auto-built from SIDEBAR_ITEMS — stays in sync with config.py
        nav_menu = tk.Menu(menubar, tearoff=0)
        for item in SIDEBAR_ITEMS:
            nav_menu.add_command(
                label=item["label"],
                command=lambda p=item["page"]: self.page_manager.show(p),
            )
        menubar.add_cascade(label="Navigate", menu=nav_menu)

        # ── Help ──────────────────────────────────────────────────────────
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="Keyboard Shortcuts",
            accelerator="Ctrl+T / Ctrl+Q",
            command=lambda: self.page_manager.show("SettingsPage"),
        )
        help_menu.add_separator()
        help_menu.add_command(
            label="About",
            command=lambda: self.page_manager.show("AboutPage"),
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _toggle_theme(self) -> None:
        self.theme_manager.toggle()
        self.set_status(f"Theme switched to {self.theme_manager.current_theme}")

    # ── Layout ─────────────────────────────────────────────────────────────
    def _create_layout(self) -> None:
        # Status bar packed FIRST — must claim space before the expanding frame
        self.status_bar = ttk.Frame(self, style="Status.TFrame", height=25)
        self.status_bar.pack(side="bottom", fill="x")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # ── Sidebar ────────────────────────────────────────────────────────
        self.sidebar = ttk.Frame(self.main_frame, style="Sidebar.TFrame", width=180)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar header — app name label
        ttk.Label(
            self.sidebar,
            text=APP_NAME,
            style="Sidebar.TLabel",
            anchor="center",
        ).pack(fill="x", padx=10, pady=(16, 4))
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=(0, 8))

        # ── Content area ───────────────────────────────────────────────────
        self.content = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.content.pack(side="right", fill="both", expand=True)

        # ── Status bar contents ────────────────────────────────────────────
        self.status_label = ttk.Label(self.status_bar, text="Ready", style="Status.TLabel")
        self.status_label.pack(side="left", padx=5)

        about_btn = ttk.Button(
            self.status_bar,
            text="ℹ",
            width=2,
            command=lambda: self.page_manager.show("AboutPage"),
        )
        about_btn.pack(side="right", padx=5, pady=2)

    # ── Public API ─────────────────────────────────────────────────────────
    def set_status(self, message: str) -> None:
        """Update the status bar text."""
        self.status_label.config(text=message)

    def add_sidebar_button(self, text: str, page_name: str) -> None:
        """Create a sidebar navigation button and store a reference to it."""
        btn = ttk.Button(
            self.sidebar,
            text=text,
            style="Sidebar.TButton",
            cursor="hand2",
            command=lambda: self.page_manager.show(page_name),
        )
        btn.pack(pady=5, padx=10, fill="x")
        self._sidebar_buttons[page_name] = btn

    def set_active_button(self, page_name: str) -> None:
        """Highlight the sidebar button for *page_name* and reset all others."""
        for name, btn in self._sidebar_buttons.items():
            style = "Sidebar.Active.TButton" if name == page_name else "Sidebar.TButton"
            btn.config(style=style)
