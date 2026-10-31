import argparse
import json
from pathlib import Path
from datetime import date, datetime
from dataclasses import dataclass, asdict
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ValidationError
import requests


FILE_NAME = Path(__file__).parent / "expenses.json"


# Expense data model
@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    date: str


class ExpenseValidator(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)


# Load expenses from JSON
def load_expenses() -> list[Expense]:
    if not FILE_NAME.exists():
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        expenses = []

        for index, item in enumerate(data, start=1):
            item.setdefault("id", index)
            expenses.append(Expense(**item))

        return expenses

    except (json.JSONDecodeError, TypeError, KeyError) as error:
        raise ValueError(f"Could not read expenses.json: {error}")


# Save expenses to JSON
def save_expenses(expenses: list[Expense]) -> None:
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            [asdict(expense) for expense in expenses],
            file,
            indent=4
        )


# Add expense
def add_expense(amount: float, category: str, description: str) -> None:
    try:
        validated = ExpenseValidator(
            amount=amount,
            category=category.strip(),
            description=description.strip()
        )

    except ValidationError as error:
        print("Invalid expense details:")
        for issue in error.errors():
            print("-", issue["msg"])
        return

    expenses = load_expenses()

    new_id = max((expense.id for expense in expenses), default=0) + 1

    expense = Expense(
        id=new_id,
        amount=validated.amount,
        category=validated.category.title(),
        description=validated.description,
        date=date.today().isoformat()
    )

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")


# List expenses
def list_expenses() -> None:
    expenses = load_expenses()

    if not expenses:
        print("No expenses found!")
        return

    print("\n===== YOUR EXPENSES =====")

    for expense in expenses:
        print(
            f"ID: {expense.id} | "
            f"Amount: {expense.amount:.2f} | "
            f"Category: {expense.category} | "
            f"Description: {expense.description} | "
            f"Date: {expense.date}"
        )


# Delete expense
def delete_expense(expense_id: int) -> None:
    expenses = load_expenses()

    for expense in expenses:
        if expense.id == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print("Expense deleted successfully!")
            return

    print("Expense ID not found!")


# Filter expenses
def filter_expenses(
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> None:

    expenses = load_expenses()

    if category:
        expenses = [
            expense for expense in expenses
            if expense.category.lower() == category.lower()
        ]

    try:
        start = date.fromisoformat(start_date) if start_date else None
        end = date.fromisoformat(end_date) if end_date else None

        if start and end and start > end:
            raise ValueError("Start date cannot be after end date.")

        if start:
            expenses = [
                expense for expense in expenses
                if date.fromisoformat(expense.date) >= start
            ]

        if end:
            expenses = [
                expense for expense in expenses
                if date.fromisoformat(expense.date) <= end
            ]

    except ValueError as error:
        raise ValueError(f"Invalid date: {error}")

    if not expenses:
        print("No matching expenses found!")
        return

    for expense in expenses:
        print(asdict(expense))


# Monthly summary per category
def monthly_summary(month: str) -> None:
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("Invalid month. Use YYYY-MM format.")

    expenses = load_expenses()
    summary = {}

    for expense in expenses:
        if expense.date.startswith(month):
            summary[expense.category] = (
                summary.get(expense.category, 0) + expense.amount
            )

    if not summary:
        print("No expenses found for this month!")
        return

    print(f"\n===== SUMMARY FOR {month} =====")

    for category, total in summary.items():
        print(f"{category}: {total:.2f}")

    print(f"Total: {sum(summary.values()):.2f}")


# Total expenses
def total_expenses() -> None:
    expenses = load_expenses()

    total = sum(expense.amount for expense in expenses)

    print(f"Total Expenses: {total:.2f}")


# Currency conversion using Frankfurter API
def convert_currency(from_currency: str, to_currency: str) -> None:
    expenses = load_expenses()

    if not expenses:
        print("No expenses available for conversion!")
        return

    total = sum(expense.amount for expense in expenses)

    url = "https://api.frankfurter.app/latest"

    try:
        response = requests.get(
            url,
            params={
                "amount": total,
                "from": from_currency.upper(),
                "to": to_currency.upper()
            },
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        converted = data["rates"][to_currency.upper()]

        print(f"Total in {from_currency.upper()}: {total:.2f}")
        print(f"Total in {to_currency.upper()}: {converted:.2f}")

    except requests.RequestException as error:
        print(f"Currency API error: {error}")

    except (KeyError, ValueError):
        print("Could not retrieve the exchange rate.")


# Argparse command-line interface
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smart Expense Tracker CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Add command
    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--description", required=True)

    # List command
    subparsers.add_parser("list", help="List all expenses")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", type=int, required=True)

    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Filter expenses")
    filter_parser.add_argument("--category")
    filter_parser.add_argument("--start-date")
    filter_parser.add_argument("--end-date")

    # Monthly summary command
    summary_parser = subparsers.add_parser(
        "summary",
        help="Show monthly category summary"
    )
    summary_parser.add_argument("--month", required=True)

    # Total command
    subparsers.add_parser("total", help="Show total expenses")

    # Currency conversion command
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert total expenses to another currency"
    )
    convert_parser.add_argument("--from-currency", required=True)
    convert_parser.add_argument("--to-currency", required=True)

    args = parser.parse_args()

    try:
        if args.command == "add":
            add_expense(args.amount, args.category, args.description)

        elif args.command == "list":
            list_expenses()

        elif args.command == "delete":
            delete_expense(args.id)

        elif args.command == "filter":
            if not any([args.category, args.start_date, args.end_date]):
                parser.error("Provide at least one filter option.")

            filter_expenses(
                args.category,
                args.start_date,
                args.end_date
            )

        elif args.command == "summary":
            monthly_summary(args.month)

        elif args.command == "total":
            total_expenses()

        elif args.command == "convert":
            convert_currency(
                args.from_currency,
                args.to_currency
            )

    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
