#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Database - Shourya Bharatgas ERP"""
import sqlite3, hashlib, os, datetime

DB = os.path.join(os.path.dirname(__file__), "erp.db")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def hpin(p): return hashlib.sha256(str(p).encode()).hexdigest()
def today(): return datetime.date.today().isoformat()
def now_ts(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def this_month(): return datetime.date.today().strftime("%Y-%m")

BDA_MAP = {
    1:{"village":"Kondigre","owner":"Sarika Waghmode","mobile":"9561242972","type":"rural"},
    2:{"village":"Nimshirgav","owner":"Kumar Thomake","mobile":"9673824646","type":"rural"},
    3:{"village":"Nimshirgav (Lakhane)","owner":"Lakhane","mobile":"7588262265","type":"rural"},
    4:{"village":"Danoli","owner":"Manoj","mobile":"9970731436","type":"rural"},
    5:{"village":"Kothali","owner":"Yadav","mobile":"9405744020","type":"rural"},
    6:{"village":"Kavatesar","owner":"Sudhakar Patil","mobile":"9822180498","type":"rural"},
    7:{"village":"Shirol","owner":"Vikrant Kamble","mobile":"7028502299","type":"rural"},
    8:{"village":"Chipri Beghar","owner":"Rajesh Awale","mobile":"8007183197","type":"rural"},
}

VEHICLES = {
    1:{"name":"Tata 407","cap":55,"extra":10},
    2:{"name":"Mega XL","cap":35,"extra":8},
    3:{"name":"Hatti","cap":20,"extra":8},
    4:{"name":"Ape","cap":20,"extra":8},
    5:{"name":"New Hatti","cap":40,"extra":5},
}

WAGE_URBAN = 8.0
WAGE_RURAL = 7.0
WAGE_PAIR  = 200.0

def init_db():
    c = get_db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);

    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, mobile TEXT UNIQUE NOT NULL, alt_mobile TEXT,
        role TEXT NOT NULL, designation TEXT,
        pin_hash TEXT NOT NULL, must_change_pin INTEGER DEFAULT 1,
        wage_type TEXT DEFAULT 'na', salary_fixed REAL DEFAULT 0,
        bda_id INTEGER, vehicle_id INTEGER,
        is_active INTEGER DEFAULT 1, is_temp INTEGER DEFAULT 0,
        temp_expires TEXT,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS erp_days(
        date TEXT PRIMARY KEY, is_locked INTEGER DEFAULT 0,
        locked_at TEXT, locked_by INTEGER, morning_locked INTEGER DEFAULT 0,
        bpcl_day_end_done INTEGER DEFAULT 0, notes TEXT
    );

    CREATE TABLE IF NOT EXISTS blocked_consumers(
        consumer_number TEXT PRIMARY KEY, consumer_name TEXT,
        block_reason TEXT, area_id TEXT
    );

    CREATE TABLE IF NOT EXISTS consumer_master(
        consumer_number TEXT PRIMARY KEY, consumer_name TEXT,
        address TEXT, mobile TEXT, area_id TEXT, area_desc TEXT,
        location_type TEXT DEFAULT 'urban', bda_id INTEGER,
        sv_number TEXT, blue_book_number TEXT, dpr_count INTEGER DEFAULT 0,
        suraksha_tube INTEGER DEFAULT 0, last_deliv_date TEXT,
        lat REAL, lng REAL, landmark TEXT, gps_saved INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS delivery_pool(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL, cashmemo_no TEXT UNIQUE NOT NULL,
        consumer_number TEXT, consumer_name TEXT,
        address TEXT, mobile TEXT, area_id TEXT, area_name TEXT,
        location_type TEXT DEFAULT 'urban', bda_id INTEGER,
        product_code TEXT DEFAULT '5350',
        lat REAL, lng REAL, gps_saved INTEGER DEFAULT 0, landmark TEXT,
        status TEXT DEFAULT 'pending',
        otp TEXT, otp_saved_at TEXT,
        trip_id INTEGER, delivered_by INTEGER,
        payment_mode TEXT, cash_amount REAL DEFAULT 0,
        online_amount REAL DEFAULT 0, cylinder_price REAL DEFAULT 856,
        is_spot INTEGER DEFAULT 0, spot_name TEXT, spot_mobile TEXT,
        is_blocked INTEGER DEFAULT 0, block_reason TEXT,
        notes TEXT, delivered_at TEXT,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS trips(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL, delivery_man_id INTEGER NOT NULL,
        helper_id INTEGER, vehicle_id INTEGER, trip_number INTEGER DEFAULT 1,
        status TEXT DEFAULT 'open',
        opening_filled INTEGER DEFAULT 0, opening_empty INTEGER DEFAULT 0,
        total_delivered INTEGER DEFAULT 0, total_spot INTEGER DEFAULT 0,
        empties_collected INTEGER DEFAULT 0,
        closing_filled INTEGER DEFAULT 0, closing_empty INTEGER DEFAULT 0,
        cash_collected REAL DEFAULT 0, online_collected REAL DEFAULT 0,
        cash_submitted_to INTEGER, cash_submitted_amt REAL DEFAULT 0,
        online_submitted_amt REAL DEFAULT 0,
        wage_cyl_urban INTEGER DEFAULT 0, wage_cyl_rural INTEGER DEFAULT 0,
        wage_amount REAL DEFAULT 0, pair_bonus REAL DEFAULT 0,
        cash_shortage REAL DEFAULT 0, cash_excess REAL DEFAULT 0,
        cash_500 INTEGER DEFAULT 0, cash_200 INTEGER DEFAULT 0,
        cash_100 INTEGER DEFAULT 0, cash_50 INTEGER DEFAULT 0,
        cash_20 INTEGER DEFAULT 0, cash_10 INTEGER DEFAULT 0,
        cash_coins REAL DEFAULT 0, notes TEXT,
        created_at TEXT DEFAULT(datetime('now','localtime')), closed_at TEXT
    );

    CREATE TABLE IF NOT EXISTS trip_transfers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER NOT NULL, transfer_type TEXT NOT NULL,
        to_location TEXT NOT NULL, to_id INTEGER,
        filled_given INTEGER DEFAULT 0, empty_taken INTEGER DEFAULT 0,
        cash_received REAL DEFAULT 0, online_received REAL DEFAULT 0,
        notes TEXT, created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS stock_ledger(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL, location TEXT NOT NULL,
        product TEXT DEFAULT '14.2kg', cylinder_type TEXT NOT NULL,
        movement_type TEXT NOT NULL, quantity REAL NOT NULL,
        ref_id INTEGER, ref_type TEXT, remarks TEXT, entered_by INTEGER,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS godown_physical(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        entry_time TEXT, entered_by INTEGER,
        f_rows INTEGER DEFAULT 0, f_cols INTEGER DEFAULT 0,
        f_extra INTEGER DEFAULT 0, f_total INTEGER DEFAULT 0,
        e_z1_rows INTEGER DEFAULT 0, e_z1_cols INTEGER DEFAULT 0,
        e_z1_d_extra INTEGER DEFAULT 0, e_z1_s_extra INTEGER DEFAULT 0, e_z1_total INTEGER DEFAULT 0,
        e_z2_rows INTEGER DEFAULT 0, e_z2_cols INTEGER DEFAULT 0,
        e_z2_d_extra INTEGER DEFAULT 0, e_z2_s_extra INTEGER DEFAULT 0, e_z2_total INTEGER DEFAULT 0,
        e_z3_rows INTEGER DEFAULT 0, e_z3_cols INTEGER DEFAULT 0,
        e_z3_d_extra INTEGER DEFAULT 0, e_z3_s_extra INTEGER DEFAULT 0, e_z3_total INTEGER DEFAULT 0,
        e_total INTEGER DEFAULT 0,
        sys_filled INTEGER DEFAULT 0, sys_empty INTEGER DEFAULT 0,
        diff_filled INTEGER DEFAULT 0, diff_empty INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS office_morning_stock(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT UNIQUE NOT NULL,
        f_142 INTEGER DEFAULT 0, e_142 INTEGER DEFAULT 0,
        f_5kg INTEGER DEFAULT 0, e_5kg INTEGER DEFAULT 0,
        blue_books INTEGER DEFAULT 0, suraksha_pipes INTEGER DEFAULT 0,
        dpr_good INTEGER DEFAULT 0, dpr_defective INTEGER DEFAULT 0,
        entered_by INTEGER, created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS office_sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        sale_type TEXT NOT NULL, quantity INTEGER DEFAULT 1,
        unit_price REAL DEFAULT 0, total_amount REAL DEFAULT 0,
        payment_mode TEXT DEFAULT 'cash',
        cash_amount REAL DEFAULT 0, online_amount REAL DEFAULT 0,
        cash_500 INTEGER DEFAULT 0, cash_200 INTEGER DEFAULT 0,
        cash_100 INTEGER DEFAULT 0, cash_50 INTEGER DEFAULT 0,
        cash_20 INTEGER DEFAULT 0, cash_10 INTEGER DEFAULT 0,
        cash_coins REAL DEFAULT 0,
        consumer_number TEXT, notes TEXT, entered_by INTEGER,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS accessory_stock(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        item_type TEXT NOT NULL, quantity INTEGER NOT NULL,
        movement_type TEXT DEFAULT 'in',
        notes TEXT, entered_by INTEGER,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS cash_ledger(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        entry_type TEXT NOT NULL, amount REAL NOT NULL,
        direction TEXT NOT NULL, payment_mode TEXT DEFAULT 'cash',
        ref_id INTEGER, ref_type TEXT, person_id INTEGER,
        cash_500 INTEGER DEFAULT 0, cash_200 INTEGER DEFAULT 0,
        cash_100 INTEGER DEFAULT 0, cash_50 INTEGER DEFAULT 0,
        cash_20 INTEGER DEFAULT 0, cash_10 INTEGER DEFAULT 0,
        cash_coins REAL DEFAULT 0,
        remarks TEXT, entered_by INTEGER,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        category TEXT NOT NULL, description TEXT,
        amount REAL NOT NULL, payment_mode TEXT DEFAULT 'cash',
        staff_id INTEGER, entered_by INTEGER,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS staff_advances(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        staff_id INTEGER NOT NULL, advance_type TEXT NOT NULL,
        amount REAL NOT NULL, notes TEXT, entered_by INTEGER,
        created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS wage_entries(
        id INTEGER PRIMARY KEY AUTOINCREMENT, month TEXT NOT NULL,
        staff_id INTEGER NOT NULL,
        urban_cyl INTEGER DEFAULT 0, rural_cyl INTEGER DEFAULT 0,
        helper_days INTEGER DEFAULT 0,
        wage_amount REAL DEFAULT 0, pair_bonus REAL DEFAULT 0,
        cash_shortage REAL DEFAULT 0,
        advance_recovered REAL DEFAULT 0, net_payable REAL DEFAULT 0,
        mgr_approved INTEGER DEFAULT 0, mgr_approved_by INTEGER, mgr_approved_at TEXT,
        owner_approved INTEGER DEFAULT 0, owner_approved_by INTEGER, owner_approved_at TEXT,
        is_paid INTEGER DEFAULT 0, paid_at TEXT, notes TEXT,
        created_at TEXT DEFAULT(datetime('now','localtime')),
        UNIQUE(month, staff_id)
    );

    CREATE TABLE IF NOT EXISTS bpcl_movements(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        movement_type TEXT NOT NULL, product TEXT DEFAULT '14.2kg',
        quantity INTEGER NOT NULL, invoice_no TEXT, vehicle_no TEXT,
        entered_by INTEGER, created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS bpcl_soa(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_date TEXT, post_date TEXT, narration TEXT,
        doc_type TEXT, doc_number TEXT,
        amount_credit REAL DEFAULT 0, amount_debit REAL DEFAULT 0,
        cheque_ref TEXT, ref_doc TEXT, month TEXT,
        uploaded_by INTEGER, created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS bpcl_day_end(
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT UNIQUE NOT NULL,
        status TEXT DEFAULT 'pending',
        bpcl_open_filled INTEGER DEFAULT 0, bpcl_received INTEGER DEFAULT 0,
        bpcl_issued INTEGER DEFAULT 0, bpcl_close_filled INTEGER DEFAULT 0,
        bpcl_close_empty INTEGER DEFAULT 0,
        erp_open_filled INTEGER DEFAULT 0, erp_close_filled INTEGER DEFAULT 0,
        erp_close_empty INTEGER DEFAULT 0,
        diff_filled INTEGER DEFAULT 0, diff_empty INTEGER DEFAULT 0,
        entered_by INTEGER, created_at TEXT DEFAULT(datetime('now','localtime'))
    );

    CREATE TABLE IF NOT EXISTS chat_messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL, message TEXT NOT NULL,
        msg_type TEXT DEFAULT 'text', is_notice INTEGER DEFAULT 0,
        photo_path TEXT, created_at TEXT DEFAULT(datetime('now','localtime'))
    );
    """)

    # Default settings
    for k,v in [
        ("cylinder_price","856"),
        ("company_name","Shourya Bharatgas Services"),
        ("dist_code","187618"),
        ("gst_no","27ABRPP5432A1ZL"),
        ("company_address","Gat No 96, Kolhapur Road, Jaysinghpur 416101"),
        ("godown_address","Gat No 15, Kondigre 416146"),
        ("gpay_mobile","7887456789"),
    ]:
        c.execute("INSERT OR IGNORE INTO settings VALUES(?,?)",(k,v))

    # Seed all staff — PIN 1234
    staff = [
        ("Vishal Patil","7887456789","9869234868","owner","Owner & Partner","na",0,None,None),
        ("Mrinmayi Patil","8080802880","","owner","Owner & Partner","na",0,None,None),
        ("Baba","9665036191","7276884888","owner","Owner's Father","na",0,None,None),
        ("Rajesh Awale","8007183197","","manager","Manager","salary",15000,None,None),
        ("Mrs. Awale","9807183197","","bda","BDA - Chipri Beghar","na",0,8,None),
        ("Vishwas Bhore","7643982982","9975464383","delivery","Delivery Man","per_cylinder",0,None,1),
        ("Swapnil Patil","8830669611","","delivery","Delivery Man","per_cylinder",0,None,2),
        ("Haroon Fakir","9970660901","","delivery","Delivery Man","per_cylinder",0,None,4),
        ("Vishal Magdum","9096853954","7643987987","delivery","Delivery Man","per_cylinder",0,None,3),
        ("Ajinath","8669164977","","driver","Truck Driver","salary",18000,None,None),
        ("Sandeep","8788076864","","loader","Unloading Crew","per_truck",400,None,None),
        ("Sager","8605444617","","loader","Unloading Crew","per_truck",400,None,None),
        ("Sarika Waghmode","9561242972","","bda","BDA - Kondigre","na",0,1,None),
        ("Kumar Thomake","9673824646","","bda","BDA - Nimshirgav","na",0,2,None),
        ("Lakhane","7588262265","","bda","BDA - Nimshirgav 2","na",0,3,None),
        ("Manoj","9970731436","","bda","BDA - Danoli","na",0,4,None),
        ("Yadav","9405744020","","bda","BDA - Kothali","na",0,5,None),
        ("Sudhakar Patil","9822180498","","bda","BDA - Kavatesar","na",0,6,None),
        ("Vikrant Kamble","7028502299","","bda","BDA - Shirol","na",0,7,None),
    ]
    for nm,mob,alt,role,desig,wt,sal,bda,veh in staff:
        c.execute("""INSERT OR IGNORE INTO users
            (name,mobile,alt_mobile,role,designation,pin_hash,wage_type,salary_fixed,bda_id,vehicle_id,must_change_pin)
            VALUES(?,?,?,?,?,?,?,?,?,?,1)""",
            (nm,mob,alt,role,desig,hpin("1234"),wt,sal,bda,veh))
    c.commit(); c.close()

# ── Stock helpers ──────────────────────────────────────────────
def stock_bal(conn, location, ctype, product="14.2kg"):
    r = conn.execute(
        "SELECT COALESCE(SUM(quantity),0) FROM stock_ledger WHERE location=? AND cylinder_type=? AND product=?",
        (location,ctype,product)).fetchone()[0]
    return int(r)

def add_stock(conn, location, ctype, qty, mtype, product="14.2kg",
              ref_id=None, ref_type=None, remarks=None, by=None, date=None):
    conn.execute("""INSERT INTO stock_ledger(date,location,product,cylinder_type,
        movement_type,quantity,ref_id,ref_type,remarks,entered_by)
        VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (date or today(),location,product,ctype,mtype,qty,ref_id,ref_type,remarks,by))

def full_stock(conn):
    locs = ["godown","office","defective","manual_adjust"]
    for v in VEHICLES: locs.append(f"vehicle_{v}")
    for b in BDA_MAP:  locs.append(f"bda_{b}")
    res = {}
    for loc in locs:
        res[loc] = {"filled": stock_bal(conn,loc,"filled"),
                    "empty":  stock_bal(conn,loc,"empty")}
    res["TOTAL"] = {
        "filled": sum(v["filled"] for k,v in res.items()),
        "empty":  sum(v["empty"]  for k,v in res.items()),
    }
    return res

# ── Cash helpers ───────────────────────────────────────────────
def add_cash(conn, etype, amount, direction, mode="cash",
             ref_id=None, ref_type=None, person_id=None,
             denoms=None, remarks=None, by=None, date=None):
    d = denoms or {}
    conn.execute("""INSERT INTO cash_ledger(date,entry_type,amount,direction,payment_mode,
        ref_id,ref_type,person_id,cash_500,cash_200,cash_100,cash_50,cash_20,cash_10,
        cash_coins,remarks,entered_by) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (date or today(),etype,amount,direction,mode,ref_id,ref_type,person_id,
         d.get("500",0),d.get("200",0),d.get("100",0),d.get("50",0),
         d.get("20",0),d.get("10",0),d.get("coins",0),remarks,by))

def cash_summary(conn, for_date=None):
    where = f" AND date='{for_date}'" if for_date else ""
    ci = conn.execute(f"SELECT COALESCE(SUM(amount),0) FROM cash_ledger WHERE direction='in'{where}").fetchone()[0]
    co = conn.execute(f"SELECT COALESCE(SUM(amount),0) FROM cash_ledger WHERE direction='out'{where}").fetchone()[0]
    return {"in":float(ci),"out":float(co),"net":float(ci)-float(co)}

def advance_balance(conn, staff_id):
    g = conn.execute("SELECT COALESCE(SUM(amount),0) FROM staff_advances WHERE staff_id=? AND advance_type='given'",(staff_id,)).fetchone()[0]
    r = conn.execute("SELECT COALESCE(SUM(amount),0) FROM staff_advances WHERE staff_id=? AND advance_type='recovered'",(staff_id,)).fetchone()[0]
    return float(g) - float(r)

def accessory_bal(conn, itype):
    r = conn.execute(
        "SELECT COALESCE(SUM(CASE WHEN movement_type='in' THEN quantity ELSE -quantity END),0) FROM accessory_stock WHERE item_type=?",
        (itype,)).fetchone()[0]
    return int(r)

def gsetting(key, default=""):
    c = get_db()
    r = c.execute("SELECT value FROM settings WHERE key=?",(key,)).fetchone()
    c.close()
    return r["value"] if r else default

def cyl_price():
    return float(gsetting("cylinder_price","856"))
