import csv
import os
from expense import Expense


class ExpenseTracker:
    def __init__(self, filepath="expenses.csv"):
        self.filepath = filepath
        self.expenses = []
        self.next_id = 101

    def _update_next_id(self):
        if not self.expenses:
            self.next_id = 101
        else:
            highest_id = 100
            for expense in self.expenses:
                if expense.id > highest_id:
                    highest_id = expense.id
            self.next_id = highest_id + 1

    def add_expense(self, title, amount, category, date_str):
        self._update_next_id()
        expense = Expense(self.next_id, title, amount, category, date_str)
        self.expenses.append(expense)
        self._update_next_id()
        return expense

    def get_all_expenses(self):
        return self.expenses

    def search_expense(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def update_expense(self, expense_id, title=None, amount=None, category=None, date_str=None):
        expense = self.search_expense(expense_id)
        if not expense:
            return False
        if title is not None and str(title).strip():
            expense.title = str(title).strip()
        if amount is not None:
            expense.amount = round(float(amount), 2)
        if category is not None and str(category).strip():
            expense.category = str(category).strip().title()
        if date_str is not None and str(date_str).strip():
            expense.date = str(date_str).strip()
        return True

    def delete_expense(self, expense_id):
        expense = self.search_expense(expense_id)
        if expense:
            self.expenses.remove(expense)
            self._update_next_id()
            return True
        return False

    def get_summary_metrics(self):
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

        grand_total = 0.0
        for exp in self.expenses:
            grand_total += exp.amount
        avg_expense = grand_total / total_items

        category_breakdown = {}
        for exp in self.expenses:
            cat = exp.category
            if cat in category_breakdown:
                category_breakdown[cat] += exp.amount
            else:
                category_breakdown[cat] = exp.amount

        max_exp = self.expenses[0]
        min_exp = self.expenses[0]
        for exp in self.expenses:
            if exp.amount > max_exp.amount:
                max_exp = exp
            if exp.amount < min_exp.amount:
                min_exp = exp

        return {
            "grand_total": round(grand_total, 2),
            "total_items": total_items,
            "category_breakdown": category_breakdown,
            "avg_expense": round(avg_expense, 2),
            "max_expense": max_exp,
            "min_expense": min_exp,
        }

    def save_to_csv(self, target_filepath=None):
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

    def load_from_csv(self, target_filepath=None):
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
