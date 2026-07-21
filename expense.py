"""
expense.py
Model class representing an individual expense entry in the Personal Expense Tracker.
"""

from typing import Dict, Any


class Expense:
    """
    Represents a single expense record.
    
    Attributes:
        id (int): Unique identifier auto-assigned to the expense.
        title (str): Brief descriptive name of the expense.
        amount (float): Monetary value of the expense.
        category (str): Category grouping (e.g., Food, Rent, Transport).
        date (str): Date of expenditure in DD-MM-YYYY string format.
    """

    def __init__(self, expense_id: int, title: str, amount: float, category: str, date_str: str):
        self.id = int(expense_id)
        self.title = str(title).strip()
        self.amount = round(float(amount), 2)
        self.category = str(category).strip().title()
        self.date = str(date_str).strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convert expense instance to a dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "amount": f"{self.amount:.2f}",
            "category": self.category,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Construct an Expense instance from a dictionary record."""
        return cls(
            expense_id=int(data["id"]),
            title=data["title"],
            amount=float(data["amount"]),
            category=data["category"],
            date_str=data["date"],
        )

    def __str__(self) -> str:
        return f"Expense[ID={self.id}, Title='{self.title}', Amount=₹{self.amount:.2f}, Category='{self.category}', Date='{self.date}']"

    def __repr__(self) -> str:
        return f"Expense({self.id}, '{self.title}', {self.amount}, '{self.category}', '{self.date}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expense):
            return False
        return (
            self.id == other.id
            and self.title == other.title
            and abs(self.amount - other.amount) < 1e-6
            and self.category == other.category
            and self.date == other.date
        )
