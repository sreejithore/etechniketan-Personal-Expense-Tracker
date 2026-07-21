"""
validators.py
Robust input validation helpers for the Personal Expense Tracker CLI application.
Uses try-except blocks to catch invalid formatting and enforce date formatting rules.
"""

from datetime import datetime
from typing import Tuple


def prompt_amount(prompt_msg: str = "Enter Expense Amount: ") -> float:
    """
    Prompts the user for a monetary amount, using a try-except block to trap
    non-numeric or non-positive inputs gracefully.
    """
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


def prompt_date(prompt_msg: str = "Enter Expense Date (DD-MM-YYYY) or leave blank for today: ") -> Tuple[str, bool]:
    """
    Prompts the user for a date string in strict DD-MM-YYYY format.
    If left blank, auto-assigns current date.
    Returns tuple: (date_string, is_auto_generated)
    """
    while True:
        raw_val = input(prompt_msg).strip()
        if not raw_val:
            today_str = datetime.now().strftime("%d-%m-%Y")
            print(f"--> [SYSTEM]: Blank detected. Auto-assigned current timestamp date: {today_str}")
            return today_str, True
        
        try:
            parsed_date = datetime.strptime(raw_val, "%d-%m-%Y")
            # Return standardized DD-MM-YYYY format string
            return parsed_date.strftime("%d-%m-%Y"), False
        except ValueError:
            print("--> [ERROR]: Invalid date configuration! Date must strictly follow the format DD-MM-YYYY (e.g. 17-07-2026).")


def prompt_non_empty(prompt_msg: str, field_name: str = "Input") -> str:
    """Prompts for a non-empty string input."""
    while True:
        val = input(prompt_msg).strip()
        if val:
            return val
        print(f"--> [ERROR]: {field_name} cannot be blank. Please enter a valid value.")


def prompt_category(prompt_msg: str = "Enter Expense Category: ") -> str:
    """Prompts for an expense category and formats it to Title Case."""
    category = prompt_non_empty(prompt_msg, "Category")
    return category.title()


def prompt_integer(prompt_msg: str, min_val: int = None, max_val: int = None) -> int:
    """
    Prompts for an integer value (e.g., ID or menu option) with optional min/max bounds.
    Traps non-integer errors using try-except.
    """
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
