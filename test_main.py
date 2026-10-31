import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import main


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "expenses.json"

        self.file_patch = patch.object(
            main, "FILE_NAME", self.test_file
        )
        self.file_patch.start()

    def tearDown(self):
        self.file_patch.stop()
        self.temp_dir.cleanup()

    def test_add_expense(self):
        main.add_expense(150, "Food", "Lunch")

        expenses = main.load_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 150)
        self.assertEqual(expenses[0].category, "Food")

    def test_delete_expense(self):
        main.add_expense(150, "Food", "Lunch")

        main.delete_expense(1)

        expenses = main.load_expenses()

        self.assertEqual(len(expenses), 0)

    def test_invalid_amount(self):
        main.add_expense(-50, "Food", "Lunch")

        expenses = main.load_expenses()

        self.assertEqual(len(expenses), 0)

    def test_filter_by_category(self):
        main.add_expense(150, "Food", "Lunch")
        main.add_expense(500, "Travel", "Bus ticket")

        expenses = main.load_expenses()

        filtered = [
            expense for expense in expenses
            if expense.category == "Food"
        ]

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].category, "Food")


if __name__ == "__main__":
    unittest.main()
