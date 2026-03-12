from __future__ import annotations
from tkinter import ttk


class BasePage(ttk.Frame):
    def __init__(self, parent, container) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.container = container
        self.event_bus = container.get("event_bus")
        self.page_manager = container.get("page_manager")
        self.app = container.get("app")

        # Register as a theme observer so on_theme_change() is called automatically
        tm = container.get("theme_manager")
        tm.add_observer(self.on_theme_change)

    def on_show(self) -> None:
        """Lifecycle hook called every time this page becomes the active view.

        Override in subclasses to refresh data, reset scroll positions, etc.
        The default implementation does nothing.
        """
        pass

    def on_theme_change(self) -> None:
        """Lifecycle hook called after the theme changes.

        Override in subclasses to re-apply any widget colours or images that
        cannot be updated by ttk styles alone.
        The default implementation does nothing.
        """
        pass
