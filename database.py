"""
================================================================================
BBAT104: FUNDAMENTALS OF TQM - DATABASE ACCESS LAYER (SQLITE3)
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
BASELINE: INVENTORY MANAGEMENT SYSTEM (DIGIT 3: PERSISTENCE & DATA INTEGRITY)
================================================================================
"""

import sqlite3
import os
import csv
import json
import datetime
from typing import Optional, List, Tuple
from models import InventoryItem, AuditLog, StockMetrics

# Database storage path
DEFAULT_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.db")

SAMPLE_DATASET = [
    ("NV-JET-ORIN-8G", "NVIDIA Jetson Orin Nano Dev Kit 8GB", "AI Accelerators", 14, 5, 44500.00, 26, "NVIDIA Partner", "Lab 402 - Cab A", "40 TOPS AI compute, 6-core ARM Cortex-A78AE"),
    ("GGL-CORAL-USB", "Google Coral Edge TPU USB Accelerator", "AI Accelerators", 4, 6, 6800.00, 18, "Google Hardware", "Lab 402 - Shelf 2", "4 TOPS ML coprocessor USB 3.0 Type-C"),
    ("RPI-5-8GB-BRD", "Raspberry Pi 5 Model B (8GB RAM)", "Microcontrollers", 25, 8, 8200.00, 45, "Element14", "Lab 401 - Bin 4", "Quad-core Cortex-A76 @ 2.4GHz, Dual 4Kp60"),
    ("ARD-MEGA-2560", "Arduino Mega 2560 Rev3", "Microcontrollers", 18, 10, 3200.00, 30, "Arduino Store", "Robotics Bench 1", "54 digital I/O pins, 16 analog inputs"),
    ("INT-RS-D435I", "Intel RealSense Depth Camera D435i", "Sensors & Vision", 3, 4, 38500.00, 9, "Intel Robotics", "Vision AI Cart", "Active IR stereo depth sensor, BMI055 IMU"),
    ("RPL-LIDAR-A1", "Slamtec RPLiDAR A1M8 360 Laser Scanner", "Sensors & Vision", 0, 3, 11900.00, 12, "Slamtec Tech", "Autonomous Cart", "12-meter range, 8000 samples/sec"),
    ("LIPO-3S-5200", "Li-Po Battery Pack 11.1V 5200mAh 35C", "Power & Batteries", 6, 5, 3400.00, 15, "Robu Power", "Battery Bunker", "3-Cell (3S1P), XT60 high-current connector"),
    ("MOT-TB6600-DRV", "TB6600 Stepper Motor Driver Controller", "Robotics & Actuators", 2, 6, 1150.00, 20, "RoboElements", "CNC Cart", "4.0A 9-42VDC, microstep 1/32 isolation"),
    ("BME-680-ENV-SEN", "Bosch BME680 Environmental Sensor Breakout", "Sensors & Vision", 15, 5, 1950.00, 22, "Adafruit Ind", "IoT Sensor Kit 3", "Temp, Humidity, Barometric Pressure & VOC"),
    ("RIG-DS1054Z-OSC", "Rigol DS1054Z 50MHz 4-Ch Oscilloscope", "Lab Instruments", 5, 2, 36000.00, 7, "Rigol Tech", "Instruments Bay", "1 GSa/s real-time rate, 24 Mpts memory depth")
]


class Database:
    """Manages SQLite database initialization, transactions, and queries."""

    def __init__(self, db_path: str = DEFAULT_DB_FILE):
        self.db_path = db_path
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        """Returns SQLite connection with row_factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_schema(self):
        """Initializes tables for hardware inventory and immutable audit logs."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT UNIQUE NOT NULL COLLATE NOCASE,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL CHECK (quantity >= 0),
                    min_threshold INTEGER NOT NULL CHECK (min_threshold >= 1),
                    unit_price REAL NOT NULL CHECK (unit_price >= 0),
                    units_issued INTEGER NOT NULL DEFAULT 0 CHECK (units_issued >= 0),
                    supplier TEXT,
                    location TEXT,
                    specs TEXT,
                    updated_at TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    action TEXT NOT NULL
                )
            ''')

            # Seed initial sample data if catalog is empty
            cursor.execute("SELECT COUNT(*) FROM items")
            if cursor.fetchone()[0] == 0:
                self._seed_sample_data(cursor)

            conn.commit()

    def _seed_sample_data(self, cursor: sqlite3.Cursor):
        """Populates baseline CSE AIML hardware catalog."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in SAMPLE_DATASET:
            cursor.execute('''
                INSERT INTO items (sku, name, category, quantity, min_threshold, unit_price, units_issued, supplier, location, specs, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*item, now))

        cursor.execute('''
            INSERT INTO audit_logs (timestamp, action)
            VALUES (?, ?)
        ''', (now, "System initialized with CSE AIML Hardware baseline catalog."))

    def log_action(self, action_text: str):
        """Records an immutable event in the audit trail."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.get_connection() as conn:
                conn.execute("INSERT INTO audit_logs (timestamp, action) VALUES (?, ?)", (now, action_text))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Warning: Failed to write audit log: {e}")

    def add_item(self, item: InventoryItem) -> int:
        """
        Inserts a new inventory product.
        Enforces Poka-Yoke validation and uniqueness constraint on SKU.
        """
        is_valid, error = item.validate()
        if not is_valid:
            raise ValueError(error)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO items (sku, name, category, quantity, min_threshold, unit_price, units_issued, supplier, location, specs, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', item.to_tuple())
                new_id = cursor.lastrowid
                conn.commit()
                self.log_action(f"Added new asset: '{item.name}' (SKU: {item.sku}).")
                return new_id
            except sqlite3.IntegrityError:
                raise ValueError(f"SKU '{item.sku}' already exists in the inventory database.")

    def get_item(self, item_id: int) -> Optional[InventoryItem]:
        """Retrieves a single inventory item by database ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, sku, name, category, quantity, min_threshold, unit_price, units_issued, supplier, location, specs, updated_at FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            return InventoryItem.from_row(row) if row else None

    def get_item_by_sku(self, sku: str) -> Optional[InventoryItem]:
        """Retrieves an item by SKU (case-insensitive)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, sku, name, category, quantity, min_threshold, unit_price, units_issued, supplier, location, specs, updated_at FROM items WHERE sku = ?", (sku.strip().upper(),))
            row = cursor.fetchone()
            return InventoryItem.from_row(row) if row else None

    def get_all_items(
        self,
        search_query: str = "",
        category: str = "ALL",
        status: str = "ALL",
        sort_by: str = "name-asc"
    ) -> List[InventoryItem]:
        """
        Queries catalog items with multi-criteria filtering and sorting.
        """
        query = "SELECT id, sku, name, category, quantity, min_threshold, unit_price, units_issued, supplier, location, specs, updated_at FROM items WHERE 1=1"
        params = []

        # Search filter across multiple fields
        q = search_query.strip().lower()
        if q:
            query += " AND (LOWER(name) LIKE ? OR LOWER(sku) LIKE ? OR LOWER(supplier) LIKE ? OR LOWER(specs) LIKE ?)"
            wildcard = f"%{q}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])

        # Category filter
        if category != "ALL":
            query += " AND category = ?"
            params.append(category)

        # Stock status filter
        if status == "IN_STOCK":
            query += " AND quantity > min_threshold"
        elif status == "LOW_STOCK":
            query += " AND quantity > 0 AND quantity <= min_threshold"
        elif status == "OUT_OF_STOCK":
            query += " AND quantity = 0"

        # Sorting logic
        sort_dict = {
            "name-asc": " ORDER BY name ASC",
            "name-desc": " ORDER BY name DESC",
            "qty-asc": " ORDER BY quantity ASC",
            "qty-desc": " ORDER BY quantity DESC",
            "price-asc": " ORDER BY unit_price ASC",
            "price-desc": " ORDER BY unit_price DESC",
            "date-desc": " ORDER BY updated_at DESC"
        }
        query += sort_dict.get(sort_by, " ORDER BY name ASC")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [InventoryItem.from_row(row) for row in cursor.fetchall()]

    def update_item(self, item: InventoryItem) -> bool:
        """Updates an existing inventory item."""
        if not item.id:
            raise ValueError("Item ID is required for update.")

        is_valid, error = item.validate()
        if not is_valid:
            raise ValueError(error)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''
                    UPDATE items SET
                        sku = ?,
                        name = ?,
                        category = ?,
                        quantity = ?,
                        min_threshold = ?,
                        unit_price = ?,
                        units_issued = ?,
                        supplier = ?,
                        location = ?,
                        specs = ?,
                        updated_at = ?
                    WHERE id = ?
                ''', (*item.to_tuple()[:-1], now, item.id))

                if cursor.rowcount == 0:
                    return False

                conn.commit()
                self.log_action(f"Updated asset details: '{item.name}' (SKU: {item.sku}).")
                return True
            except sqlite3.IntegrityError:
                raise ValueError(f"SKU '{item.sku}' conflicts with another item in catalog.")

    def adjust_quantity(self, item_id: int, delta: int) -> Tuple[bool, int, str]:
        """
        Quick stock adjustment (+1 / -1) with boundary checks.
        Returns (success, new_quantity, item_name).
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, quantity FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if not row:
                return False, 0, ""

            name, current_qty = row
            new_qty = max(0, current_qty + delta)
            if new_qty == current_qty:
                return True, current_qty, name

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE items SET quantity = ?, updated_at = ? WHERE id = ?", (new_qty, now, item_id))
            conn.commit()

            self.log_action(f"Adjusted stock for '{name}': {current_qty} -> {new_qty} units.")
            return True, new_qty, name

    def delete_item(self, item_id: int) -> Tuple[bool, str]:
        """Deletes an item by ID. Returns (success, item_name)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, sku FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if not row:
                return False, ""

            name, sku = row
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()

            self.log_action(f"Deleted asset: '{name}' (SKU: {sku}).")
            return True, name

    def get_metrics(self) -> StockMetrics:
        """Computes aggregate inventory performance metrics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    COUNT(*),
                    COALESCE(SUM(quantity), 0),
                    COALESCE(SUM(quantity * unit_price), 0.0),
                    COALESCE(SUM(CASE WHEN quantity <= min_threshold AND quantity > 0 THEN 1 ELSE 0 END), 0),
                    COALESCE(SUM(CASE WHEN quantity = 0 THEN 1 ELSE 0 END), 0),
                    COALESCE(AVG(CASE WHEN quantity > 0 THEN CAST(units_issued AS REAL) / quantity ELSE 0 END), 0.0)
                FROM items
            ''')
            row = cursor.fetchone()
            return StockMetrics(
                total_skus=row[0],
                total_units=row[1],
                total_valuation=row[2],
                low_stock_count=row[3],
                out_of_stock_count=row[4],
                avg_turnover=row[5]
            )

    def get_audit_logs(self, limit: int = 50) -> List[AuditLog]:
        """Fetches recent audit log entries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, action FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
            return [AuditLog(log_id=row[0], timestamp=row[1], action=row[2]) for row in cursor.fetchall()]

    def reset_to_demo_data(self):
        """Restores the original laboratory baseline catalog."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items")
            self._seed_sample_data(cursor)
            conn.commit()
            self.log_action("Catalog reset to baseline CSE AIML demo dataset.")

    def export_csv(self, filepath: str):
        """Exports catalog to CSV file."""
        items = self.get_all_items()
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "SKU", "Item Name", "Category", "Quantity", "Min Threshold",
                "Unit Price (INR)", "Units Issued", "Turnover Ratio", "Status",
                "Supplier", "Location", "Specs", "Last Updated"
            ])
            for it in items:
                status_code, label, _ = it.get_stock_status()
                writer.writerow([
                    it.sku, it.name, it.category, it.quantity, it.min_threshold,
                    f"{it.unit_price:.2f}", it.units_issued, f"{it.get_turnover_ratio()}x",
                    label, it.supplier, it.location, it.specs, it.updated_at
                ])
        self.log_action(f"Exported inventory catalog to CSV: {os.path.basename(filepath)}")

    def export_json(self, filepath: str):
        """Exports catalog to formatted JSON file."""
        items = self.get_all_items()
        data = [
            {
                "id": it.id,
                "sku": it.sku,
                "name": it.name,
                "category": it.category,
                "quantity": it.quantity,
                "min_threshold": it.min_threshold,
                "unit_price": it.unit_price,
                "units_issued": it.units_issued,
                "supplier": it.supplier,
                "location": it.location,
                "specs": it.specs,
                "updated_at": it.updated_at
            }
            for it in items
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.log_action(f"Exported inventory catalog to JSON: {os.path.basename(filepath)}")

    def import_json(self, filepath: str) -> int:
        """
        Imports and validates items from JSON.
        Returns count of successfully imported records.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if not isinstance(raw_data, list):
            raise ValueError("Root element of JSON must be an array of item objects.")

        imported_count = 0
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for entry in raw_data:
                try:
                    item = InventoryItem(
                        sku=entry.get("sku", ""),
                        name=entry.get("name", ""),
                        category=entry.get("category", "AI Accelerators"),
                        quantity=entry.get("quantity", 0),
                        min_threshold=entry.get("min_threshold", 5),
                        unit_price=entry.get("unit_price", 0.0),
                        units_issued=entry.get("units_issued", 0),
                        supplier=entry.get("supplier", ""),
                        location=entry.get("location", ""),
                        specs=entry.get("specs", ""),
                        updated_at=now
                    )
                    is_valid, _ = item.validate()
                    if is_valid:
                        cursor.execute('''
                            INSERT INTO items (sku, name, category, quantity, min_threshold, unit_price, units_issued, supplier, location, specs, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(sku) DO UPDATE SET
                                name=excluded.name,
                                category=excluded.category,
                                quantity=excluded.quantity,
                                min_threshold=excluded.min_threshold,
                                unit_price=excluded.unit_price,
                                supplier=excluded.supplier,
                                location=excluded.location,
                                specs=excluded.specs,
                                updated_at=excluded.updated_at
                        ''', item.to_tuple())
                        imported_count += 1
                except Exception as e:
                    print(f"Skipping invalid item in import: {e}")

            conn.commit()

        self.log_action(f"Imported/merged {imported_count} inventory items from {os.path.basename(filepath)}.")
        return imported_count
