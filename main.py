import csv

FILE_NAME = "expenses.csv"


def add_expense():
    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

        category = input("Enter category: ").strip().title()

        if not category:
            print("Category cannot be empty!")
            return

        description = input("Enter description: ").strip()

        if not description:
            print("Description cannot be empty!")
            return

        with open(FILE_NAME, "a+", newline="", encoding="utf-8") as file:
            file.seek(0, 2)

            if file.tell() == 0:
                writer = csv.writer(file, lineterminator="\n")
                writer.writerow(["amount", "category", "description"])
            else:
                file.seek(0)
                content = file.read()

                if not content.endswith(("\n", "\r")):
                    file.write("\n")

            writer = csv.writer(file, lineterminator="\n")
            writer.writerow([amount, category, description])

        print("Expense added successfully!")

    except ValueError:
        print("Please enter a valid number!")


def view_expenses():
    print("\n===== YOUR EXPENSES =====")

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                print("\nAmount:", row["amount"])
                print("Category:", row["category"])
                print("Description:", row["description"])
                print("--------------------------")

    except FileNotFoundError:
        print("No expense file found!")


def category_summary():
    expenses = {}

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                category = row["category"].strip().title()
                amount = float(row["amount"])

                if category in expenses:
                    expenses[category] += amount
                else:
                    expenses[category] = amount

        print("===== CATEGORY SUMMARY =====")

        if not expenses:
            print("No expenses found!")
            return

        for category, total in expenses.items():
            print(category, ":", total)

    except FileNotFoundError:
        print("No expense file found!")


def total_expenses():
    total = 0

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                total += float(row["amount"])

        print("Total Expenses:", total)

    except FileNotFoundError:
        print("No expense file found!")

while True:
    print("\n===== SMART EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Category Summary")
    print("4. Total Expenses")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        category_summary()

    elif choice == "4":
        total_expenses()

    elif choice == "5":
        print("Thank you for using Smart Expense Tracker!")
        break

    else:
        print("Invalid choice! Please try again.")