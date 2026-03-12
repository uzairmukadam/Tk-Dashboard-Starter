# 📘 Development Guide

> **Python 3.8+ required.** No external dependencies — stdlib only.

---

## 1. Architecture

The app is split into three layers:

```
app/
├── config.py          ← All settings (single source of truth)
├── core/              ← Framework engine (never edit for new features)
│   ├── app.py         ← Main window, layout, sidebar, menu
│   ├── container.py   ← Dependency injection container
│   ├── event_bus.py   ← Pub/sub event system
│   ├── page_manager.py← Navigation + lazy page instantiation
│   └── theme_manager.py← Light/dark theming + observer pattern
└── pages/             ← UI screens (add yours here)
    ├── base_page.py   ← Base class; all pages must inherit this
    ├── home.py
    ├── data_table.py
    ├── settings.py
    └── about.py
```

**Data flow on navigation:**
```
Sidebar button click
  → PageManager.show("PageName")
  → page.pack()               # show frame
  → page.on_show()            # lifecycle hook
  → app.set_active_button()   # highlight sidebar
  → app.set_status()          # update status bar
```

---

## 2. Creating a New Page

### Step 1 — Create the file

```python
# app/pages/reports.py
from __future__ import annotations
from tkinter import ttk
from .base_page import BasePage


class ReportsPage(BasePage):
    def __init__(self, parent, container) -> None:
        super().__init__(parent, container)
        self.build()

    def build(self) -> None:
        wrapper = ttk.Frame(self, style="Content.TFrame", padding=20)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="Reports", style="TLabel").pack()

    # ── Lifecycle hooks (optional) ─────────────────────────────────────
    def on_show(self) -> None:
        """Called every time this page becomes visible."""
        self._load_data()

    def on_theme_change(self) -> None:
        """Called automatically after any theme switch (Ctrl+T or code)."""
        pass          # re-draw canvas, update images, etc.
```

### Step 2 — Register in `config.py`

```python
SIDEBAR_ITEMS = [
    {"label": "🏠 Home",      "page": "HomePage"},
    {"label": "📊 Reports",   "page": "ReportsPage"},  # ← add this
]
```

That's it. No changes to `core/` required.

---

## 3. Theming & Styles

**Rule:** Never hardcode colours (`bg="white"`). Use named `ttk` styles so the app renders correctly in both themes.

| Style | Used on | Notes |
|---|---|---|
| `Content.TFrame` | Page outer wrapper | Main content background |
| `Card.TFrame` | Panel / card containers | Stands out from the background |
| `TLabel` | Text on `Content.TFrame` | Theme-aware text colour |
| `Card.TLabel` | Text inside `Card.TFrame` | **Required** for dark mode correctness |
| `Status.TLabel` | Status bar text | |
| `Sidebar.TLabel` | Sidebar header text | Bold, white |
| `Sidebar.TButton` | Sidebar nav buttons | |
| `Sidebar.Active.TButton` | Currently-active nav button | Accent colour |

### Example — Card

```python
card = ttk.Frame(parent, style="Card.TFrame", padding=15)
card.pack(fill="x", pady=10)

ttk.Label(card, text="Title", style="Card.TLabel").pack(anchor="w")
ttk.Label(card, text="Body text", style="Card.TLabel").pack(anchor="w")
```

### Adding a Custom Colour

Add your key to both theme dicts in `config.py`, then reference `c["my_key"]` inside `ThemeManager._configure()`.

---

## 4. Services (Dependency Injection)

Every page has `self.container`. Use it to access framework services:

```python
# In any page method:
bus   = self.container.get("event_bus")
theme = self.container.get("theme_manager")
pm    = self.container.get("page_manager")

# Guard against optional services:
if self.container.has("my_service"):
    svc = self.container.get("my_service")
```

### Available Services

| Key | Type | Description |
|---|---|---|
| `"app"` | `DashboardApp` | Main window; `set_status()`, `set_active_button()` |
| `"event_bus"` | `EventBus` | Pub/sub messaging |
| `"theme_manager"` | `ThemeManager` | Theme state + observer API |
| `"page_manager"` | `PageManager` | `show(name)`, `current_page_name` |
| `"content_frame"` | `ttk.Frame` | The main content area |

### Registering Your Own Service

```python
# In DashboardApp.__init__() in app.py:
from myapp.services.database import Database
db = Database("myapp.db")
self.container.register("database", db)
```

---

## 5. Page Lifecycle Hooks

`BasePage` provides two hooks:

| Hook | When called |
|---|---|
| `on_show()` | Every time the page becomes the active view |
| `on_theme_change()` | Immediately after any theme change |

Both are registered automatically — you only need to override them.

```python
def on_show(self) -> None:
    self._refresh_table()   # reload data on every visit

def on_theme_change(self) -> None:
    self._canvas.config(bg=...)  # re-draw theme-dependent canvas
```

---

## 6. EventBus

Use `EventBus` for decoupled communication (e.g. service → page):

```python
bus = self.container.get("event_bus")

# Subscribe
bus.subscribe("data_ready", self._on_data_ready)

# Publish (from anywhere)
bus.publish("data_ready", {"rows": data})

# Clean up (call if your page widget is destroyed)
bus.unsubscribe("data_ready", self._on_data_ready)
```

---

## 7. ThemeManager Observers

If you need to react to theme changes from outside a page:

```python
tm = self.container.get("theme_manager")
tm.add_observer(my_callback)   # called after every apply_theme()
tm.remove_observer(my_callback)
```

> `BasePage.__init__` already calls `add_observer(self.on_theme_change)` automatically.

---

## 8. Building for Distribution

```bash
python build.py          # → dist/Internal_Tool.exe
python build.py --onedir # → dist/Internal_Tool/  (folder, faster startup)
python build.py --debug  # keeps console window for traceback inspection
```

`build.py` reads `APP_NAME` and `APP_VERSION` from `config.py` automatically.