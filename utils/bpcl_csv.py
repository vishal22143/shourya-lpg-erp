import csv

def read_bpcl_scheduled_list(csv_path):
    deliveries = []
    header = None

    with open(csv_path, encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            # Detect real header row
            if row and 'SLNo' in row and 'ConsumerName' in row:
                header = row
                break

        if not header:
            raise Exception('BPCL header not found')

        idx = {name: header.index(name) for name in header}

        for row in reader:
            if not row or not row[idx['SLNo']].strip().isdigit():
                continue

            deliveries.append({
                'area': row[idx['AreaDescription']].strip(),
                'cashmemo': row[idx['CashMemoNo']].strip(),
                'consumer': row[idx['ConsumerName']].strip(),
                'address': ' '.join([
                    row[idx['Address1']].strip(),
                    row[idx['Address2']].strip(),
                    row[idx['Address3']].strip()
                ]),
                'mobile': row[idx['MobileNumber']].strip(),
                'status': 'Scheduled'
            })

    deliveries.sort(key=lambda x: (x['area'], x['consumer']))
    return deliveries
