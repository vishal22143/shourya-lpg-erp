class OfficeExpense:
    def __init__(self):
        self.expenses = []

    def add(self, category, amount, note=None):
        self.expenses.append({
            'category': category,
            'amount': amount,
            'note': note
        })

    def total(self):
        return sum(e['amount'] for e in self.expenses)
