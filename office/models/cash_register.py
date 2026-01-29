class CashRegister:
    def __init__(self):
        self.denominations = {
            500: 0,
            200: 0,
            100: 0,
            50: 0,
            20: 0,
            10: 0,
            1: 0
        }

    def set_count(self, denom, qty):
        if denom in self.denominations:
            self.denominations[denom] = qty

    def total_cash(self):
        return sum(d * q for d, q in self.denominations.items())

    def validate_against(self, expected_amount):
        return self.total_cash() == expected_amount
