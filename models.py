"""
================================================================================
BBAT104: FUNDAMENTALS OF TQM - DOMAIN DATA MODELS & VALIDATION (POKA-YOKE)
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
BASELINE: INVENTORY MANAGEMENT SYSTEM (DIGIT 3: STOCKOUT ELIMINATION & TURNOVER)
================================================================================
"""

import datetime
import math

# Recognized Component Categories in CSE AIML Laboratory
VALID_CATEGORIES = [
    "AI Accelerators",
    "Microcontrollers",
    "Sensors & Vision",
    "Robotics & Actuators",
    "Power & Batteries",
    "Lab Instruments"
]


class InventoryItem:
    """Represents a single hardware asset in the inventory catalog."""

    def __init__(
        self,
        sku: str,
        name: str,
        category: str,
        quantity: int,
        min_threshold: int,
        unit_price: float,
        units_issued: int = 0,
        supplier: str = "",
        location: str = "",
        specs: str = "",
        updated_at: str = None,
        item_id: int = None
    ):
        self.id = item_id
        self.sku = str(sku).strip().upper()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.quantity = int(quantity)
        self.min_threshold = int(min_threshold)
        self.unit_price = round(float(unit_price), 2)
        self.units_issued = int(units_issued)
        self.supplier = str(supplier).strip()
        self.location = str(location).strip()
        self.specs = str(specs).strip()
        self.updated_at = updated_at or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def validate(self) -> tuple[bool, str]:
        """
        Poka-Yoke (Mistake-Proofing) validation.
        Returns (True, '') if valid, or (False, error_message).
        """
        if not self.sku:
            return False, "SKU / Asset Code is mandatory."
        if len(self.sku) < 3 or len(self.sku) > 30:
            return False, "SKU must be between 3 and 30 alphanumeric characters."
        if not self.name:
            return False, "Item Name is mandatory."
        if len(self.name) < 2:
            return False, "Item Name must have at least 2 characters."
        if not self.category or self.category not in VALID_CATEGORIES:
            return False, f"Category must be one of: {', '.join(VALID_CATEGORIES)}."
        if self.quantity < 0:
            return False, "Quantity cannot be negative."
        if self.min_threshold < 1:
            return False, "Low stock threshold must be at least 1 unit."
        if self.unit_price < 0:
            return False, "Unit price cannot be negative."
        return True, ""

    def get_stock_status(self) -> tuple[str, str, str]:
        """
        Determines current stockout risk level.
        Returns: (status_code, display_label, symbol)
        """
        if self.quantity == 0:
            return "OUT_OF_STOCK", "Out of Stock", "×"
        elif self.quantity <= self.min_threshold:
            return "LOW_STOCK", f"Low Stock ({self.quantity}/{self.min_threshold})", "⚠"
        else:
            return "IN_STOCK", "In Stock", "✓"

    def get_turnover_ratio(self) -> float:
        """
        Inventory Turnover Ratio (ITR) = Units Issued / Current Units Held.
        Reflects capital velocity and component utilization.
        """
        effective_stock = max(1, self.quantity)
        return round(self.units_issued / effective_stock, 2)

    def get_fsn_classification(self) -> str:
        """
        Fast, Slow, and Non-Moving (FSN) Inventory Analysis:
        - Fast-Moving (F): ITR >= 2.0x (high academic utilization)
        - Slow-Moving (S): 0.8x <= ITR < 2.0x (moderate utilization)
        - Non-Moving (N): ITR < 0.8x (low or stagnant utilization)
        """
        ratio = self.get_turnover_ratio()
        if ratio >= 2.0:
            return "Fast (F)"
        elif ratio >= 0.8:
            return "Slow (S)"
        else:
            return "Non-Moving (N)"

    def calculate_reorder_point(self, lead_time_days: int = 7, daily_usage: float = 0.5) -> int:
        """
        Reorder Point (ROP) = (Daily Demand * Lead Time) + Safety Stock.
        Safety Stock SS = Z * sqrt(Lead Time * var_demand).
        """
        z_score = 1.65  # 95% service level
        safety_stock = math.ceil(z_score * math.sqrt(lead_time_days * 0.4))
        lead_time_demand = math.ceil(daily_usage * lead_time_days)
        return lead_time_demand + safety_stock

    def to_tuple(self) -> tuple:
        return (
            self.sku,
            self.name,
            self.category,
            self.quantity,
            self.min_threshold,
            self.unit_price,
            self.units_issued,
            self.supplier,
            self.location,
            self.specs,
            self.updated_at
        )

    @classmethod
    def from_row(cls, row: tuple) -> "InventoryItem":
        """Factory method to instantiate from SQLite row."""
        return cls(
            item_id=row[0],
            sku=row[1],
            name=row[2],
            category=row[3],
            quantity=row[4],
            min_threshold=row[5],
            unit_price=row[6],
            units_issued=row[7] if len(row) > 7 else 0,
            supplier=row[8] if len(row) > 8 else "",
            location=row[9] if len(row) > 9 else "",
            specs=row[10] if len(row) > 10 else "",
            updated_at=row[11] if len(row) > 11 else None
        )


class AuditLog:
    """Represents a timestamped change entry in the activity audit trail."""

    def __init__(self, action: str, timestamp: str = None, log_id: int = None):
        self.id = log_id
        self.timestamp = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.action = action


class StockMetrics:
    """Aggregated inventory performance metrics for the dashboard."""

    def __init__(
        self,
        total_skus: int,
        total_units: int,
        total_valuation: float,
        low_stock_count: int,
        out_of_stock_count: int,
        avg_turnover: float
    ):
        self.total_skus = total_skus
        self.total_units = total_units
        self.total_valuation = total_valuation
        self.low_stock_count = low_stock_count
        self.out_of_stock_count = out_of_stock_count
        self.avg_turnover = round(avg_turnover, 2)
