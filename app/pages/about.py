from __future__ import annotations
from tkinter import ttk
from app.config import APP_NAME, APP_VERSION, COMPANY_NAME, FONT_HEADER, FONT_BODY, FONT_SMALL
from .base_page import BasePage


class AboutPage(BasePage):
    def __init__(self, parent, container) -> None:
        super().__init__(parent, container)
        self.build()

    def build(self) -> None:
        wrapper = ttk.Frame(self, padding=40, style="Content.TFrame")
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text=APP_NAME,            style="TLabel", font=FONT_HEADER).pack(pady=10)
        ttk.Label(wrapper, text=f"Version {APP_VERSION}", style="TLabel").pack(pady=5)

        ttk.Separator(wrapper).pack(fill="x", pady=20)

        ttk.Label(
            wrapper,
            text="Internal tool built using Tk Dashboard Starter.",
            style="TLabel",
            wraplength=500,
            justify="center",
        ).pack(pady=10)

        ttk.Label(
            wrapper,
            text=f"© 2026 {COMPANY_NAME}",
            style="TLabel",
            font=FONT_SMALL,
        ).pack(pady=20)
