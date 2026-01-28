import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "erp.db"

def conn():
    return sqlite3.connect(DB)

def init_db():
    c = conn()
    cur = c.cursor()

    # Event table (operational input)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS godown_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        event_type TEXT,
        filled INTEGER,
        empty INTEGER,
        defective INTEGER,
        remark TEXT
    )
    """)

    # Derived strict ledger (append-only)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS godown_ledger(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        opening_filled INTEGER,
        inward_filled INTEGER,
        outward_filled INTEGER,
        closing_filled INTEGER
    )
    """)

    c.commit()
    c.close()
# backward compatibility
def get_conn():
    return conn()

