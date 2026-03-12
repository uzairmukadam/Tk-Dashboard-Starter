from __future__ import annotations
from typing import Callable, List
from tkinter import ttk
from app.config import THEMES


class ThemeManager:
    def __init__(self, root, default_theme: str = "light") -> None:
        self.root = root
        self.style = ttk.Style(root)
        self.style.theme_use("clam")
        self.current_theme = default_theme
        self._observers: List[Callable[[], None]] = []
        self.apply_theme(default_theme)

    # ── Observer registry ──────────────────────────────────────────────────
    def add_observer(self, callback: Callable[[], None]) -> None:
        """Register a zero-argument callable to be called after every theme change."""
        if callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback: Callable[[], None]) -> None:
        """Unregister a previously added observer."""
        if callback in self._observers:
            self._observers.remove(callback)

    # ── Theme application ──────────────────────────────────────────────────
    def apply_theme(self, theme_name: str) -> None:
        self.current_theme = theme_name
        colors = THEMES[theme_name]
        self._configure(colors)
        for cb in list(self._observers):
            cb()

    def toggle(self) -> None:
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)

    # ── Style configuration ────────────────────────────────────────────────
    def _configure(self, c: dict) -> None:
        s = self.style

        s.configure("TFrame",           background=c["bg"])
        s.configure("Content.TFrame",   background=c["content"])
        s.configure("Sidebar.TFrame",   background=c["sidebar"])
        s.configure("Status.TFrame",    background=c["status"])
        s.configure("Card.TFrame",      background=c["card"])

        s.configure("TLabel",
                    background=c["content"],
                    foreground=c["text"])
        s.configure("Card.TLabel",
                    background=c["card"],
                    foreground=c["text"])
        s.configure("Status.TLabel",
                    background=c["status"],
                    foreground=c["text"])
        s.configure("Sidebar.TLabel",
                    background=c["sidebar"],
                    foreground=c["sidebar_text"],
                    font=("Segoe UI", 11, "bold"))

        s.configure("Sidebar.TButton",
                    background=c["button"],
                    foreground=c["sidebar_text"],
                    borderwidth=0,
                    focuscolor=c["hover"])
        s.map("Sidebar.TButton",
              background=[("active", c["hover"])])

        s.configure("Sidebar.Active.TButton",
                    background=c["active"],
                    foreground=c["sidebar_text"],
                    borderwidth=0,
                    focuscolor=c["active"])
        s.map("Sidebar.Active.TButton",
              background=[("active", c["active"])])
