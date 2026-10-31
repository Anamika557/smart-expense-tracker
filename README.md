# Smart Expense Tracker CLI

## Project Description

Smart Expense Tracker is a Python-based command-line application that helps users manage and track their daily expenses.

It allows users to add, view, delete, filter, and summarize expenses. All expense records are stored in a JSON file. It also supports currency conversion using a free exchange-rate API.

## Features

* Add new expenses with amount, category, and description.
* View all recorded expenses.
* Delete expenses using their ID.
* Filter expenses by category.
* Filter expenses by date range.
* Generate monthly category-wise summaries.
* Calculate total expenses.
* Convert total expenses into another currency using an exchange-rate API.
* Validate user inputs and display error messages.
* Store expense records in JSON format.

## Technologies Used

* Python
* argparse
* JSON
* Dataclasses
* Type Hints
* Requests
* Frankfurter Exchange Rate API

## Project Structure

```text
smart-expense-tracker/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── expenses.json  (generated automatically)
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Anamika557/smart-expense-tracker.git
```

2. Navigate to the project directory:

```bash
cd smart-expense-tracker
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Add an Expense

```bash
python main.py add --amount 150 --category Food --description "Lunch"
```

### List All Expenses

```bash
python main.py list
```

### Delete an Expense

```bash
python main.py delete --id 1
```

### Filter by Category

```bash
python main.py filter --category Food
```

### Filter by Date Range

```bash
python main.py filter --start-date 2026-10-01 --end-date 2026-10-31
```

### Monthly Summary

```bash
python main.py summary --month 2026-10
```

### Calculate Total Expenses

```bash
python main.py total
```

### Currency Conversion

```bash
python main.py convert --from-currency INR --to-currency USD
```

### View Available Commands

```bash
python main.py --help
```

## Sample Output

```text
===== YOUR EXPENSES =====

ID: 1 | Amount: 150.00 | Category: Food
Description: Lunch | Date: 2026-10-31

ID: 2 | Amount: 500.00 | Category: Travel
Description: Bus ticket | Date: 2026-10-31
```

## Data Storage

Expense records are stored locally in `expenses.json`. The application automatically creates and updates this file whenever expenses are added or deleted.

## Currency Conversion

The application uses the Frankfurter Exchange Rate API to retrieve exchange rates and convert the total expense amount into the selected currency.

## What I Learned

* Working with Python command-line arguments using argparse.
* Reading and writing JSON files.
* Using dataclasses and type hints.
* Implementing filtering and summary operations.
* Integrating an external API using Requests.
* Handling invalid inputs and errors.

## Author

Anamika MP
