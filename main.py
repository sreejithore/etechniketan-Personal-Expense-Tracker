import sys
from datetime import datetime
from tracker import ExpenseTracker
from validators import (
    prompt_amount,
    prompt_date,
    prompt_category,
    prompt_non_empty,
    prompt_integer,
)
from cli_view import (
    print_header,
    display_expense_table,
    display_telemetry_dashboard,
    display_single_expense,
)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def display_menu():
    print("\n=== PERSONAL EXPENSE TRACKER ===")
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. Search Expense")
    print("4. Update Expense")
    print("5. Delete Expense")
    print("6. View Summary Metrics")
    print("7. Exit & Save Data")


def handle_add_expense(tracker):
    print("\n--- ADD NEW EXPENSE ---")
    title = prompt_non_empty("Enter Expense Title: ", "Title")
    amount = prompt_amount("Enter Expense Amount: ")
    category = prompt_category("Enter Expense Category: ")
    date_str, _ = prompt_date("Enter Expense Date (DD-MM-YYYY) or leave blank for today: ")
    new_expense = tracker.add_expense(title, amount, category, date_str)
    print(f"\nSuccess: New record securely appended! [Generated ID: {new_expense.id}]")


def handle_view_expenses(tracker):
    print_header("EXPENSE LEDGER OVERVIEW")
    expenses = tracker.get_all_expenses()
    display_expense_table(expenses)


def handle_search_expense(tracker):
    print("\n--- SEARCH EXPENSE RECORD ---")
    expense_id = prompt_integer("Enter Expense ID to search: ", min_val=1)
    expense = tracker.search_expense(expense_id)
    if expense:
        display_single_expense(expense)
    else:
        print(f"\n--> [ERROR]: Expense with ID {expense_id} not found in tracking ledger.")


def handle_update_expense(tracker):
    print("\n--- UPDATE EXISTING EXPENSE ---")
    expense_id = prompt_integer("Enter Expense ID to update: ", min_val=1)
    expense = tracker.search_expense(expense_id)
    if not expense:
        print(f"\n--> [ERROR]: Expense with ID {expense_id} not found in tracking ledger.")
        return
    print("\nCurrent Record Details:")
    display_single_expense(expense)
    print("\nLeave input blank and hit Enter to keep the existing value.")

    new_title_raw = input(f"Enter New Title [{expense.title}]: ").strip()
    if new_title_raw:
        new_title = new_title_raw
    else:
        new_title = None

    new_amount = None
    while True:
        raw_amt = input(f"Enter New Amount [{expense.amount:.2f}]: ").strip()
        if not raw_amt:
            break
        try:
            val = float(raw_amt)
            if val <= 0:
                print("--> [ERROR]: Amount must be a positive number greater than zero.")
                continue
            new_amount = round(val, 2)
            break
        except ValueError:
            print("--> [ERROR]: Invalid monetary value. Please enter a valid numerical decimal amount.")

    new_cat_raw = input(f"Enter New Category [{expense.category}]: ").strip()
    if new_cat_raw:
        new_cat = new_cat_raw.title()
    else:
        new_cat = None

    new_date = None
    while True:
        raw_dt = input(f"Enter New Date DD-MM-YYYY [{expense.date}]: ").strip()
        if not raw_dt:
            break
        try:
            parsed = datetime.strptime(raw_dt, "%d-%m-%Y")
            new_date = parsed.strftime("%d-%m-%Y")
            break
        except ValueError:
            print("--> [ERROR]: Invalid date configuration! Date must strictly follow the format DD-MM-YYYY.")

    updated = tracker.update_expense(
        expense_id=expense_id,
        title=new_title,
        amount=new_amount,
        category=new_cat,
        date_str=new_date,
    )
    if updated:
        print(f"\nSuccess: Record [ID: {expense_id}] updated successfully in memory!")
        display_single_expense(tracker.search_expense(expense_id))


def handle_delete_expense(tracker):
    print("\n--- DELETE EXPENSE RECORD ---")
    expense_id = prompt_integer("Enter Expense ID to delete: ", min_val=1)
    expense = tracker.search_expense(expense_id)
    if not expense:
        print(f"\n--> [ERROR]: Expense with ID {expense_id} not found in tracking ledger.")
        return
    display_single_expense(expense)
    confirm = input("\nAre you sure you want to permanently delete this expense? (y/N): ").strip().lower()
    if confirm == "y" or confirm == "yes":
        if tracker.delete_expense(expense_id):
            print(f"\nSuccess: Expense record [ID: {expense_id}] removed from tracking ledger.")
        else:
            print(f"\n--> [ERROR]: Could not delete expense record [ID: {expense_id}].")
    else:
        print("\n[SYSTEM]: Deletion canceled.")


def handle_view_summary(tracker):
    metrics = tracker.get_summary_metrics()
    display_telemetry_dashboard(metrics)


def main():
    tracker = ExpenseTracker(filepath="expenses.csv")
    loaded, count = tracker.load_from_csv()
    if loaded:
        print(f"\n[SYSTEM]: Successfully loaded {count} expense record(s) from 'expenses.csv'.")
    else:
        print("\n[SYSTEM]: Starting new expense tracking session.")

    while True:
        display_menu()
        choice = prompt_integer("Choose option (1-7): ", min_val=1, max_val=7)

        if choice == 1:
            handle_add_expense(tracker)
        elif choice == 2:
            handle_view_expenses(tracker)
        elif choice == 3:
            handle_search_expense(tracker)
        elif choice == 4:
            handle_update_expense(tracker)
        elif choice == 5:
            handle_delete_expense(tracker)
        elif choice == 6:
            handle_view_summary(tracker)
        elif choice == 7:
            print("\n[SYSTEM]: Saving updates back to disk...")
            if tracker.save_to_csv():
                print("Success: Operational updates saved to 'expenses.csv'.")
            print("[SYSTEM]: Exiting Personal Expense Tracker. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
