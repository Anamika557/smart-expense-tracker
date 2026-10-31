import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import main


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "expenses.json"
        self.file_patch = patch.object(main, "FILE_NAME", self.test_file)
        self.file_patch.start()

    def tearDown(self):
        self.file_patch.stop()
        self.temp_dir.cleanup()

    def test_add_expense(self):
        main.add_expense(150, "Food", "Lunch")
        expenses = main.load_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 150)

    def test_delete_expense(self):
        main.add_expense(150, "Food", "Lunch")
        main.delete_expense(1)

        self.assertEqual(len(main.load_expenses()), 0)

    def test_invalid_amount(self):
        main.add_expense(-50, "Food", "Lunch")

        expenses = main.load_expenses()
        self.assertEqual(len(expenses), 0)


if __name__ == "__main__":
    unittest.main()