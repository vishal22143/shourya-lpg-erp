from datetime import date
from app.core.database import SessionLocal
from app.models.stock import StockLocation, StockOpening
from app.models.delivery import DeliveryMan
from app.models.bda import BDA

db = SessionLocal()
today = date.today()

# ------------------------
# BASE LOCATIONS (PRODUCT-WISE)
# ------------------------
base_locations = [
    'GODOWN_14_2', 'GODOWN_5',
    'OFFICE_14_2', 'OFFICE_5',
    'TRANSIT_14_2', 'TRANSIT_5'
]

for lt in base_locations:
    if not db.query(StockLocation).filter(StockLocation.location_type == lt).first():
        db.add(StockLocation(location_type=lt, ref_id=None))

db.commit()

# ------------------------
# DELIVERY LOCATIONS
# ------------------------
for d in db.query(DeliveryMan).all():
    for p in ('14_2', '5'):
        lt = f'DELIVERY_{d.id}_{p}'
        if not db.query(StockLocation).filter(StockLocation.location_type == lt).first():
            db.add(StockLocation(location_type=lt, ref_id=d.id))

# ------------------------
# BDA LOCATIONS
# ------------------------
for b in db.query(BDA).all():
    for p in ('14_2', '5'):
        lt = f'BDA_{b.id}_{p}'
        if not db.query(StockLocation).filter(StockLocation.location_type == lt).first():
            db.add(StockLocation(location_type=lt, ref_id=b.id))

db.commit()

# ------------------------
# OPENING STOCK (PRODUCT-WISE)
# ------------------------
opening_stock = {
    'GODOWN_14_2': (500, 480),
    'GODOWN_5': (120, 110),
    'OFFICE_14_2': (0, 0),
    'OFFICE_5': (0, 0),
    'TRANSIT_14_2': (0, 0),
    'TRANSIT_5': (0, 0),
}

for lt, (f, e) in opening_stock.items():
    loc = db.query(StockLocation).filter(StockLocation.location_type == lt).one()
    if not db.query(StockOpening).filter(
        StockOpening.location_id == loc.id,
        StockOpening.date == today
    ).first():
        db.add(StockOpening(
            location_id=loc.id,
            date=today,
            filled_qty=f,
            empty_qty=e
        ))

db.commit()
db.close()

print('PHASE 6.1 SEEDING COMPLETED SUCCESSFULLY')
