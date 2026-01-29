from datetime import date

class OfficeSale:
    def __init__(self, sale_date=None):
        self.sale_date = sale_date or date.today()
        self.items = []

    def add_item(self, item_type, qty, payment_mode, cash_amount=0, note=None):
        self.items.append({
            'item_type': item_type,
            'qty': qty,
            'payment_mode': payment_mode,
            'cash_amount': cash_amount,
            'note': note
        })

    def total_cash(self):
        return sum(i['cash_amount'] for i in self.items)

    def total_qty(self):
        return sum(i['qty'] for i in self.items)
