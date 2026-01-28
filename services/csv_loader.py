import csv

def load(path):
    rows = []
    with open(path, encoding='utf-8-sig') as f:
        data = list(csv.reader(f))
        for r in data[10:]:
            if len(r) > 14 and r[10].strip():
                rows.append({
                    'cashmemo': r[7],
                    'name': r[10],
                    'address': ' '.join(r[11:14]),
                    'mobile': r[14]
                })
    return rows