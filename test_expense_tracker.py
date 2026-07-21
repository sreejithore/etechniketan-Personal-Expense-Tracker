import os
import unittest
from datetime import datetime
from expense import Expense
from tracker import ExpenseTracker


class TestExpenseModel(unittest.TestCase):
    def test_expense_creation(self):
        exp = Expense(101, "Team Lunch", 42.50, "Food", "17-07-2026")
        self.assertEqual(exp.id, 101)
        self.assertEqual(exp.title, "Team Lunch")
        self.assertEqual(exp.amount, 42.50)
        self.assertEqual(exp.category, "Food")
        self.assertEqual(exp.date, "17-07-2026")

    def test_to_dict_and_from_dict(self):
        exp = Expense(102, "Office Rent", 1500.00, "Rent", "01-07-2026")
        data = exp.to_dict()
        self.assertEqual(data["id"], 102)
        self.assertEqual(data["title"], "Office Rent")
        self.assertEqual(data["amount"], "1500.00")
        self.assertEqual(data["category"], "Rent")

        reconstructed = Expense.from_dict(data)
        self.assertEqual(exp, reconstructed)


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_expenses.csv"
        self.tracker = ExpenseTracker(filepath=self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_expense_auto_id(self):
        e1 = self.tracker.add_expense("Lunch", 192.50, "Food", "17-07-2026")
        self.assertEqual(e1.id, 101)
        e2 = self.tracker.add_expense("Rent", 1500.00, "Rent", "18-07-2026")
        self.assertEqual(e2.id, 102)
        self.assertEqual(len(self.tracker.get_all_expenses()), 2)

    def test_search_expense(self):
        e1 = self.tracker.add_expense("Lunch", 192.50, "Food", "17-07-2026")
        found = self.tracker.search_expense(101)
        self.assertEqual(found, e1)
        not_found = self.tracker.search_expense(999)
        self.assertIsNone(not_found)

    def test_update_expense(self):
        e1 = self.tracker.add_expense("Lunch", 192.50, "Food", "17-07-2026")
        success = self.tracker.update_expense(101, title="Client Lunch", amount=200.00)
        self.assertTrue(success)
        updated = self.tracker.search_expense(101)
        self.assertEqual(updated.title, "Client Lunch")
        self.assertEqual(updated.amount, 200.00)
        self.assertEqual(updated.category, "Food")

    def test_delete_expense(self):
        e1 = self.tracker.add_expense("Lunch", 192.50, "Food", "17-07-2026")
        e2 = self.tracker.add_expense("Movie", 500.00, "Entertainment", "18-07-2026")
        self.assertEqual(len(self.tracker.get_all_expenses()), 2)
        deleted = self.tracker.delete_expense(101)
        self.assertTrue(deleted)
        self.assertEqual(len(self.tracker.get_all_expenses()), 1)
        self.assertIsNone(self.tracker.search_expense(101))

    def test_telemetry_summary(self):
        self.tracker.add_expense("Team Lunch", 192.50, "Food", "17-07-2026")
        self.tracker.add_expense("Rent", 1500.00, "Rent", "01-07-2026")
        self.tracker.add_expense("Movie", 500.00, "Entertainment", "18-07-2026")

        metrics = self.tracker.get_summary_metrics()
        self.assertEqual(metrics["grand_total"], 2192.50)
        self.assertEqual(metrics["total_items"], 3)
        self.assertEqual(metrics["category_breakdown"]["Food"], 192.50)
        self.assertEqual(metrics["category_breakdown"]["Rent"], 1500.00)
        self.assertEqual(metrics["category_breakdown"]["Entertainment"], 500.00)

    def test_persistence_save_and_load(self):
        self.tracker.add_expense("Team Lunch", 192.50, "Food", "17-07-2026")
        self.tracker.add_expense("Rent", 1500.00, "Rent", "01-07-2026")

        save_success = self.tracker.save_to_csv()
        self.assertTrue(save_success)
        self.assertTrue(os.path.exists(self.test_filename))

        new_tracker = ExpenseTracker(filepath=self.test_filename)
        load_success, loaded_count = new_tracker.load_from_csv()
        self.assertTrue(load_success)
        self.assertEqual(loaded_count, 2)
        self.assertEqual(len(new_tracker.get_all_expenses()), 2)
        self.assertEqual(new_tracker.next_id, 103)


class TestValidators(unittest.TestCase):
    def test_date_strict_format(self):
        try:
            parsed = datetime.strptime("17-07-2026", "%d-%m-%Y")
            self.assertEqual(parsed.day, 17)
            self.assertEqual(parsed.month, 7)
            self.assertEqual(parsed.year, 2026)
        except ValueError:
            self.fail("Date 17-07-2026 should be valid.")

        with self.assertRaises(ValueError):
            datetime.strptime("2026/07/17", "%d-%m-%Y")

        with self.assertRaises(ValueError):
            datetime.strptime("31-02-2026", "%d-%m-%Y")


if __name__ == "__main__":
    unittest.main()
