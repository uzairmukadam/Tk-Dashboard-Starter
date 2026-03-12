# Tk Dashboard Starter

A lightweight, modular **Tkinter** framework for building portable internal desktop tools.  
Zero external dependencies — ships as a single `.exe` via PyInstaller.

---

## Features

| | |
|---|---|
| 🗂️ Modular page system | Pages auto-discovered from `app/pages/` |
| ⚙️ Config-driven | App name, theme, sidebar — all in one file |
| 🌙 Light / Dark mode | Full `ttk` style theming with observer pattern |
| 🔌 Dependency Injection | `Container` wires services to every page |
| 📡 Event Bus | Pub/sub messaging between components |
| ⚡ Lazy page loading | Pages instantiated only on first visit |
| 🔔 Lifecycle hooks | `on_show()` and `on_theme_change()` on every page |
| 🗺️ Navigate menu | Menu bar auto-reflects sidebar from config |
| 📦 PyInstaller-ready | `build.py` packages to a standalone `.exe` |

---

## Quick Start

```bash
# 1. Clone
git clone <repo-url>
cd tk-dashboard-starter

# 2. Run (no pip install needed — stdlib only)
python main.py

# 3. Build executable
python build.py
```

---

## Configuration — `app/config.py`

All settings live in one file:

```python
APP_NAME    = "My Tool"       # Window title & sidebar header
APP_VERSION = "1.0.0"
COMPANY_NAME = "Your Company"

DEFAULT_THEME = "dark"        # "light" or "dark"

SIDEBAR_ITEMS = [
    {"label": "🏠 Home",       "page": "HomePage"},
    {"label": "📊 Reports",    "page": "ReportsPage"},
]

THEMES = {
    "light": { "active": "#1abc9c", ... },
    "dark":  { "active": "#0e9d7a", ... },
}
```

> Changing `SIDEBAR_ITEMS` automatically updates the sidebar **and** the Navigate menu bar.

---

## Adding a New Page

**1. Create `app/pages/reports.py`:**

```python
from tkinter import ttk
from .base_page import BasePage

class ReportsPage(BasePage):
    def __init__(self, parent, container):
        super().__init__(parent, container)
        self.build()

    def build(self):
        wrapper = ttk.Frame(self, style="Content.TFrame", padding=20)
        wrapper.pack(fill="both", expand=True)
        ttk.Label(wrapper, text="Reports").pack()

    def on_show(self):
        """Called every time this page is navigated to."""
        self._refresh()

    def on_theme_change(self):
        """Called automatically after any theme switch."""
        pass
```

**2. Register in `config.py`:**

```python
SIDEBAR_ITEMS = [
    {"label": "🏠 Home",    "page": "HomePage"},
    {"label": "📊 Reports", "page": "ReportsPage"},  # ← add this
]
```

That's it — no core changes needed.

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + Q` | Exit |
| `Ctrl + T` | Toggle light/dark theme |

---

## Project Structure

```
tk-dashboard-starter/
│
├── main.py              # Entry point
├── build.py             # PyInstaller packaging script
├── requirements.txt     # Empty — stdlib only
│
├── README.md
├── DEVELOPMENT_GUIDE.md
├── AGENTS.md
│
└── app/
    ├── config.py        # All settings
    ├── core/
    │   ├── app.py           # Main window (DashboardApp)
    │   ├── container.py     # DI container
    │   ├── event_bus.py     # Pub/sub event system
    │   ├── page_manager.py  # Navigation + lazy loading
    │   └── theme_manager.py # Light/dark themes + observers
    └── pages/
        ├── base_page.py     # Base class all pages inherit from
        ├── home.py          # Example: dashboard cards
        ├── data_table.py    # Example: sortable/searchable table
        ├── settings.py      # Example: theme toggle + info
        └── about.py         # About screen (Help menu)
```

---

## Intended Use

This template is designed for internal desktop tools that:

- Must be **portable** (single `.exe`, no install)
- Require **minimal setup** for end users
- Need a **consistent look and feel** across light/dark environments
- Are built and maintained by a small team

---

## License

Internal company usage template.
