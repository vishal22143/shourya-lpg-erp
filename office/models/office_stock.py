class OfficeStock:
    def __init__(self, opening_full=0, opening_empty=0):
        self.opening_full = opening_full
        self.opening_empty = opening_empty
        self.transfers_in = []
        self.sales_out = []

    def transfer_in(self, full, empty):
        self.transfers_in.append({'full': full, 'empty': empty})

    def sale(self, full):
        self.sales_out.append(full)

    def closing_full(self):
        return self.opening_full + sum(t['full'] for t in self.transfers_in) - sum(self.sales_out)

    def closing_empty(self):
        return self.opening_empty + sum(t['empty'] for t in self.transfers_in) + sum(self.sales_out)
