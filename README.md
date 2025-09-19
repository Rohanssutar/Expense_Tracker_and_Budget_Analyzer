# Expense Tracker & Budget Analyzer
#### Video Demo: <>

#### Description:
A command-line Python application that helps you **track expenses**, **categorize transactions**, and **analyze monthly budgets** using a CSV file of transactions.

This project is perfect for managing personal finances and looks great on a resume or portfolio. It was built following structured programming principles and includes unit tests using `pytest`.

---

## **Features**
- 📊 **Transaction Parsing**
  Reads transaction data from a CSV file with headers:
date, description, amount
- Supports multiple date formats (`YYYY-MM-DD`, `DD-MM-YYYY`, `MM-DD-YYYY`).
- Automatically converts amounts to floats, handling commas in numbers.

- 🗂 **Automatic Categorization**
Uses keyword-based rules to categorize transactions into:
  - Coffee
  - Groceries
  - Income
  - Housing
  - Transport
  - Subscriptions
  - Shopping
  - Uncategorized (fallback)

- 📅 **Monthly Summary**
Groups transactions by month and calculates:
  - Total income/expenses
  - Transaction count
  - Category breakdown

- 💵 **Budget Recommendations**
Provides simple, data-driven suggestions, such as:
  - Areas where you can cut back spending
  - Progress towards a target savings goal

- ✅ **Unit Testing with Pytest**
Three core functions are fully tested:
  - `parse_transactions`
  - `categorize_transactions`
  - `monthly_summary`

---

## **Project Structure**
```
expense-tracker/
│
├── project.py # Main project file
├── test_project.py # Unit tests
├── sample.csv # Example transaction data
└── README.md # This file
```
## **Running the Project**

Once you have your CSV file ready, run:

```
python project.py sample.csv
```

## Sample Output
```
Monthly summary (month: total, count):
2025-09: 1087.44, 7 transactions
```

### This output shows:
The total balance for the month (Income - Expenses).
The number of transactions recorded
