from __future__ import annotations


class PageManager:
    def __init__(self, container) -> None:
        self.container = container
        self._classes: dict = {}       # Registered page classes (not yet instantiated)
        self._instances: dict = {}     # Lazily-created page instances
        self.current_page = None
        self.current_page_name: str | None = None

    def register_pages(self, page_classes: dict) -> None:
        """Register page classes for lazy instantiation on first visit."""
        self._classes.update(page_classes)

    def show(self, name: str) -> None:
        """Navigate to the named page, creating it lazily if needed."""
        # Hide the current page
        if self.current_page:
            self.current_page.pack_forget()

        # Lazy-instantiate the page on first visit
        if name not in self._instances:
            cls = self._classes.get(name)
            if cls is None:
                return
            parent = self.container.get("content_frame")
            self._instances[name] = cls(parent, self.container)

        page = self._instances[name]
        page.pack(fill="both", expand=True)
        self.current_page = page
        self.current_page_name = name

        # Fire the lifecycle hook
        if hasattr(page, "on_show"):
            page.on_show()

        app = self.container.get("app")
        app.set_status(f"{name} loaded")
        app.set_active_button(name)
