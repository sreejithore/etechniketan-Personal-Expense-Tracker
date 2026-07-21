from datetime import datetime


def prompt_amount(prompt_msg="Enter Expense Amount: "):
    while True:
        raw_val = input(prompt_msg).strip()
        try:
            val = float(raw_val)
            if val <= 0:
                print("--> [ERROR]: Amount must be a positive number greater than zero. Please try again.")
                continue
            return round(val, 2)
        except ValueError:
            print("--> [ERROR]: Invalid monetary value. Please enter a valid numerical decimal amount.")


def prompt_date(prompt_msg="Enter Expense Date (DD-MM-YYYY) or leave blank for today: "):
    while True:
        raw_val = input(prompt_msg).strip()
        if not raw_val:
            today_str = datetime.now().strftime("%d-%m-%Y")
            print(f"--> [SYSTEM]: Blank detected. Auto-assigned current timestamp date: {today_str}")
            return today_str, True
        try:
            parsed_date = datetime.strptime(raw_val, "%d-%m-%Y")
            return parsed_date.strftime("%d-%m-%Y"), False
        except ValueError:
            print("--> [ERROR]: Invalid date configuration! Date must strictly follow the format DD-MM-YYYY (e.g. 17-07-2026).")


def prompt_non_empty(prompt_msg, field_name="Input"):
    while True:
        val = input(prompt_msg).strip()
        if val:
            return val
        print(f"--> [ERROR]: {field_name} cannot be blank. Please enter a valid value.")


def prompt_category(prompt_msg="Enter Expense Category: "):
    category = prompt_non_empty(prompt_msg, "Category")
    return category.title()


def prompt_integer(prompt_msg, min_val=None, max_val=None):
    while True:
        raw_val = input(prompt_msg).strip()
        try:
            val = int(raw_val)
            if min_val is not None and val < min_val:
                print(f"--> [ERROR]: Value cannot be less than {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"--> [ERROR]: Value cannot be greater than {max_val}.")
                continue
            return val
        except ValueError:
            print("--> [ERROR]: Invalid integer input. Please enter a valid numeric integer.")
