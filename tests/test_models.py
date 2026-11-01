"""
================================================================================
UNIT TESTS: INVENTORY MODELS & POKA-YOKE VALIDATION
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
================================================================================
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import InventoryItem, VALID_CATEGORIES


class TestInventoryModels(unittest.TestCase):

    def test_valid_item_creation(self):
        item = InventoryItem(
            sku="NV-JET-01",
            name="NVIDIA Jetson Orin Nano",
            category="AI Accelerators",
            quantity=10,
            min_threshold=5,
            unit_price=45000.0,
            units_issued=20
        )
        is_valid, error = item.validate()
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
        self.assertEqual(item.sku, "NV-JET-01")

    def test_empty_sku_rejection(self):
        item = InventoryItem(
            sku="",
            name="Jetson Nano",
            category="AI Accelerators",
            quantity=5,
            min_threshold=2,
            unit_price=10000.0
        )
        is_valid, error = item.validate()
        self.assertFalse(is_valid)
        self.assertIn("SKU / Asset Code is mandatory", error)

    def test_invalid_category_rejection(self):
        item = InventoryItem(
            sku="TST-01",
            name="Test Board",
            category="NonExistentCategory",
            quantity=5,
            min_threshold=2,
            unit_price=1000.0
        )
        is_valid, error = item.validate()
        self.assertFalse(is_valid)
        self.assertIn("Category must be one of", error)

    def test_negative_quantity_rejection(self):
        item = InventoryItem(
            sku="TST-02",
            name="Test Sensor",
            category="Sensors & Vision",
            quantity=-1,
            min_threshold=2,
            unit_price=500.0
        )
        is_valid, error = item.validate()
        self.assertFalse(is_valid)
        self.assertIn("Quantity cannot be negative", error)

    def test_zero_threshold_rejection(self):
        item = InventoryItem(
            sku="TST-03",
            name="Test Sensor",
            category="Sensors & Vision",
            quantity=10,
            min_threshold=0,
            unit_price=500.0
        )
        is_valid, error = item.validate()
        self.assertFalse(is_valid)
        self.assertIn("Low stock threshold must be at least 1 unit", error)

    def test_stock_status_out_of_stock(self):
        item = InventoryItem(
            sku="ZERO-01",
            name="Empty Stock Part",
            category="Microcontrollers",
            quantity=0,
            min_threshold=5,
            unit_price=2000.0
        )
        code, label, sym = item.get_stock_status()
        self.assertEqual(code, "OUT_OF_STOCK")
        self.assertEqual(sym, "×")

    def test_stock_status_low_stock(self):
        item = InventoryItem(
            sku="LOW-01",
            name="Low Stock Part",
            category="Microcontrollers",
            quantity=4,
            min_threshold=5,
            unit_price=2000.0
        )
        code, label, sym = item.get_stock_status()
        self.assertEqual(code, "LOW_STOCK")
        self.assertEqual(sym, "⚠")

    def test_stock_status_in_stock(self):
        item = InventoryItem(
            sku="IN-01",
            name="Well Stocked Part",
            category="Microcontrollers",
            quantity=15,
            min_threshold=5,
            unit_price=2000.0
        )
        code, label, sym = item.get_stock_status()
        self.assertEqual(code, "IN_STOCK")
        self.assertEqual(sym, "✓")

    def test_turnover_and_fsn_classification(self):
        # Fast moving: 30 issued / 10 held = 3.0x
        fast_item = InventoryItem("FST-01", "Fast Part", "AI Accelerators", 10, 5, 1000.0, units_issued=30)
        self.assertEqual(fast_item.get_turnover_ratio(), 3.0)
        self.assertEqual(fast_item.get_fsn_classification(), "Fast (F)")

        # Slow moving: 10 issued / 10 held = 1.0x
        slow_item = InventoryItem("SLW-01", "Slow Part", "AI Accelerators", 10, 5, 1000.0, units_issued=10)
        self.assertEqual(slow_item.get_turnover_ratio(), 1.0)
        self.assertEqual(slow_item.get_fsn_classification(), "Slow (S)")

        # Non moving: 2 issued / 10 held = 0.2x
        non_item = InventoryItem("NON-01", "Non-moving Part", "AI Accelerators", 10, 5, 1000.0, units_issued=2)
        self.assertEqual(non_item.get_turnover_ratio(), 0.2)
        self.assertEqual(non_item.get_fsn_classification(), "Non-Moving (N)")

    def test_reorder_point_calculation(self):
        item = InventoryItem("ROP-01", "ROP Test Item", "Robotics & Actuators", 8, 5, 1500.0)
        rop = item.calculate_reorder_point(lead_time_days=7, daily_usage=0.5)
        self.assertGreater(rop, 0)
        # ROP should equal lead_time_demand + safety_stock
        self.assertTrue(rop >= 7)


if __name__ == "__main__":
    unittest.main()
