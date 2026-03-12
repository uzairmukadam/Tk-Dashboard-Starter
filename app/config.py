APP_NAME = "Internal Tool"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Your Company"

WINDOW_SIZE = "1000x600"
MIN_WINDOW_SIZE = "800x600"
DEFAULT_THEME = "light"

APP_ICON_PATH = "app/assets/app.ico"

SIDEBAR_ITEMS = [
    {"label": "🏠 Home",         "page": "HomePage"},
    {"label": "📊 Data Table",   "page": "DataTablePage"},
    {"label": "⚙️  Settings",    "page": "SettingsPage"},
]

# Fonts
FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_SUBHEADER = ("Segoe UI", 14)
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

THEMES = {
    "light": {
        "bg": "#f5f5f5",
        "sidebar": "#2c3e50",
        "content": "#ecf0f1",
        "status": "#bdc3c7",
        "button": "#34495e",
        "hover": "#3d566e",
        "active": "#1abc9c",
        "text": "#000000",
        "sidebar_text": "#ffffff",
        "card": "#ffffff",
    },
    "dark": {
        "bg": "#1e1e1e",
        "sidebar": "#252526",
        "content": "#2d2d30",
        "status": "#3c3c3c",
        "button": "#3a3d41",
        "hover": "#505357",
        "active": "#0e9d7a",
        "text": "#ffffff",
        "sidebar_text": "#ffffff",
        "card": "#3a3d41",
    }
}
