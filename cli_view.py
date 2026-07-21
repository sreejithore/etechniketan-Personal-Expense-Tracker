import sys
from expense import Expense


def get_currency_symbol():
    try:
        if sys.stdout and sys.stdout.encoding:
            "₹".encode(sys.stdout.encoding)
            return "₹"
    except (UnicodeEncodeError, AttributeError, TypeError):
        pass
    return "Rs."


CURRENCY_SYMBOL = get_currency_symbol()


def print_header(title):
    border = "=" * 67
    print(f"\n{border}")
    print(f" {title.center(65)} ")
    print(f"{border}")


def display_expense_table(expenses):
    if not expenses:
        print("\n-------------------------------------------------------------------")
        print(" [INFO]: No expense records found in the ledger.")
        print("-------------------------------------------------------------------")
        return

    sym = get_currency_symbol()
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
        if len(exp.title) <= title_w:
            disp_title = exp.title
        else:
            disp_title = exp.title[: title_w - 3] + "..."

        if len(exp.category) <= cat_w:
            disp_cat = exp.category
        else:
            disp_cat = exp.category[: cat_w - 3] + "..."

        amt_str = f"{sym}{exp.amount:,.2f}"

        row_str = (
            f"| {str(exp.id).center(id_w)} | {exp.date.center(date_w)} | "
            f"{disp_cat.ljust(cat_w)} | {disp_title.ljust(title_w)} | {amt_str.rjust(amt_w)} |"
        )
        print(row_str)

    print(line_sep)
    print(f" Total Count: {len(expenses)} item(s)\n")


def display_telemetry_dashboard(metrics):
    sym = get_currency_symbol()
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
    if total_items == 1:
        record_label = "Record"
    else:
        record_label = "Records"
    print(f"Total Active Unique Tracked Items : {total_items} {record_label}")

    if total_items > 0:
        print(f"Average Expense Per Record       : {sym}{metrics['avg_expense']:,.2f}")
        if metrics.get("max_expense"):
            max_e = metrics["max_expense"]
            print(f"Highest Single Expense           : {sym}{max_e.amount:,.2f} ({max_e.title} - {max_e.category})")

    print("\n--- DYNAMIC CATEGORY-WISE BREAKDOWN ---")
    cat_map = metrics.get("category_breakdown", {})

    if not cat_map:
        print("No category data available.")
    else:
        max_cat_len = 14
        for cat in cat_map.keys():
            if len(cat) > max_cat_len:
                max_cat_len = len(cat)

        sorted_cats = sorted(cat_map.items(), key=lambda item: item[1], reverse=True)

        for cat_name, cat_amount in sorted_cats:
            if grand_total > 0:
                percentage = cat_amount / grand_total * 100
            else:
                percentage = 0

            bar_blocks = int(round(percentage / 10))
            if bar_blocks < 0:
                bar_blocks = 0
            if bar_blocks > 10:
                bar_blocks = 10

            if use_blocks:
                progress_bar = f"[{'█' * bar_blocks}{'░' * (10 - bar_blocks)}]"
            else:
                progress_bar = f"[{'#' * bar_blocks}{'-' * (10 - bar_blocks)}]"

            cat_label = cat_name.ljust(max_cat_len)
            amt_formatted = f"{sym}{cat_amount:,.2f}".rjust(12)
            print(f"{cat_label} : {amt_formatted}  {progress_bar} {percentage:5.1f}%")

    print("\n=====================================================================")


def display_single_expense(expense):
    sym = get_currency_symbol()
    print("\n+----------------------------------------------------+")
    print(f"|  EXPENSE DETAILS RECORD [ID: {expense.id}]".ljust(53) + "|")
    print("+----------------------------------------------------+")
    print(f"|  Title    : {expense.title}".ljust(53) + "|")
    print(f"|  Amount   : {sym}{expense.amount:,.2f}".ljust(53) + "|")
    print(f"|  Category : {expense.category}".ljust(53) + "|")
    print(f"|  Date     : {expense.date}".ljust(53) + "|")
    print("+----------------------------------------------------+")
