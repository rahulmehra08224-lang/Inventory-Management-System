"""
================================================================================
BBAT104: ACCESSIBLE ITEM ADD / EDIT MODAL DIALOG
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
FEATURES: KEYBOARD OPERABLE, POKA-YOKE INPUT VALIDATION, HIGH CONTRAST THEMED
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from models import InventoryItem, VALID_CATEGORIES
from ui.theme import ThemeEngine


class ItemDialog:
    """Accessible modal dialog for inserting or modifying an inventory item."""

    def __init__(
        self,
        parent: tk.Tk,
        theme_engine: ThemeEngine,
        on_save: Callable[[InventoryItem], None],
        item: Optional[InventoryItem] = None
    ):
        self.parent = parent
        self.theme = theme_engine
        self.on_save = on_save
        self.item = item
        self.is_edit = item is not None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Hardware Asset" if self.is_edit else "Add New Hardware Asset")
        self.dialog.geometry("560x580")
        self.dialog.minsize(500, 520)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.entries = {}
        self.build_ui()
        self.apply_theme()
        self.bind_keys()

    def build_ui(self):
        palette = self.theme.get_palette()

        # Header Frame
        header = tk.Frame(self.dialog, pady=10, padx=16)
        header.pack(fill=tk.X)
        self.header_frame = header

        title_text = f"Edit Asset: {self.item.name}" if self.is_edit else "Add New Equipment to Catalog"
        self.lbl_title = tk.Label(header, text=title_text, font=self.theme.get_font(12, "bold"))
        self.lbl_title.pack(anchor=tk.W)

        self.lbl_sub = tk.Label(
            header,
            text="All fields marked with an asterisk (*) are required by Poka-Yoke rules.",
            font=self.theme.get_font(9)
        )
        self.lbl_sub.pack(anchor=tk.W)

        # Form Container
        self.form_frame = tk.Frame(self.dialog, padx=16, pady=8)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("SKU / Asset Code *", "sku", "entry"),
            ("Item Name *", "name", "entry"),
            ("Hardware Category *", "category", "combo"),
            ("Current Physical Stock *", "quantity", "entry"),
            ("Low Stock Alert Threshold *", "min_threshold", "entry"),
            ("Unit Price (₹ INR) *", "unit_price", "entry"),
            ("Units Issued for Lab Use", "units_issued", "entry"),
            ("Supplier / Academic Partner", "supplier", "entry"),
            ("Lab Bin / Shelf Location", "location", "entry"),
            ("Technical Specifications", "specs", "entry")
        ]

        self.labels = []
        for idx, (label_text, key, widget_type) in enumerate(fields):
            lbl = tk.Label(self.form_frame, text=label_text, font=self.theme.get_font(9, "bold"))
            lbl.grid(row=idx, column=0, sticky=tk.W, pady=3, padx=(0, 10))
            self.labels.append(lbl)

            if widget_type == "combo":
                w = ttk.Combobox(self.form_frame, values=VALID_CATEGORIES, state="readonly", width=30)
                w.set(VALID_CATEGORIES[0])
            else:
                w = tk.Entry(self.form_frame, font=self.theme.get_font(9), width=32)

            w.grid(row=idx, column=1, sticky=tk.W, pady=3)
            self.entries[key] = w

        # Error banner (hidden initially)
        self.lbl_error = tk.Label(self.form_frame, text="", font=self.theme.get_font(9, "bold"), fg=palette["danger"])
        self.lbl_error.grid(row=len(fields), column=0, columnspan=2, pady=6, sticky=tk.W)

        # Pre-populate if editing
        if self.is_edit and self.item:
            self.entries["sku"].insert(0, self.item.sku)
            self.entries["name"].insert(0, self.item.name)
            self.entries["category"].set(self.item.category)
            self.entries["quantity"].insert(0, str(self.item.quantity))
            self.entries["min_threshold"].insert(0, str(self.item.min_threshold))
            self.entries["unit_price"].insert(0, str(self.item.unit_price))
            self.entries["units_issued"].insert(0, str(self.item.units_issued))
            self.entries["supplier"].insert(0, self.item.supplier or "")
            self.entries["location"].insert(0, self.item.location or "")
            self.entries["specs"].insert(0, self.item.specs or "")

        # Action Buttons
        self.btn_frame = tk.Frame(self.dialog, padx=16, pady=12)
        self.btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.btn_save = tk.Button(
            self.btn_frame,
            text="Save Asset Details",
            command=self.submit_form,
            font=self.theme.get_font(9, "bold"),
            padx=10, pady=4
        )
        self.btn_save.pack(side=tk.RIGHT, padx=4)

        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="Cancel (Esc)",
            command=self.dialog.destroy,
            font=self.theme.get_font(9),
            padx=8, pady=4
        )
        self.btn_cancel.pack(side=tk.RIGHT, padx=4)

    def apply_theme(self):
        palette = self.theme.get_palette()
        self.dialog.config(bg=palette["bg"])
        self.header_frame.config(bg=palette["bg"])
        self.lbl_title.config(bg=palette["bg"], fg=palette["fg"])
        self.lbl_sub.config(bg=palette["bg"], fg=palette["fg_muted"])
        self.form_frame.config(bg=palette["bg"])
        self.btn_frame.config(bg=palette["surface_alt"])
        self.lbl_error.config(bg=palette["bg"], fg=palette["danger"])

        for lbl in self.labels:
            lbl.config(bg=palette["bg"], fg=palette["fg"])

        for w in self.entries.values():
            if isinstance(w, tk.Entry):
                w.config(
                    bg=palette["surface"],
                    fg=palette["fg"],
                    insertbackground=palette["fg"],
                    highlightbackground=palette["border"],
                    highlightcolor=palette["focus_ring"],
                    highlightthickness=1
                )

        self.btn_save.config(
            bg=palette["primary"],
            fg=palette["primary_fg"],
            activebackground=palette["primary_hover"],
            activeforeground=palette["primary_fg"]
        )
        self.btn_cancel.config(
            bg=palette["surface"],
            fg=palette["fg"],
            activebackground=palette["surface_alt"]
        )

    def bind_keys(self):
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        self.dialog.bind("<Return>", lambda e: self.submit_form())
        # Initial focus
        self.dialog.after(50, lambda: self.entries["sku"].focus_set())

    def submit_form(self):
        sku = self.entries["sku"].get().strip().upper()
        name = self.entries["name"].get().strip()
        category = self.entries["category"].get().strip()
        qty_str = self.entries["quantity"].get().strip()
        thresh_str = self.entries["min_threshold"].get().strip()
        price_str = self.entries["unit_price"].get().strip()
        issued_str = self.entries["units_issued"].get().strip() or "0"
        supplier = self.entries["supplier"].get().strip()
        location = self.entries["location"].get().strip()
        specs = self.entries["specs"].get().strip()

        # Parse numeric types safely
        try:
            quantity = int(qty_str)
        except ValueError:
            self.show_error("Stock Quantity must be a valid whole integer (e.g. 10).")
            self.entries["quantity"].focus_set()
            return

        try:
            min_threshold = int(thresh_str)
        except ValueError:
            self.show_error("Alert threshold must be a positive integer (e.g. 5).")
            self.entries["min_threshold"].focus_set()
            return

        try:
            unit_price = float(price_str)
        except ValueError:
            self.show_error("Unit price must be a valid number (e.g. 45000.00).")
            self.entries["unit_price"].focus_set()
            return

        try:
            units_issued = int(issued_str)
        except ValueError:
            units_issued = 0

        # Construct and validate model
        item_id = self.item.id if self.is_edit else None
        item = InventoryItem(
            sku=sku,
            name=name,
            category=category,
            quantity=quantity,
            min_threshold=min_threshold,
            unit_price=unit_price,
            units_issued=units_issued,
            supplier=supplier,
            location=location,
            specs=specs,
            item_id=item_id
        )

        is_valid, error = item.validate()
        if not is_valid:
            self.show_error(error)
            return

        try:
            self.on_save(item)
            self.dialog.destroy()
        except ValueError as e:
            self.show_error(str(e))

    def show_error(self, message: str):
        self.lbl_error.config(text=f"⚠ Error: {message}")
