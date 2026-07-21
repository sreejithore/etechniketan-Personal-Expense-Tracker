"""
tracker.py
ExpenseTracker manager class serving as the system brain for the Personal Expense Tracker.
Manages the in-memory array of Expense objects, unique ID allocation, CRUD logic,
financial summary metrics, and CSV file persistence.
"""

import csv
import os
from typing import List, Optional, Dict, Any, Tuple
from expense import Expense


class ExpenseTracker:
    """
    Manager class for controlling expense operations and disk persistence.
    """

    def __init__(self, filepath: str = "expenses.csv"):
        self.filepath = filepath
        self.expenses: List[Expense] = []
        self.next_id: int = 101

    def _update_next_id(self) -> None:
        """Calculates the next available unique ID."""
        if not self.expenses:
            self.next_id = 101
        else:
            self.next_id = max(e.id for e in self.expenses) + 1

    def add_expense(self, title: str, amount: float, category: str, date_str: str) -> Expense:
        """
        Creates and stores a new Expense object with an auto-generated unique ID.
        """
        self._update_next_id()
        new_id = self.next_id
        expense = Expense(expense_id=new_id, title=title, amount=amount, category=category, date_str=date_str)
        self.expenses.append(expense)
        self._update_next_id()
        return expense

    def get_all_expenses(self) -> List[Expense]:
        """Returns the list of all tracked expenses."""
        return self.expenses

    def search_expense(self, expense_id: int) -> Optional[Expense]:
        """Searches and retrieves an individual expense by unique ID."""
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def update_expense(
        self,
        expense_id: int,
        title: Optional[str] = None,
        amount: Optional[float] = None,
        category: Optional[str] = None,
        date_str: Optional[str] = None,
    ) -> bool:
        """
        Dynamically updates fields for an existing expense entry in memory.
        Returns True if successful, False if expense ID not found.
        """
        expense = self.search_expense(expense_id)
        if not expense:
            return False

        if title is not None and title.strip():
            expense.title = title.strip()
        if amount is not None:
            expense.amount = round(float(amount), 2)
        if category is not None and category.strip():
            expense.category = category.strip().title()
        if date_str is not None and date_str.strip():
            expense.date = date_str.strip()

        return True

    def delete_expense(self, expense_id: int) -> bool:
        """
        Removes an expense record by unique ID safely from the tracking ledger.
        Returns True if deleted, False if not found.
        """
        expense = self.search_expense(expense_id)
        if expense:
            self.expenses.remove(expense)
            self._update_next_id()
            return True
        return False

    def get_summary_metrics(self) -> Dict[str, Any]:
        """
        Generates real-time financial telemetry summaries and category-wise spending totals.
        """
        total_items = len(self.expenses)
        if total_items == 0:
            return {
                "grand_total": 0.0,
                "total_items": 0,
                "category_breakdown": {},
                "avg_expense": 0.0,
                "max_expense": None,
                "min_expense": None,
            }

        grand_total = sum(e.amount for e in self.expenses)
        avg_expense = grand_total / total_items

        category_breakdown: Dict[str, float] = {}
        for e in self.expenses:
            category_breakdown[e.category] = category_breakdown.get(e.category, 0.0) + e.amount

        max_exp = max(self.expenses, key=lambda e: e.amount)
        min_exp = min(self.expenses, key=lambda e: e.amount)

        return {
            "grand_total": round(grand_total, 2),
            "total_items": total_items,
            "category_breakdown": category_breakdown,
            "avg_expense": round(avg_expense, 2),
            "max_expense": max_exp,
            "min_expense": min_exp,
        }

    def save_to_csv(self, target_filepath: Optional[str] = None) -> bool:
        """
        Persists all in-memory records to a CSV storage file.
        """
        filepath = target_filepath or self.filepath
        try:
            fieldnames = ["id", "title", "amount", "category", "date"]
            with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow(expense.to_dict())
            return True
        except Exception as e:
            print(f"--> [ERROR]: Persistence save error: {e}")
            return False

    def load_from_csv(self, target_filepath: Optional[str] = None) -> Tuple[bool, int]:
        """
        Loads expense records from disk into memory on startup.
        Returns tuple: (success_status, number_of_records_loaded)
        """
        filepath = target_filepath or self.filepath
        if not os.path.exists(filepath):
            return False, 0

        loaded_expenses = []
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row:
                        loaded_expenses.append(Expense.from_dict(row))
            self.expenses = loaded_expenses
            self._update_next_id()
            return True, len(loaded_expenses)
        except Exception as e:
            print(f"--> [WARNING]: Could not load data file ({e}). Starting with clean ledger.")
            return False, 0
