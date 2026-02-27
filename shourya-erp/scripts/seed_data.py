"""
Run ONCE on a fresh database to set up initial users, vehicles, and BDA masters.
Command: python scripts/seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, SessionLocal, Base
from app.models.models import User, Vehicle, BdaMaster, UserRole
from app.core.auth import hash_pin

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # ── USERS ──────────────────────────────────────────────────────
    # Real data from ERP_system_Development.docx
    # Urban rate: ₹8/cylinder (doc says 8), Rural: ₹7/cylinder
    # Pair bonus ₹200 extra (handled separately)
    users = [
        {"name": "Vishal Patil",    "mobile": "7887456789", "role": UserRole.OWNER,    "pin": "1234", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Vishal Patil (Alt)","mobile": "9869234868","role": UserRole.OWNER,   "pin": "1234", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Mrinmayi Patil",  "mobile": "8080802880", "role": UserRole.PARTNER,  "pin": "5678", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Baba",            "mobile": "7276884888", "role": UserRole.OFFICE,   "pin": "9999", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Vishwas Bhore",   "mobile": "7643982982", "role": UserRole.DELIVERY, "pin": "1111", "rate_urban": 8.0, "rate_rural": 7.0},
        {"name": "Swapnil Patil",   "mobile": "8830669611", "role": UserRole.DELIVERY, "pin": "2222", "rate_urban": 8.0, "rate_rural": 7.0},
        {"name": "Vishal Magdum",   "mobile": "9096853954", "role": UserRole.DELIVERY, "pin": "3333", "rate_urban": 8.0, "rate_rural": 7.0},
        {"name": "Haroon Fakir",    "mobile": "9970660901", "role": UserRole.DELIVERY, "pin": "4444", "rate_urban": 8.0, "rate_rural": 7.0},
        {"name": "Sandeep",         "mobile": "8788076864", "role": UserRole.LOADER,   "pin": "5555", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Sager",           "mobile": "8605444617", "role": UserRole.LOADER,   "pin": "6666", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Ajinath",         "mobile": "8669164977", "role": UserRole.LOADER,   "pin": "7777", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Rakesh Awale",    "mobile": "8007183197", "role": UserRole.OFFICE,   "pin": "8888", "rate_urban": 0,   "rate_rural": 0},
        # BDA owners as ERP users — they can log in to capture OTP and spot deliveries
        {"name": "Sarika Waghmode", "mobile": "9561242972", "role": UserRole.BDA,      "pin": "9001", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Kumar Thomake",   "mobile": "9673824646", "role": UserRole.BDA,      "pin": "9002", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Vikrant Kamble",  "mobile": "7028502299", "role": UserRole.BDA,      "pin": "9003", "rate_urban": 0,   "rate_rural": 0},
        {"name": "Chipri BDA",      "mobile": "8007183198", "role": UserRole.BDA,      "pin": "9004", "rate_urban": 0,   "rate_rural": 0},
    ]
    for u in users:
        existing = db.query(User).filter(User.mobile == u["mobile"]).first()
        if not existing:
            db.add(User(
                name=u["name"], mobile=u["mobile"], role=u["role"],
                pin_hash=hash_pin(u["pin"]),
                rate_urban=u["rate_urban"], rate_rural=u["rate_rural"]
            ))
    db.commit()
    print("✅ Users seeded")

    # ── VEHICLES ───────────────────────────────────────────────────
    # Get driver IDs
    bhore   = db.query(User).filter(User.name == "Bhore").first()
    swapnil = db.query(User).filter(User.name == "Swapnil Patil").first()
    magdum  = db.query(User).filter(User.name == "Vishal Magdum").first()
    haroon  = db.query(User).filter(User.name == "Haroon").first()

    vehicles = [
        {"name": "Tata 407",  "capacity": 55, "extra_cap": 10, "driver": bhore},
        {"name": "Mega XL",   "capacity": 35, "extra_cap": 8,  "driver": swapnil},
        {"name": "Hatti",     "capacity": 20, "extra_cap": 8,  "driver": magdum},
        {"name": "Appe",      "capacity": 20, "extra_cap": 8,  "driver": haroon},
        {"name": "New Hatti", "capacity": 40, "extra_cap": 5,  "driver": None},
    ]
    for v in vehicles:
        existing = db.query(Vehicle).filter(Vehicle.name == v["name"]).first()
        if not existing:
            db.add(Vehicle(
                name=v["name"], capacity=v["capacity"], extra_cap=v["extra_cap"],
                default_driver_id=v["driver"].id if v["driver"] else None
            ))
    db.commit()
    print("✅ Vehicles seeded")

    # Real BDA data from ERP_system_Development.docx
    bdas = [
        {"name": "Kondigre BDA",   "village": "Kondigre",   "owner": "Sarika Waghmode", "mobile": "9561242972", "max_allowed": 50},
        {"name": "Nimshirgav BDA", "village": "Nimshirgav", "owner": "Kumar Thomake",   "mobile": "9673824646", "max_allowed": 40},
        {"name": "Shirol BDA",     "village": "Shirol",     "owner": "Vikrant Kamble",  "mobile": "7028502299", "max_allowed": 50},
        {"name": "Chipri Beghar BDA","village": "Chipri Beghar","owner": "Rajesh Awale","mobile": "8007183197", "max_allowed": 30},
    ]
    for b in bdas:
        existing = db.query(BdaMaster).filter(BdaMaster.name == b["name"]).first()
        if not existing:
            db.add(BdaMaster(name=b["name"], village=b["village"],
                             owner_name=b["owner"], mobile=b["mobile"],
                             max_allowed=b["max_allowed"]))
    db.commit()
    print("✅ BDA Masters seeded")

    print("\n🎉 Seed complete! Real data from your documents.")
    print("\nLogin credentials (change PINs after first login):")
    print("  Vishal (Owner):        mobile=7887456789   PIN=1234")
    print("  Mrinmayi (Partner):    mobile=8080802880   PIN=1234")
    print("  Bhore (Delivery):      mobile=7643982982   PIN=1111")
    print("  Swapnil (Delivery):    mobile=8830669611   PIN=2222")
    print("  Vishal M (Delivery):   mobile=9096853954   PIN=3333")
    print("  Haroon (Delivery):     mobile=9970660901   PIN=4444")
    print("  Sandeep (Loader):      mobile=8788076864   PIN=5555")
    print("  Sager (Loader):        mobile=8605444617   PIN=6666")
    print("  Ajinath (Loader):      mobile=8669164977   PIN=7777")
    print("  Rakesh Awale (Office): mobile=8007183197   PIN=8888")
    print("  Sarika BDA (Kondigre): mobile=9561242972   PIN=9001")
    print("  Kumar BDA (Nimshirgav):mobile=9673824646   PIN=9002")
    print("  Vikrant BDA (Shirol):  mobile=7028502299   PIN=9003")
    print("  Chipri BDA:            mobile=8007183198   PIN=9004")
    print("\n⚠️  CHANGE ALL PINS IMMEDIATELY AFTER FIRST LOGIN!")

seed()
db.close()
