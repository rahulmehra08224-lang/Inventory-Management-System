"""
================================================================================
UNIT TESTS: DATABASE PERSISTENCE, CRUD OPERATIONS & INTEGRITY (SQLITE)
STUDENT: RAHUL MEHRA | CSE AIML (SECTION B)
================================================================================
"""

import unittest
import os
import sys
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import Database
from models import InventoryItem


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        # Create unique temporary SQLite file for isolated testing
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db = Database(self.temp_file.name)

    def tearDown(self):
        # Remove temporary database file after tests
        if os.path.exists(self.temp_file.name):
            try:
                os.remove(self.temp_file.name)
            except PermissionError:
                pass

    def test_database_initialization_and_seeding(self):
        # Check initial sample items exist
        items = self.db.get_all_items()
        self.assertGreater(len(items), 0)
        metrics = self.db.get_metrics()
        self.assertGreater(metrics.total_skus, 0)
        self.assertGreater(metrics.total_units, 0)
        self.assertGreater(metrics.total_valuation, 0)

    def test_add_item_success(self):
        item = InventoryItem(
            sku="TEST-SKU-999",
            name="Test Equipment Unit",
            category="AI Accelerators",
            quantity=15,
            min_threshold=5,
            unit_price=25000.0,
            supplier="Test Vendor"
        )
        new_id = self.db.add_item(item)
        self.assertIsInstance(new_id, int)
        self.assertGreater(new_id, 0)

        # Retrieve and verify
        retrieved = self.db.get_item(new_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.sku, "TEST-SKU-999")
        self.assertEqual(retrieved.name, "Test Equipment Unit")
        self.assertEqual(retrieved.quantity, 15)

    def test_duplicate_sku_rejection(self):
        item1 = InventoryItem(
            sku="DUP-SKU-100",
            name="First Unit",
            category="Microcontrollers",
            quantity=5,
            min_threshold=2,
            unit_price=1000.0
        )
        self.db.add_item(item1)

        # Attempt to insert same SKU
        item2 = InventoryItem(
            sku="DUP-SKU-100",
            name="Second Unit Duplicate",
            category="Microcontrollers",
            quantity=8,
            min_threshold=3,
            unit_price=1200.0
        )
        with self.assertRaises(ValueError) as context:
            self.db.add_item(item2)
        self.assertIn("already exists", str(context.exception))

    def test_update_item(self):
        item = InventoryItem(
            sku="UPD-SKU-200",
            name="Original Name",
            category="Sensors & Vision",
            quantity=10,
            min_threshold=4,
            unit_price=5000.0
        )
        item_id = self.db.add_item(item)

        # Fetch, modify, update
        to_update = self.db.get_item(item_id)
        to_update.name = "Modified Updated Name"
        to_update.quantity = 22
        success = self.db.update_item(to_update)
        self.assertTrue(success)

        # Verify modification persisted
        updated = self.db.get_item(item_id)
        self.assertEqual(updated.name, "Modified Updated Name")
        self.assertEqual(updated.quantity, 22)

    def test_adjust_quantity(self):
        item = InventoryItem(
            sku="ADJ-SKU-300",
            name="Adjustment Test Part",
            category="Power & Batteries",
            quantity=10,
            min_threshold=3,
            unit_price=1500.0
        )
        item_id = self.db.add_item(item)

        # Increment +3
        success, new_qty, _ = self.db.adjust_quantity(item_id, 3)
        self.assertTrue(success)
        self.assertEqual(new_qty, 13)

        # Decrement -5
        success, new_qty, _ = self.db.adjust_quantity(item_id, -5)
        self.assertTrue(success)
        self.assertEqual(new_qty, 8)

        # Decrement past zero (should clamp to 0, not negative)
        success, new_qty, _ = self.db.adjust_quantity(item_id, -100)
        self.assertTrue(success)
        self.assertEqual(new_qty, 0)

    def test_delete_item(self):
        item = InventoryItem(
            sku="DEL-SKU-400",
            name="Delete Candidate",
            category="Lab Instruments",
            quantity=2,
            min_threshold=1,
            unit_price=8000.0
        )
        item_id = self.db.add_item(item)
        self.assertIsNotNone(self.db.get_item(item_id))

        # Delete
        success, name = self.db.delete_item(item_id)
        self.assertTrue(success)
        self.assertEqual(name, "Delete Candidate")

        # Confirm gone
        self.assertIsNone(self.db.get_item(item_id))

    def test_search_and_filtering(self):
        # Search by specific keyword
        results = self.db.get_all_items(search_query="Jetson")
        self.assertTrue(any("Jetson" in it.name for it in results))

        # Filter by category
        ai_items = self.db.get_all_items(category="AI Accelerators")
        self.assertTrue(all(it.category == "AI Accelerators" for it in ai_items))

        # Filter by stock status
        out_of_stock_items = self.db.get_all_items(status="OUT_OF_STOCK")
        self.assertTrue(all(it.quantity == 0 for it in out_of_stock_items))

    def test_audit_logs_recording(self):
        initial_logs = self.db.get_audit_logs()
        self.db.log_action("Test event logged manually.")
        updated_logs = self.db.get_audit_logs()
        self.assertGreater(len(updated_logs), len(initial_logs))
        self.assertEqual(updated_logs[0].action, "Test event logged manually.")


if __name__ == "__main__":
    unittest.main()
