from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from app.config import APP_NAME, APP_VERSION, COMPANY_NAME, FONT_HEADER, FONT_SUBHEADER, FONT_BODY, FONT_SMALL
from .base_page import BasePage


class SettingsPage(BasePage):
    """Settings page — theme toggling, config display, keyboard shortcuts."""

    def __init__(self, parent, container) -> None:
        super().__init__(parent, container)
        self._theme_btn: ttk.Button | None = None
        self._theme_indicator: ttk.Label | None = None
        self.build()

    def build(self) -> None:
        wrapper = ttk.Frame(self, style="Content.TFrame", padding=30)
        wrapper.pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────
        ttk.Label(wrapper, text="⚙️  Settings", font=FONT_HEADER).pack(anchor="w", pady=(0, 20))
        ttk.Separator(wrapper).pack(fill="x", pady=(0, 20))

        # ── Appearance card ───────────────────────────────────────────────
        appearance_card = ttk.Frame(wrapper, style="Card.TFrame", padding=20)
        appearance_card.pack(fill="x", pady=(0, 15))

        ttk.Label(appearance_card, text="Appearance", font=FONT_SUBHEADER, style="Card.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        btn_row = ttk.Frame(appearance_card, style="Card.TFrame")
        btn_row.pack(anchor="w")

        ttk.Label(btn_row, text="Theme:", style="Card.TLabel").pack(side="left", padx=(0, 10))

        self._theme_btn = ttk.Button(btn_row, command=self._toggle_theme)
        self._theme_btn.pack(side="left")

        self._theme_indicator = ttk.Label(btn_row, font=FONT_SMALL, style="Card.TLabel")
        self._theme_indicator.pack(side="left", padx=10)

        # ── App info card ─────────────────────────────────────────────────
        info_card = ttk.Frame(wrapper, style="Card.TFrame", padding=20)
        info_card.pack(fill="x", pady=(0, 15))

        ttk.Label(info_card, text="Application Info", font=FONT_SUBHEADER, style="Card.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        for label, value in [("App Name", APP_NAME), ("Version", APP_VERSION), ("Company", COMPANY_NAME)]:
            row = ttk.Frame(info_card, style="Card.TFrame")
            row.pack(fill="x", pady=3)
            ttk.Label(row, text=f"{label}:", width=14, style="Card.TLabel", font=FONT_BODY).pack(side="left")
            ttk.Label(row, text=value, style="Card.TLabel").pack(side="left")

        # ── Keyboard shortcuts card ───────────────────────────────────────
        shortcuts_card = ttk.Frame(wrapper, style="Card.TFrame", padding=20)
        shortcuts_card.pack(fill="x", pady=(0, 15))

        ttk.Label(shortcuts_card, text="Keyboard Shortcuts", font=FONT_SUBHEADER, style="Card.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        for key, desc in [("Ctrl + Q", "Exit the application"), ("Ctrl + T", "Toggle light / dark theme")]:
            row = ttk.Frame(shortcuts_card, style="Card.TFrame")
            row.pack(fill="x", pady=3)
            ttk.Label(row, text=key,  width=14, font=("Courier New", 9, "bold"), style="Card.TLabel").pack(side="left")
            ttk.Label(row, text=desc, style="Card.TLabel").pack(side="left")

        # Set initial text now that widgets exist
        self._refresh_theme_ui()

    # ── Lifecycle hooks ────────────────────────────────────────────────────
    def on_show(self) -> None:
        """Keep button text and indicator fresh each time the page is shown."""
        self._refresh_theme_ui()

    def on_theme_change(self) -> None:
        """Keep button text in sync even when theme is changed via Ctrl+T."""
        self._refresh_theme_ui()

    # ── Helpers ────────────────────────────────────────────────────────────
    def _refresh_theme_ui(self) -> None:
        """Update the theme button label and indicator text to match current theme."""
        if self._theme_btn is None:
            return
        theme = self.container.get("theme_manager").current_theme
        if theme == "light":
            self._theme_btn.config(text="🌙  Switch to Dark")
        else:
            self._theme_btn.config(text="☀️  Switch to Light")
        if self._theme_indicator is not None:
            self._theme_indicator.config(text=f"(currently: {theme})")

    def _toggle_theme(self) -> None:
        tm = self.container.get("theme_manager")
        tm.toggle()
        self.app.set_status(f"Theme switched to {tm.current_theme}")
