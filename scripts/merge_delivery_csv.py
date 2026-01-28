from pathlib import Path
import sqlite3, csv, re
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
CSV_DIR = BASE / 'uploads' / 'csv'
DB_PATH = BASE / 'data' / 'erp.db'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def norm(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())

def find_col(headers, keys):
    for i, h in enumerate(headers):
        nh = norm(h)
        for k in keys:
            if k in nh:
                return i
    return None

def merge_all_csv():
    now = datetime.now().isoformat(timespec='seconds')
    total_i = total_g = 0

    for csv_file in CSV_DIR.glob('*.csv'):
        with open(csv_file, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)

            ix_cash = find_col(headers, ['CASH','MEMO','DOC','DOCUMENT'])
            ix_name = find_col(headers, ['CUSTOMER','CONSUMER','NAME'])
            ix_addr = find_col(headers, ['ADDRESS'])
            ix_mob  = find_col(headers, ['MOBILE','PHONE'])
            ix_qty  = find_col(headers, ['QTY','QUANTITY'])
            ix_type = find_col(headers, ['KG','CYLINDER','PRODUCT'])

            # 🔴 FINAL FALLBACK — BPCL REALITY
            if ix_cash is None:
                ix_cash = 0  # FIRST COLUMN IS CASH MEMO

            ins = ign = 0

            for r in reader:
                if len(r) == 0:
                    continue

                cashmemo = r[ix_cash].strip()
                if not cashmemo:
                    continue

                qty = 1
                if ix_qty is not None:
                    try:
                        qty = int(r[ix_qty])
                    except:
                        qty = 1

                cyl = '14.2'
                if ix_type is not None:
                    v = r[ix_type]
                    if '5' in v:
                        cyl = '5'
                    elif '19' in v or '18' in v:
                        cyl = '19'

                cur.execute("""
                INSERT OR IGNORE INTO delivery_orders
                (cashmemo, customer_name, address, mobile, cylinder_type, qty, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    cashmemo,
                    r[ix_name].strip() if ix_name is not None else '',
                    r[ix_addr].strip() if ix_addr is not None else '',
                    r[ix_mob].strip() if ix_mob is not None else '',
                    cyl,
                    qty,
                    now
                ))

                if cur.rowcount == 1:
                    ins += 1
                else:
                    ign += 1

            cur.execute(
                "INSERT INTO csv_upload_log (filename, uploaded_at) VALUES (?, ?)",
                (csv_file.name, now)
            )
            conn.commit()

            total_i += ins
            total_g += ign
            print(f'{csv_file.name} → Inserted: {ins}, Ignored: {ign}')

    print(f'ALL CSVs DONE | Inserted: {total_i}, Ignored: {total_g}')

if __name__ == '__main__':
    merge_all_csv()
