from __future__ import annotations
from tkinter import ttk
from app.config import FONT_HEADER, FONT_SUBHEADER, FONT_BODY
from .base_page import BasePage


# Metric cards: (title, value, sub-label, colour-tag)
_METRICS = [
    ("👥 Users",    "1,500",   "+12% this month"),
    ("💰 Revenue",  "$12,300", "+8% this month"),
    ("📦 Orders",   "320",     "+5% this month"),
]


class HomePage(BasePage):
    def __init__(self, parent, container) -> None:
        super().__init__(parent, container)
        self.build()

    def build(self) -> None:
        wrapper = ttk.Frame(self, style="Content.TFrame", padding=(30, 20))
        wrapper.pack(fill="both", expand=True)

        # ── Page header ───────────────────────────────────────────────────
        ttk.Label(wrapper, text="🏠  Dashboard", font=FONT_HEADER).pack(anchor="w")
        ttk.Label(
            wrapper,
            text="Welcome back. Here's what's happening today.",
            font=FONT_BODY,
        ).pack(anchor="w", pady=(2, 20))
        ttk.Separator(wrapper).pack(fill="x", pady=(0, 20))

        # ── Metric cards row ──────────────────────────────────────────────
        cards_row = ttk.Frame(wrapper, style="Content.TFrame")
        cards_row.pack(fill="x")

        for title, value, sublabel in _METRICS:
            card = ttk.Frame(cards_row, style="Card.TFrame", padding=20)
            card.pack(side="left", padx=(0, 15), ipadx=5)

            ttk.Label(card, text=title,    style="Card.TLabel", font=FONT_BODY).pack(anchor="w")
            ttk.Label(card, text=value,    style="Card.TLabel", font=FONT_SUBHEADER).pack(anchor="w", pady=(4, 2))
            ttk.Label(card, text=sublabel, style="Card.TLabel", font=("Segoe UI", 8)).pack(anchor="w")
