"""
cli_view.py
Presentation logic and text formatting for the Personal Expense Tracker CLI application.
Handles structural tabular output formatting and visual Financial Telemetry Dashboards.
"""
import sys
from typing import List, Dict, Any
from expense import Expense


def get_currency_symbol() -> str:
    """Returns '₹' if terminal supports UTF-8, otherwise falls back to 'Rs.'."""
    try:
        if sys.stdout and sys.stdout.encoding:
            "₹".encode(sys.stdout.encoding)
            return "₹"
    except (UnicodeEncodeError, AttributeError, TypeError):
        pass
    return "Rs."


CURRENCY_SYMBOL = get_currency_symbol()


def print_header(title: str) -> None:
    """Prints a styled header line."""
    border = "=" * 67
    print(f"\n{border}")
    print(f" {title.center(65)} ")
    print(f"{border}")


def display_expense_table(expenses: List[Expense]) -> None:
    """
    Displays a collection of Expense objects formatted cleanly in a structural tabular format.
    """
    if not expenses:
        print("\n-------------------------------------------------------------------")
        print(" [INFO]: No expense records found in the ledger.")
        print("-------------------------------------------------------------------")
        return

    # Dynamic symbol selection
    sym = get_currency_symbol()

    # Table layout definitions
    id_w = 6
    date_w = 12
    cat_w = 15
    title_w = 22
    amt_w = 12

    line_sep = f"+{'-'*(id_w+2)}+{'-'*(date_w+2)}+{'-'*(cat_w+2)}+{'-'*(title_w+2)}+{'-'*(amt_w+2)}+"

    print("\n" + line_sep)
    header_str = (
        f"| {'ID'.center(id_w)} | {'Date'.center(date_w)} | "
        f"{'Category'.center(cat_w)} | {'Title'.center(title_w)} | {f'Amount ({sym})'.center(amt_w)} |"
    )
    print(header_str)
    print(line_sep)

    for exp in expenses:
        # Truncate title if it exceeds column width
        disp_title = exp.title if len(exp.title) <= title_w else exp.title[: title_w - 3] + "..."
        disp_cat = exp.category if len(exp.category) <= cat_w else exp.category[: cat_w - 3] + "..."
        amt_str = f"{sym}{exp.amount:,.2f}"

        row_str = (
            f"| {str(exp.id).center(id_w)} | {exp.date.center(date_w)} | "
            f"{disp_cat.ljust(cat_w)} | {disp_title.ljust(title_w)} | {amt_str.rjust(amt_w)} |"
        )
        print(row_str)

    print(line_sep)
    print(f" Total Count: {len(expenses)} item(s)\n")


def display_telemetry_dashboard(metrics: Dict[str, Any]) -> None:
    """
    Renders the real-time Financial Telemetry Dashboard including category-wise spending
    breakdowns, live grand totals, and text bar charts.
    """
    sym = get_currency_symbol()

    # Check progress bar block character encoding support
    use_blocks = True
    try:
        if sys.stdout and sys.stdout.encoding:
            "█░".encode(sys.stdout.encoding)
    except (UnicodeEncodeError, AttributeError, TypeError):
        use_blocks = False

    print("\n=================== FINANCIAL TELEMETRY DASHBOARD ===================")
    print("\n--- COMPREHENSIVE STATUS SUMMARY ---")
    grand_total = metrics["grand_total"]
    total_items = metrics["total_items"]
    print(f"Grand Combined Total Expenditures : {sym}{grand_total:,.2f}")
    print(f"Total Active Unique Tracked Items : {total_items} Record{'s' if total_items != 1 else ''}")

    if total_items > 0:
        print(f"Average Expense Per Record       : {sym}{metrics['avg_expense']:,.2f}")
        if metrics.get("max_expense"):
            max_e = metrics["max_expense"]
            print(f"Highest Single Expense           : {sym}{max_e.amount:,.2f} ({max_e.title} - {max_e.category})")

    print("\n--- DYNAMIC CATEGORY-WISE BREAKDOWN ---")
    cat_map: Dict[str, float] = metrics.get("category_breakdown", {})

    if not cat_map:
        print("No category data available.")
    else:
        # Determine maximum key length for alignment
        max_cat_len = max(len(cat) for cat in cat_map.keys())
        max_cat_len = max(max_cat_len, 14)

        # Sort categories by spending descending
        sorted_cats = sorted(cat_map.items(), key=lambda item: item[1], reverse=True)

        for cat_name, cat_amount in sorted_cats:
            percentage = (cat_amount / grand_total * 100) if grand_total > 0 else 0
            
            # Generate visual text progress bar (10 blocks long)
            bar_blocks = int(round(percentage / 10))
            bar_blocks = max(0, min(10, bar_blocks))
            if use_blocks:
                progress_bar = f"[{'█' * bar_blocks}{'░' * (10 - bar_blocks)}]"
            else:
                progress_bar = f"[{'#' * bar_blocks}{'-' * (10 - bar_blocks)}]"

            cat_label = cat_name.ljust(max_cat_len)
            amt_formatted = f"{sym}{cat_amount:,.2f}".rjust(12)
            print(f"{cat_label} : {amt_formatted}  {progress_bar} {percentage:5.1f}%")

    print("\n=====================================================================")


def display_single_expense(expense: Expense) -> None:
    """Displays a single expense record formatted in a card box layout."""
    sym = get_currency_symbol()
    print("\n+----------------------------------------------------+")
    print(f"|  EXPENSE DETAILS RECORD [ID: {expense.id}]".ljust(53) + "|")
    print("+----------------------------------------------------+")
    print(f"|  Title    : {expense.title}".ljust(53) + "|")
    print(f"|  Amount   : {sym}{expense.amount:,.2f}".ljust(53) + "|")
    print(f"|  Category : {expense.category}".ljust(53) + "|")
    print(f"|  Date     : {expense.date}".ljust(53) + "|")
    print("+----------------------------------------------------+")
