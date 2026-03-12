import tkinter as tk
from tkinter import ttk
from app.config import FONT_HEADER, FONT_BODY, FONT_SMALL
from .base_page import BasePage


# ─── Sample data ──────────────────────────────────────────────────────────────
SAMPLE_DATA = [
    ("Alice Johnson",   "Engineering",  "Senior Engineer",  "$120,000",  "Active"),
    ("Bob Martinez",    "Marketing",    "Campaign Manager", "$85,000",   "Active"),
    ("Carol White",     "Engineering",  "Junior Engineer",  "$72,000",   "Active"),
    ("David Kim",       "HR",           "HR Specialist",    "$68,000",   "On Leave"),
    ("Eva Brown",       "Finance",      "Analyst",          "$90,000",   "Active"),
    ("Frank Turner",    "Engineering",  "Lead Architect",   "$145,000",  "Active"),
    ("Grace Lee",       "Marketing",    "SEO Specialist",   "$75,000",   "Inactive"),
    ("Henry Davis",     "Finance",      "Senior Analyst",   "$105,000",  "Active"),
    ("Iris Chen",       "HR",           "HR Manager",       "$95,000",   "Active"),
    ("Jake Wilson",     "Engineering",  "DevOps Engineer",  "$115,000",  "Active"),
]

COLUMNS = ("Name", "Department", "Role", "Salary", "Status")


class DataTablePage(BasePage):
    """Data Table page — sortable, filterable ttk.Treeview demo."""

    def __init__(self, parent, container):
        super().__init__(parent, container)
        self._sort_reverse = {col: False for col in COLUMNS}
        self._data = list(SAMPLE_DATA)
        self.build()

    def build(self):
        wrapper = ttk.Frame(self, style="Content.TFrame", padding=30)
        wrapper.pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────
        header_row = ttk.Frame(wrapper, style="Content.TFrame")
        header_row.pack(fill="x", pady=(0, 15))

        ttk.Label(header_row, text="📊  Employee Data", font=FONT_HEADER).pack(side="left")

        # Search box
        search_frame = ttk.Frame(header_row, style="Content.TFrame")
        search_frame.pack(side="right")

        ttk.Label(search_frame, text="🔍  Search:").pack(side="left", padx=(0, 5))
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search)
        ttk.Entry(search_frame, textvariable=self._search_var, width=25).pack(side="left")

        ttk.Separator(wrapper).pack(fill="x", pady=(0, 15))

        # ── Treeview ──────────────────────────────────────────────────────
        table_frame = ttk.Frame(wrapper, style="Content.TFrame")
        table_frame.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(
            table_frame,
            columns=COLUMNS,
            show="headings",
            selectmode="browse",
        )

        # Column headings — click to sort
        for col in COLUMNS:
            self._tree.heading(
                col,
                text=col,
                command=lambda c=col: self._sort_by(c),
            )
            self._tree.column(col, anchor="w", minwidth=80, width=140)

        # Adjust widths
        self._tree.column("Name", width=180)
        self._tree.column("Role", width=180)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)

        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # ── Status / row count ────────────────────────────────────────────
        self._row_count_label = ttk.Label(wrapper, text="", font=FONT_SMALL)
        self._row_count_label.pack(anchor="e", pady=(8, 0))

        # Populate with all rows initially
        self._populate(self._data)

    # ── on_show lifecycle hook ────────────────────────────────────────────
    def on_show(self):
        """Refresh the table every time this page becomes active."""
        self._populate(self._data)

    # ── Helpers ───────────────────────────────────────────────────────────
    def _populate(self, rows):
        self._tree.delete(*self._tree.get_children())
        for row in rows:
            self._tree.insert("", "end", values=row)
        count = len(rows)
        self._row_count_label.config(text=f"{count} record{'s' if count != 1 else ''} shown")

    def _sort_by(self, col):
        """Sort all rows by the given column, toggling direction on each click."""
        col_idx = COLUMNS.index(col)
        reverse = self._sort_reverse[col]
        self._sort_reverse[col] = not reverse

        sorted_data = sorted(self._data, key=lambda r: r[col_idx], reverse=reverse)
        self._populate(sorted_data)

        # Update heading arrows
        for c in COLUMNS:
            arrow = ""
            if c == col:
                arrow = " ▲" if not reverse else " ▼"
            self._tree.heading(c, text=c + arrow, command=lambda cc=c: self._sort_by(cc))

    def _on_search(self, *_):
        query = self._search_var.get().lower().strip()
        if not query:
            self._populate(self._data)
            return
        filtered = [row for row in self._data if any(query in str(cell).lower() for cell in row)]
        self._populate(filtered)
