import unittest
import tempfile
import io

from pathlib import Path
from datetime import date
from contextlib import redirect_stdout
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

        self.assertEqual(len(main.load_expenses()), 0)

    def test_invalid_amount(self):
        output = io.StringIO()

        with redirect_stdout(output):
            main.add_expense(-50, "Food", "Lunch")

        self.assertEqual(len(main.load_expenses()), 0)
        self.assertIn("Invalid expense details", output.getvalue())

    def test_filter_by_category(self):
        main.add_expense(150, "Food", "Lunch")
        main.add_expense(500, "Travel", "Bus ticket")

        expenses = main.load_expenses()

        filtered = [
            expense for expense in expenses
            if expense.category.lower() == "food"
        ]

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].amount, 150)

    def test_filter_by_date(self):
        main.add_expense(150, "Food", "Lunch")

        today = date.today().isoformat()
        expenses = main.load_expenses()

        filtered = [
            expense for expense in expenses
            if expense.date == today
        ]

        self.assertEqual(len(filtered), 1)

    def test_monthly_summary(self):
        main.add_expense(150, "Food", "Lunch")
        main.add_expense(500, "Travel", "Bus ticket")

        current_month = date.today().strftime("%Y-%m")
        output = io.StringIO()

        with redirect_stdout(output):
            main.monthly_summary(current_month)

        result = output.getvalue()

        self.assertIn("Food: 150.00", result)
        self.assertIn("Travel: 500.00", result)
        self.assertIn("Total: 650.00", result)
    def test_invalid_json_data(self):
        self.test_file.write_text(
            '{"invalid": "data"}',
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            main.load_expenses()

if __name__ == "__main__":
    unittest.main()
