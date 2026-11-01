"""
================================================================================
BBAT104: MAIN INVENTORY MANAGEMENT APPLICATION WINDOW
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
BASELINE: INVENTORY MANAGEMENT SYSTEM (DIGIT 3)
QUALITY GOAL: Q12 IMPROVE ACCESSIBILITY (5 FEATURES INTEGRATED)
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from database import Database
from models import InventoryItem, VALID_CATEGORIES
from ui.theme import ThemeEngine
from ui.item_dialog import ItemDialog
from ui.tqm_views import TqmAuditWindow


class InventoryAppWindow:
    """Main Application GUI coordinating accessibility features, CRUD, and TQM tools."""

    def __init__(self, root: tk.Tk, db: Database):
        self.root = root
        self.db = db
        self.theme = ThemeEngine()

        self.root.title("CSE AIML Hardware Inventory Management System | Q12 Accessibility Suite - Rahul Mehra")
        self.root.geometry("1260x800")
        self.root.minsize(980, 640)

        # Reactive search and filter state
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="ALL")
        self.status_var = tk.StringVar(value="ALL")
        self.sort_var = tk.StringVar(value="name-asc")

        self.build_ui()
        self.bind_keyboard_shortcuts()
        self.apply_theme()
        self.refresh_table()

    def build_ui(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # 1. TOP PERSISTENT ACCESSIBILITY TOOLBAR
        # -------------------------------------------------------------
        self.a11y_toolbar = tk.Frame(self.main_container, pady=6, padx=14, relief=tk.RAISED, bd=1)
        self.a11y_toolbar.pack(fill=tk.X, side=tk.TOP)

        self.lbl_student = tk.Label(
            self.a11y_toolbar,
            text="Student: Rahul Mehra | CSE AIML (Sec B) | Q12: Accessibility Suite",
            font=self.theme.get_font(9, "bold")
        )
        self.lbl_student.pack(side=tk.LEFT, padx=4)

        # Right-aligned A11y & TQM Controls
        self.btn_tqm = tk.Button(
            self.a11y_toolbar,
            text="📊 TQM & SQC Audit",
            command=self.open_tqm_audit,
            font=self.theme.get_font(9, "bold")
        )
        self.btn_tqm.pack(side=tk.RIGHT, padx=4)

        self.btn_shortcuts = tk.Button(
            self.a11y_toolbar,
            text="⌨ Shortcuts (?)",
            command=self.show_shortcuts_dialog,
            font=self.theme.get_font(9, "bold")
        )
        self.btn_shortcuts.pack(side=tk.RIGHT, padx=4)

        self.btn_minimalist = tk.Button(
            self.a11y_toolbar,
            text="Minimalist (Alt+M)",
            command=self.toggle_minimalist,
            font=self.theme.get_font(9)
        )
        self.btn_minimalist.pack(side=tk.RIGHT, padx=4)

        self.btn_theme = tk.Button(
            self.a11y_toolbar,
            text="Dark Mode (Alt+D)",
            command=self.toggle_theme,
            font=self.theme.get_font(9)
        )
        self.btn_theme.pack(side=tk.RIGHT, padx=4)

        self.btn_contrast = tk.Button(
            self.a11y_toolbar,
            text="High Contrast (Alt+H)",
            command=self.toggle_contrast,
            font=self.theme.get_font(9, "bold")
        )
        self.btn_contrast.pack(side=tk.RIGHT, padx=4)

        # Font Resizing Controls
        self.btn_font_plus = tk.Button(
            self.a11y_toolbar,
            text="A+ (Alt++)",
            command=lambda: self.adjust_font(1),
            font=self.theme.get_font(9, "bold")
        )
        self.btn_font_plus.pack(side=tk.RIGHT, padx=2)

        self.lbl_font_scale = tk.Label(
            self.a11y_toolbar,
            text="100%",
            font=self.theme.get_font(9, "bold"),
            width=5
        )
        self.lbl_font_scale.pack(side=tk.RIGHT, padx=2)

        self.btn_font_minus = tk.Button(
            self.a11y_toolbar,
            text="A- (Alt+-)",
            command=lambda: self.adjust_font(-1),
            font=self.theme.get_font(9, "bold")
        )
        self.btn_font_minus.pack(side=tk.RIGHT, padx=2)

        # -------------------------------------------------------------
        # 2. BRANDING & GLOBAL ACTIONS HEADER
        # -------------------------------------------------------------
        self.header_frame = tk.Frame(self.main_container, pady=10, padx=16)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        header_left = tk.Frame(self.header_frame)
        header_left.pack(side=tk.LEFT)

        self.lbl_title = tk.Label(
            header_left,
            text="CSE AIML Hardware & Inventory System",
            font=self.theme.get_font(16, "bold")
        )
        self.lbl_title.pack(anchor=tk.W)

        self.lbl_subtitle = tk.Label(
            header_left,
            text="Automated Stockout Elimination, Turnover Tracking & Accessible Asset Registry",
            font=self.theme.get_font(9)
        )
        self.lbl_subtitle.pack(anchor=tk.W)

        header_right = tk.Frame(self.header_frame)
        header_right.pack(side=tk.RIGHT)

        self.btn_add = tk.Button(
            header_right,
            text="+ Add New Item (Alt+N)",
            command=self.open_add_dialog,
            font=self.theme.get_font(10, "bold"),
            padx=10, pady=5
        )
        self.btn_add.pack(side=tk.LEFT, padx=4)

        self.btn_export_csv = tk.Button(
            header_right,
            text="Export CSV (Alt+E)",
            command=self.export_csv,
            font=self.theme.get_font(10),
            padx=8, pady=5
        )
        self.btn_export_csv.pack(side=tk.LEFT, padx=4)

        self.btn_export_json = tk.Button(
            header_right,
            text="Export JSON",
            command=self.export_json,
            font=self.theme.get_font(10),
            padx=8, pady=5
        )
        self.btn_export_json.pack(side=tk.LEFT, padx=4)

        self.btn_reset_data = tk.Button(
            header_right,
            text="Reset Demo Data",
            command=self.reset_demo_data,
            font=self.theme.get_font(10),
            padx=8, pady=5
        )
        self.btn_reset_data.pack(side=tk.LEFT, padx=4)

        # -------------------------------------------------------------
        # 3. METRICS DASHBOARD CARDS (Dynamically hidden in Minimalist mode)
        # -------------------------------------------------------------
        self.metrics_frame = tk.Frame(self.main_container, pady=6, padx=16)
        self.metrics_frame.pack(fill=tk.X, side=tk.TOP)

        self.card_skus = self._create_card(self.metrics_frame, "TOTAL UNIQUE SKUs", "0", "Catalog components")
        self.card_units = self._create_card(self.metrics_frame, "TOTAL HARDWARE UNITS", "0", "Physical items in lab")
        self.card_val = self._create_card(self.metrics_frame, "INVENTORY VALUATION", "₹0.00", "Total asset capital")
        self.card_low = self._create_card(self.metrics_frame, "LOW / ZERO STOCK", "0", "Need reorder (Q <= ROP)", is_alert=True)
        self.card_turnover = self._create_card(self.metrics_frame, "AVG TURNOVER RATIO", "0.0x", "Annual capital velocity")

        # -------------------------------------------------------------
        # 4. SEARCH & FILTER CONTROLS TOOLBAR
        # -------------------------------------------------------------
        self.filter_frame = tk.Frame(self.main_container, pady=8, padx=16)
        self.filter_frame.pack(fill=tk.X, side=tk.TOP)

        tk.Label(self.filter_frame, text="Search (Alt+S):", font=self.theme.get_font(9, "bold")).pack(side=tk.LEFT, padx=(0, 4))
        self.entry_search = tk.Entry(self.filter_frame, textvariable=self.search_var, font=self.theme.get_font(9), width=24)
        self.entry_search.pack(side=tk.LEFT, padx=(0, 12))
        self.search_var.trace_add("write", lambda *args: self.refresh_table())

        tk.Label(self.filter_frame, text="Category:", font=self.theme.get_font(9, "bold")).pack(side=tk.LEFT, padx=(6, 4))
        self.cb_category = ttk.Combobox(
            self.filter_frame,
            textvariable=self.category_var,
            values=["ALL"] + VALID_CATEGORIES,
            state="readonly",
            width=17
        )
        self.cb_category.pack(side=tk.LEFT, padx=(0, 12))
        self.cb_category.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        tk.Label(self.filter_frame, text="Stock Status:", font=self.theme.get_font(9, "bold")).pack(side=tk.LEFT, padx=(6, 4))
        self.cb_status = ttk.Combobox(
            self.filter_frame,
            textvariable=self.status_var,
            values=["ALL", "IN_STOCK", "LOW_STOCK", "OUT_OF_STOCK"],
            state="readonly",
            width=14
        )
        self.cb_status.pack(side=tk.LEFT, padx=(0, 12))
        self.cb_status.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        tk.Label(self.filter_frame, text="Sort By:", font=self.theme.get_font(9, "bold")).pack(side=tk.LEFT, padx=(6, 4))
        self.cb_sort = ttk.Combobox(
            self.filter_frame,
            textvariable=self.sort_var,
            values=["name-asc", "name-desc", "qty-asc", "qty-desc", "price-asc", "price-desc", "date-desc"],
            state="readonly",
            width=12
        )
        self.cb_sort.pack(side=tk.LEFT, padx=(0, 12))
        self.cb_sort.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        self.btn_reset_filters = tk.Button(
            self.filter_frame,
            text="Reset Filters",
            command=self.reset_filters,
            font=self.theme.get_font(9)
        )
        self.btn_reset_filters.pack(side=tk.LEFT, padx=4)

        self.lbl_table_count = tk.Label(self.filter_frame, text="Showing 0 items", font=self.theme.get_font(9, "italic"))
        self.lbl_table_count.pack(side=tk.RIGHT)

        # -------------------------------------------------------------
        # 5. DATA TABLE (TREEVIEW WITH KEYBOARD NAVIGATION)
        # -------------------------------------------------------------
        self.table_frame = tk.Frame(self.main_container, padx=16, pady=4)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "sku", "name", "category", "qty", "threshold", "price", "turnover", "status", "supplier")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="# ID")
        self.tree.heading("sku", text="SKU Code")
        self.tree.heading("name", text="Item Name & Specification")
        self.tree.heading("category", text="Category")
        self.tree.heading("qty", text="Stock Units")
        self.tree.heading("threshold", text="Min Alert")
        self.tree.heading("price", text="Unit Price (₹)")
        self.tree.heading("turnover", text="Turnover (FSN)")
        self.tree.heading("status", text="Stock Status")
        self.tree.heading("supplier", text="Supplier / Location")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("sku", width=125, anchor=tk.W)
        self.tree.column("name", width=280, anchor=tk.W)
        self.tree.column("category", width=130, anchor=tk.W)
        self.tree.column("qty", width=80, anchor=tk.CENTER)
        self.tree.column("threshold", width=75, anchor=tk.CENTER)
        self.tree.column("price", width=100, anchor=tk.E)
        self.tree.column("turnover", width=110, anchor=tk.CENTER)
        self.tree.column("status", width=125, anchor=tk.CENTER)
        self.tree.column("supplier", width=160, anchor=tk.W)

        scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind row interaction
        self.tree.bind("<Double-1>", lambda e: self.edit_selected_item())
        self.tree.bind("<Return>", lambda e: self.edit_selected_item())

        # -------------------------------------------------------------
        # 6. ROW ACTIONS BAR & STATUS FEEDBACK
        # -------------------------------------------------------------
        self.actions_bar = tk.Frame(self.main_container, pady=6, padx=16)
        self.actions_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.btn_stock_minus = tk.Button(
            self.actions_bar,
            text="- Decrement Stock",
            command=lambda: self.adjust_selected_stock(-1),
            font=self.theme.get_font(9, "bold"),
            padx=8, pady=3
        )
        self.btn_stock_minus.pack(side=tk.LEFT, padx=3)

        self.btn_stock_plus = tk.Button(
            self.actions_bar,
            text="+ Increment Stock",
            command=lambda: self.adjust_selected_stock(1),
            font=self.theme.get_font(9, "bold"),
            padx=8, pady=3
        )
        self.btn_stock_plus.pack(side=tk.LEFT, padx=3)

        self.btn_edit = tk.Button(
            self.actions_bar,
            text="Edit Asset (Enter)",
            command=self.edit_selected_item,
            font=self.theme.get_font(9),
            padx=8, pady=3
        )
        self.btn_edit.pack(side=tk.LEFT, padx=6)

        self.btn_delete = tk.Button(
            self.actions_bar,
            text="Delete Asset (Del)",
            command=self.delete_selected_item,
            font=self.theme.get_font(9),
            padx=8, pady=3
        )
        self.btn_delete.pack(side=tk.LEFT, padx=3)

        self.lbl_status_msg = tk.Label(
            self.actions_bar,
            text="Ready. Use Up/Down arrows to navigate rows. Press ? for Shortcuts.",
            font=self.theme.get_font(9, "italic")
        )
        self.lbl_status_msg.pack(side=tk.RIGHT)

    def _create_card(self, parent, label_text, default_val, subtext, is_alert=False):
        palette = self.theme.get_palette()
        card = tk.Frame(parent, relief=tk.GROOVE, bd=palette["card_bd"], padx=10, pady=8)
        card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

        lbl = tk.Label(card, text=label_text, font=self.theme.get_font(8, "bold"))
        lbl.pack(anchor=tk.W)

        val = tk.Label(card, text=default_val, font=self.theme.get_font(13, "bold"))
        val.pack(anchor=tk.W)

        sub = tk.Label(card, text=subtext, font=self.theme.get_font(8))
        sub.pack(anchor=tk.W)

        card.val_widget = val
        card.sub_widget = sub
        card.lbl_widget = lbl
        card.is_alert = is_alert
        return card

    # -----------------------------------------------------------------
    # ACCESSIBILITY CONTROLLER METHODS
    # -----------------------------------------------------------------
    def adjust_font(self, direction: int):
        new_scale = self.theme.step_font_scale(direction)
        percent_str = f"{int(new_scale * 100)}%"
        self.lbl_font_scale.config(text=percent_str)
        self.apply_theme()
        self.set_status(f"Font scale adjusted to {percent_str}.")

    def toggle_theme(self):
        is_dark = self.theme.toggle_theme()
        self.btn_theme.config(text="Light Mode" if is_dark else "Dark Mode")
        self.apply_theme()
        self.set_status(f"Switched to {'Dark' if is_dark else 'Light'} theme.")

    def toggle_contrast(self):
        is_high = self.theme.toggle_contrast()
        self.btn_contrast.config(text="Normal Contrast" if is_high else "High Contrast")
        self.apply_theme()
        self.set_status(f"High Contrast mode {'enabled (WCAG AAA)' if is_high else 'restored to standard'}.")

    def toggle_minimalist(self):
        is_minimal = self.theme.toggle_minimalist()
        self.btn_minimalist.config(text="Full View" if is_minimal else "Minimalist View")
        if is_minimal:
            self.metrics_frame.pack_forget()
            self.lbl_subtitle.pack_forget()
            self.set_status("Minimalist Layout enabled: Cognitive clutter and decorative elements hidden.")
        else:
            self.metrics_frame.pack(fill=tk.X, side=tk.TOP, after=self.header_frame)
            self.lbl_subtitle.pack(anchor=tk.W)
            self.set_status("Standard Full View restored.")

    def apply_theme(self):
        palette = self.theme.get_palette()
        self.root.config(bg=palette["bg"])
        self.main_container.config(bg=palette["bg"])
        self.a11y_toolbar.config(bg=palette["surface_alt"], bd=palette["card_bd"])
        self.lbl_student.config(bg=palette["surface_alt"], fg=palette["fg"])
        self.lbl_font_scale.config(bg=palette["surface_alt"], fg=palette["fg"])
        self.header_frame.config(bg=palette["bg"])
        self.lbl_title.config(bg=palette["bg"], fg=palette["fg"], font=self.theme.get_font(16, "bold"))
        self.lbl_subtitle.config(bg=palette["bg"], fg=palette["fg_muted"], font=self.theme.get_font(9))
        self.metrics_frame.config(bg=palette["bg"])
        self.filter_frame.config(bg=palette["surface_alt"])
        self.table_frame.config(bg=palette["bg"])
        self.actions_bar.config(bg=palette["surface_alt"])
        self.lbl_status_msg.config(bg=palette["surface_alt"], fg=palette["fg_muted"])
        self.lbl_table_count.config(bg=palette["surface_alt"], fg=palette["fg_muted"])

        # Metric cards
        for card in [self.card_skus, self.card_units, self.card_val, self.card_low, self.card_turnover]:
            card.config(bg=palette["surface"], bd=palette["card_bd"])
            card.lbl_widget.config(bg=palette["surface"], fg=palette["fg_muted"], font=self.theme.get_font(8, "bold"))
            card_val_fg = palette["danger"] if card.is_alert and self.theme.high_contrast else palette["fg"]
            card.val_widget.config(bg=palette["surface"], fg=card_val_fg, font=self.theme.get_font(13, "bold"))
            card.sub_widget.config(bg=palette["surface"], fg=palette["fg_muted"], font=self.theme.get_font(8))

        # Buttons
        self.btn_add.config(bg=palette["primary"], fg=palette["primary_fg"])
        self.btn_export_csv.config(bg=palette["surface"], fg=palette["fg"])
        self.btn_export_json.config(bg=palette["surface"], fg=palette["fg"])
        self.btn_reset_data.config(bg=palette["surface"], fg=palette["fg"])

        # Treeview Styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=palette["surface"],
            foreground=palette["fg"],
            fieldbackground=palette["surface"],
            rowheight=int(26 * self.theme.font_scale),
            font=self.theme.get_font(9)
        )
        style.configure(
            "Treeview.Heading",
            background=palette["surface_alt"],
            foreground=palette["fg"],
            font=self.theme.get_font(9, "bold")
        )
        style.map("Treeview", background=[("selected", palette["select_bg"])], foreground=[("selected", palette["select_fg"])])

    def bind_keyboard_shortcuts(self):
        self.root.bind("<Alt-n>", lambda e: self.open_add_dialog())
        self.root.bind("<Alt-s>", lambda e: self.entry_search.focus_set())
        self.root.bind("<Alt-h>", lambda e: self.toggle_contrast())
        self.root.bind("<Alt-d>", lambda e: self.toggle_theme())
        self.root.bind("<Alt-m>", lambda e: self.toggle_minimalist())
        self.root.bind("<Alt-plus>", lambda e: self.adjust_font(1))
        self.root.bind("<Alt-equal>", lambda e: self.adjust_font(1))
        self.root.bind("<Alt-minus>", lambda e: self.adjust_font(-1))
        self.root.bind("<Alt-0>", lambda e: self.reset_font())
        self.root.bind("<Alt-e>", lambda e: self.export_csv())
        self.root.bind("<Delete>", lambda e: self.delete_selected_item())
        self.root.bind("<question>", lambda e: self.show_shortcuts_dialog())

    def reset_font(self):
        scale = self.theme.reset_font_scale()
        self.lbl_font_scale.config(text=f"{int(scale * 100)}%")
        self.apply_theme()
        self.set_status("Font size reset to 100% default.")

    def set_status(self, msg: str):
        self.lbl_status_msg.config(text=msg)

    # -----------------------------------------------------------------
    # CRUD & DATA WORKFLOWS
    # -----------------------------------------------------------------
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        items = self.db.get_all_items(
            search_query=self.search_var.get(),
            category=self.category_var.get(),
            status=self.status_var.get(),
            sort_by=self.sort_var.get()
        )

        metrics = self.db.get_metrics()
        self.card_skus.val_widget.config(text=str(metrics.total_skus))
        self.card_units.val_widget.config(text=str(metrics.total_units))
        self.card_val.val_widget.config(text=f"₹{metrics.total_valuation:,.2f}")
        self.card_low.val_widget.config(text=str(metrics.low_stock_count + metrics.out_of_stock_count))
        self.card_turnover.val_widget.config(text=f"{metrics.avg_turnover:.1f}x (Annual)")

        self.lbl_table_count.config(text=f"Showing {len(items)} of {metrics.total_skus} items")

        for it in items:
            status_code, label, sym = it.get_stock_status()
            turnover_str = f"{it.get_turnover_ratio()}x ({it.get_fsn_classification()})"
            display_status = f"{sym} {label}"

            self.tree.insert("", tk.END, values=(
                it.id,
                it.sku,
                it.name,
                it.category,
                it.quantity,
                it.min_threshold,
                f"₹{it.unit_price:,.2f}",
                turnover_str,
                display_status,
                it.supplier or "N/A"
            ))

    def reset_filters(self):
        self.search_var.set("")
        self.category_var.set("ALL")
        self.status_var.set("ALL")
        self.sort_var.set("name-asc")
        self.refresh_table()
        self.set_status("All search queries and category filters reset.")

    def open_add_dialog(self):
        def on_save(new_item: InventoryItem):
            self.db.add_item(new_item)
            self.refresh_table()
            self.set_status(f"Added item '{new_item.name}' ({new_item.sku}).")

        ItemDialog(self.root, self.theme, on_save, item=None)

    def edit_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select an inventory item row to edit.")
            return

        item_id = self.tree.item(selected[0])["values"][0]
        item = self.db.get_item(item_id)
        if not item:
            messagebox.showerror("Error", "Selected item was not found in database.")
            return

        def on_save(updated_item: InventoryItem):
            self.db.update_item(updated_item)
            self.refresh_table()
            self.set_status(f"Successfully updated '{updated_item.name}'.")

        ItemDialog(self.root, self.theme, on_save, item=item)

    def adjust_selected_stock(self, delta: int):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select an item row to adjust stock.")
            return

        item_id = self.tree.item(selected[0])["values"][0]
        success, new_qty, name = self.db.adjust_quantity(item_id, delta)
        if success:
            self.refresh_table()
            self.set_status(f"Stock for '{name}' updated to {new_qty} units.")

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select an item row to delete.")
            return

        values = self.tree.item(selected[0])["values"]
        item_id = values[0]
        name = values[2]
        sku = values[1]

        if messagebox.askyesno("Confirm Deletion", f"Permanently delete '{name}' (SKU: {sku}) from catalog?"):
            success, _ = self.db.delete_item(item_id)
            if success:
                self.refresh_table()
                self.set_status(f"Item '{name}' deleted from database.")

    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.db.export_csv(filename)
            self.set_status(f"Exported inventory to CSV: {os.path.basename(filename)}")
            messagebox.showinfo("Export Successful", f"Inventory catalog exported to:\n{filename}")

    def export_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self.db.export_json(filename)
            self.set_status(f"Exported catalog to JSON: {os.path.basename(filename)}")
            messagebox.showinfo("Export Successful", f"JSON catalog saved to:\n{filename}")

    def reset_demo_data(self):
        if messagebox.askyesno("Reset Catalog", "Reset inventory to the baseline CSE AIML hardware sample dataset?"):
            self.db.reset_to_demo_data()
            self.refresh_table()
            self.set_status("Catalog restored to original baseline sample dataset.")

    def open_tqm_audit(self):
        TqmAuditWindow(self.root, self.theme)

    def show_shortcuts_dialog(self):
        msg = (
            "BBAT104 Q12 Keyboard Shortcuts:\n\n"
            "• Alt + N : Open Add New Item Dialog\n"
            "• Alt + S : Focus Search Input Field\n"
            "• Alt + H : Toggle High Contrast (WCAG AAA)\n"
            "• Alt + D : Toggle Dark / Light Theme\n"
            "• Alt + M : Toggle Minimalist Cognitive View\n"
            "• Alt + + : Increase Font Scale (+20% step)\n"
            "• Alt + - : Decrease Font Scale (-20% step)\n"
            "• Alt + 0 : Reset Font Scale to 100%\n"
            "• Alt + E : Export Inventory to CSV\n"
            "• Up/Down : Traverse table rows\n"
            "• Enter   : Edit Selected Row Item\n"
            "• Delete  : Delete Selected Row Item\n"
            "• Esc     : Close Active Dialog\n"
            "• ?       : Open this Keyboard Shortcuts Guide\n"
        )
        messagebox.showinfo("Keyboard Navigation & Shortcuts", msg)
