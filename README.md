# Personal Expense Tracker CLI Application

A menu-driven command-line Personal Expense Tracker written in **Python 3.x**. Designed with Object-Oriented Programming (OOP) principles, CSV file persistence, input validation traps, automatic date fallbacks, and visual financial telemetry dashboards.

---

## Key Features

- **No External Dependencies**: Built entirely using Python's standard library (`csv`, `datetime`, `os`, `sys`).
- **Auto-Generated Unique IDs**: Every new transaction gets a unique numerical ID starting at `101`.
- **Flexible & Validated Inputs**:
  - Traps non-numeric and non-positive monetary inputs.
  - Enforces strict `DD-MM-YYYY` date formats.
  - Pressing **Enter** on the date prompt automatically assigns today's timestamp.
  - Category names are automatically formatted into Title Case.
- **Tabular Ledger Display**: Renders clean ASCII tables with dynamically detected currency symbols (`₹` for UTF-8 terminals or fallback `Rs.`).
- **Financial Telemetry Dashboard**: Real-time spending summary including:
  - Grand combined expenditures total.
  - Total active items count & average expense per record.
  - Highest single expense highlight.
  - Dynamic category-wise spending breakdown with visual progress bar charts (`[██████░░░░]`) and percentage calculations.
- **CSV Disk Persistence**: Automatically loads data from `expenses.csv` on startup and saves all changes when exiting.

---

## File Architecture

| File | Description |
| :--- | :--- |
| **`main.py`** | Main CLI menu loop connecting user choices to controller functions. |
| **`expense.py`** | `Expense` class representing single transaction records (`id`, `title`, `amount`, `category`, `date`). |
| **`tracker.py`** | `ExpenseTracker` manager class controlling in-memory lists, auto-IDs, CRUD operations, telemetry summaries, and CSV storage. |
| **`validators.py`** | Input validation functions using `try-except` blocks for positive numbers, strict dates, and valid integers. |
| **`cli_view.py`** | Presentation layer formatting ASCII tables, telemetry dashboard charts, and expense card views. |
| **`expenses.csv`** | Persistent CSV database file created automatically on disk. |

---

## Requirements

- **Python 3.x** installed on your system.
- Standard terminal / command prompt (PowerShell, CMD, Bash, zsh).

---

## How to Run

Navigate to the project directory in your terminal and run:

```bash
python main.py
```

---

## User Guide & CLI Menu Workflow

When you launch `main.py`, you will be presented with the primary menu:

```text
=== PERSONAL EXPENSE TRACKER ===
1. Add New Expense
2. View All Expenses
3. Search Expense
4. Update Expense
5. Delete Expense
6. View Summary Metrics
7. Exit & Save Data
```

### Option 1: Add New Expense
1. Enter the title (e.g., `Team Lunch`).
2. Enter the amount (e.g., `192.50`). Must be a positive number greater than 0.
3. Enter the category (e.g., `food` -> auto-formatted to `Food`).
4. Enter date in `DD-MM-YYYY` format or press **Enter** to auto-assign today's date.

### Option 2: View All Expenses
Displays all recorded transactions formatted cleanly in a table:

```text
===================================================================
                      EXPENSE LEDGER OVERVIEW
===================================================================

+--------+--------------+-----------------+------------------------+--------------+
|   ID   |     Date     |     Category    |         Title          |  Amount (₹)  |
+--------+--------------+-----------------+------------------------+--------------+
|  101   |  17-07-2026  | Food            | Team Lunch Meeting     |      ₹192.50 |
|  102   |  01-07-2026  | Rent            | Monthly House Rent     |    ₹1,500.00 |
|  105   |  21-07-2026  | Travel          | Travelling             |      ₹800.00 |
+--------+--------------+-----------------+------------------------+--------------+
 Total Count: 3 item(s)
```

### Option 3: Search Expense
Enter an Expense ID (e.g., `105`) to inspect a single record in card layout:

```text
+----------------------------------------------------+
|  EXPENSE DETAILS RECORD [ID: 105]                  |
+----------------------------------------------------+
|  Title    : Travelling                             |
|  Amount   : ₹800.00                                |
|  Category : Travel                                 |
|  Date     : 21-07-2026                             |
+----------------------------------------------------+
```

### Option 4: Update Expense
Enter the ID of the expense you wish to update. Press **Enter** on any prompt to retain the current value, or type a new value to update title, amount, category, or date.

### Option 5: Delete Expense
Enter the Expense ID. The system displays record details and asks for confirmation (`y/N`) before permanently removing it.

### Option 6: View Summary Metrics & Financial Dashboard
Renders real-time telemetry metrics and visual progress bar charts:

```text
=================== FINANCIAL TELEMETRY DASHBOARD ===================

--- COMPREHENSIVE STATUS SUMMARY ---
Grand Combined Total Expenditures : ₹2,492.50
Total Active Unique Tracked Items : 3 Records
Average Expense Per Record       : ₹830.83
Highest Single Expense           : ₹1,500.00 (Monthly House Rent - Rent)

--- DYNAMIC CATEGORY-WISE BREAKDOWN ---
Rent           :    ₹1,500.00  [██████░░░░]  60.2%
Travel         :      ₹800.00  [███░░░░░░░]  32.1%
Food           :      ₹192.50  [█░░░░░░░░░]   7.7%

=====================================================================
```

### Option 7: Exit & Save Data
Saves all memory changes back to `expenses.csv` and closes the program safely.

---

## CSV File Format (`expenses.csv`)

Expenses are saved in standard CSV format:

```csv
id,title,amount,category,date
101,Team Lunch Meeting,192.50,Food,17-07-2026
102,Monthly House Rent,1500.00,Rent,01-07-2026
105,Travelling,800.00,Travel,21-07-2026
```

---

## Validation & Error Handling

- **Non-Numeric/Zero Amount**: Rejects negative numbers, `0`, or text inputs with explicit error messages.
- **Invalid Date**: Rejects invalid dates (e.g., `31-02-2026` or wrong separator `/`) and requests strict `DD-MM-YYYY` input.
- **Empty Title/Category**: Rejects blank title inputs.
- **Non-Existent ID**: Safely handles invalid ID lookups for search, update, and delete actions without crashing.
