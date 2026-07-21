class Expense:
    def __init__(self, expense_id, title, amount, category, date_str):
        self.id = int(expense_id)
        self.title = str(title).strip()
        self.amount = round(float(amount), 2)
        self.category = str(category).strip().title()
        self.date = str(date_str).strip()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": f"{self.amount:.2f}",
            "category": self.category,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            expense_id=data["id"],
            title=data["title"],
            amount=data["amount"],
            category=data["category"],
            date_str=data["date"]
        )

    def __str__(self):
        return f"Expense[ID={self.id}, Title='{self.title}', Amount=₹{self.amount:.2f}, Category='{self.category}', Date='{self.date}']"

    def __repr__(self):
        return f"Expense({self.id}, '{self.title}', {self.amount}, '{self.category}', '{self.date}')"

    def __eq__(self, other):
        if not isinstance(other, Expense):
            return False
        return (
            self.id == other.id and
            self.title == other.title and
            abs(self.amount - other.amount) < 1e-6 and
            self.category == other.category and
            self.date == other.date
        )
