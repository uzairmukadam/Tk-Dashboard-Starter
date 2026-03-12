# AGENTS.md — AI Agent Guide

This file documents the codebase for AI coding agents. Read this before making changes.

---

## Project at a Glance

| Property | Value |
|---|---|
| Language | Python 3.8+ |
| UI toolkit | `tkinter` / `ttk` (stdlib only) |
| Architecture | Service-Oriented with Dependency Injection |
| Zero dependencies | `requirements.txt` is intentionally empty |
| Entry point | `main.py` → `DashboardApp()` |
| Build | `python build.py` → `dist/` |

---

## File Map

```
main.py                         Entry point (6 lines — don't touch)
build.py                        PyInstaller packaging script
app/config.py                   ← ONLY place for app-wide settings
app/core/
  app.py         DashboardApp   Main window, layout, menu, sidebar
  container.py   Container      Service locator / DI container
  event_bus.py   EventBus       Pub/sub (subscribe / publish / unsubscribe)
  page_manager.py PageManager   Lazy page navigation + lifecycle dispatch
  theme_manager.py ThemeManager ttk style config + observer pattern
app/pages/
  base_page.py   BasePage       Base class (ttk.Frame) — all pages inherit this
  home.py        HomePage       Dashboard metric cards
  data_table.py  DataTablePage  Sortable/searchable ttk.Treeview
  settings.py    SettingsPage   Theme toggle, app info, shortcuts reference
  about.py       AboutPage      About screen (reachable from Help menu)
```

---

## The Golden Rules

1. **Never hardcode colours.** Use named `ttk` styles (`Content.TFrame`, `Card.TLabel`, etc.). Hardcoded colours break dark mode.
2. **Never touch `app/core/` for new features.** Add pages, edit `config.py` — the framework handles the rest.
3. **Every page must inherit `BasePage`.** The `__init__` auto-discovers the page and wires DI services.
4. **Use `container.get(name)`, not direct imports**, to access shared services inside pages.
5. **Config is the single source of truth.** App name, theme, sidebar items, fonts, window size — all in `app/config.py`.

---

## How to Add a Page

```python
# app/pages/my_page.py
from __future__ import annotations
from tkinter import ttk
from .base_page import BasePage

class MyPage(BasePage):
    def __init__(self, parent, container) -> None:
        super().__init__(parent, container)
        self.build()

    def build(self) -> None:
        wrapper = ttk.Frame(self, style="Content.TFrame", padding=20)
        wrapper.pack(fill="both", expand=True)
        ttk.Label(wrapper, text="My Page", style="TLabel").pack()

    def on_show(self) -> None:
        """Refresh data every time the page is navigated to."""
        pass

    def on_theme_change(self) -> None:
        """Re-render theme-sensitive widgets after a theme switch."""
        pass
```

Then add one line to `config.py`:
```python
{"label": "🔧 My Page", "page": "MyPage"},
```

---

## Service API Reference

Access via `self.container.get(key)` from any `BasePage` subclass.

### `Container`
```python
container.get("key")           # resolve service (KeyError if missing)
container.has("key") -> bool   # safe existence check
container.register("key", obj) # add a new service
```

### `EventBus`
```python
bus.subscribe("event", callback)
bus.publish("event", data=None)
bus.unsubscribe("event", callback)
bus.clear("event")             # remove all listeners
```

### `ThemeManager`
```python
tm.current_theme               # "light" or "dark"
tm.toggle()                    # switch theme
tm.apply_theme("dark")         # set explicitly
tm.add_observer(fn)            # fn() called after every apply_theme()
tm.remove_observer(fn)
```

### `PageManager`
```python
pm.show("PageName")            # navigate; creates page lazily on first call
pm.current_page_name           # str | None — name of active page
```

### `DashboardApp`
```python
app.set_status("message")      # update the status bar
app.set_active_button("Name")  # highlight sidebar button (called by PageManager)
```

---

## ttk Style Reference

All styles are configured in `ThemeManager._configure()` and update on every theme change.

| Style Name | Type | Usage |
|---|---|---|
| `Content.TFrame` | Frame | Page outer wrapper / main content bg |
| `Card.TFrame` | Frame | Elevated card / panel |
| `Sidebar.TFrame` | Frame | Sidebar container |
| `Status.TFrame` | Frame | Status bar at bottom |
| `TLabel` | Label | Text on `Content.TFrame` |
| `Card.TLabel` | Label | Text inside `Card.TFrame` |
| `Status.TLabel` | Label | Status bar text |
| `Sidebar.TLabel` | Label | Sidebar header (bold, white) |
| `Sidebar.TButton` | Button | Normal nav button |
| `Sidebar.Active.TButton` | Button | Currently active nav button (accent colour) |

---

## Theme Color Keys

Both `"light"` and `"dark"` dicts in `THEMES` must contain these keys:

| Key | Used for |
|---|---|
| `bg` | `TFrame` default background |
| `sidebar` | Sidebar frame bg |
| `content` | `Content.TFrame` bg |
| `status` | Status bar bg |
| `button` | Sidebar button bg |
| `hover` | Sidebar button hover/active bg |
| `active` | `Sidebar.Active.TButton` bg (accent) |
| `text` | Default label foreground |
| `sidebar_text` | Sidebar button/label text |
| `card` | `Card.TFrame` bg |

---

## Common Mistakes

| ❌ Wrong | ✅ Correct |
|---|---|
| `ttk.Label(..., bg="white")` | `ttk.Label(..., style="TLabel")` |
| `ttk.Label(..., style="TLabel")` inside a `Card.TFrame` | `ttk.Label(..., style="Card.TLabel")` |
| Calling `container.resolve()` before `register()` | Register all services before showing first page |
| Importing `DashboardApp` directly inside a page | Use `self.app` (already provided by `BasePage`) |
| Putting `BasePage` subclass in a file outside `app/pages/` | Pages must live in `app/pages/` for auto-discovery |

---

## Layout Rules

- **Status bar must be packed before `main_frame`** — in Tkinter, `side="bottom"` widgets must claim space before any `fill="both", expand=True` widget or they get pushed off screen.
- `self.sidebar.pack_propagate(False)` keeps the sidebar at a fixed 180 px width.
- Pages use `self.pack(fill="both", expand=True)` in `PageManager.show()` — do **not** call `.pack()` yourself inside a page's `__init__`.

---

## Build

```bash
python build.py              # single .exe → dist/
python build.py --onedir     # folder build (faster startup)
python build.py --debug      # show console (useful for tracebacks)
```

Output name comes from `APP_NAME` in `config.py`.
