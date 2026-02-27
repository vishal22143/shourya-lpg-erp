from sqlalchemy.orm import Session
from app.models.models import WageEntry, Trip, DeliveryPool, DeliveryStatus, User
from datetime import date


RATE_URBAN  = 8.0   # ₹ per cylinder (urban delivery) — from ERP doc
RATE_RURAL  = 7.0   # ₹ per cylinder (rural/BDA delivery) — from ERP doc
RATE_PAIR_BONUS = 200.0  # ₹ extra per day when 2 delivery men work together


def compute_wages_for_trip(db: Session, trip: Trip) -> WageEntry:
    """Called when a trip is closed. Auto-computes wages."""
    # Count urban vs rural deliveries in this trip
    deliveries = db.query(DeliveryPool).filter(
        DeliveryPool.trip_id == trip.id,
        DeliveryPool.status.in_([DeliveryStatus.DELIVERED, DeliveryStatus.DELIVERED_EMERGENCY])
    ).all()

    urban_count  = len([d for d in deliveries if not _is_rural(d.area)])
    rural_count  = len([d for d in deliveries if _is_rural(d.area)])

    # BDA deliveries count as rural
    rural_count += _get_bda_count(db, trip.id)

    staff = db.query(User).filter(User.id == trip.delivery_man_id).first()
    rate_u = staff.rate_urban if staff and staff.rate_urban else RATE_URBAN
    rate_r = staff.rate_rural if staff and staff.rate_rural else RATE_RURAL

    gross = (urban_count * rate_u) + (rural_count * rate_r)

    # Check pending advance recovery
    advance_balance = _get_advance_balance(db, trip.delivery_man_id)
    recovery = min(advance_balance, gross * 0.2)  # max 20% recovery per day
    net = gross - recovery

    wage = WageEntry(
        erp_date=trip.erp_date,
        staff_id=trip.delivery_man_id,
        trip_id=trip.id,
        cylinders_urban=urban_count,
        cylinders_rural=rural_count,
        rate_urban=rate_u,
        rate_rural=rate_r,
        gross_wage=gross,
        advance_recovery=recovery,
        net_wage=net
    )
    db.add(wage)
    db.commit()
    db.refresh(wage)
    return wage


def _is_rural(area: str) -> bool:
    if not area:
        return False
    rural_keywords = ["shirol", "kondigre", "kagal", "hatkanangale", "nandani"]
    return any(k in area.lower() for k in rural_keywords)


def _get_bda_count(db: Session, trip_id: int) -> int:
    from app.models.models import BdaTransaction
    txns = db.query(BdaTransaction).filter(BdaTransaction.trip_id == trip_id).all()
    return sum(t.filled_issued for t in txns)


def _get_advance_balance(db: Session, staff_id: int) -> float:
    from app.models.models import StaffAdvance
    from sqlalchemy import func
    result = db.query(func.sum(StaffAdvance.amount)).filter(
        StaffAdvance.staff_id == staff_id
    ).scalar()
    return float(result or 0.0)


def get_monthly_wages(db: Session, staff_id: int, year: int, month: int):
    from sqlalchemy import extract
    return db.query(WageEntry).filter(
        WageEntry.staff_id == staff_id,
        extract("year", WageEntry.erp_date) == year,
        extract("month", WageEntry.erp_date) == month
    ).all()
