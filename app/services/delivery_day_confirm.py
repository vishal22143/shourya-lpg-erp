from datetime import datetime
from sqlalchemy.orm import Session
from app.models import DeliveryDaySummary
from app.models import DeliveryCylinderDetail

def classify_day(db: Session, delivery_man_id: int, on_date):
    rows = db.query(DeliveryCylinderDetail).filter(
        DeliveryCylinderDetail.delivery_man_id == delivery_man_id,
        DeliveryCylinderDetail.date == on_date
    ).all()

    total = sum(r.cylinders for r in rows)
    has_urban = any(r.area_type == 'URBAN' for r in rows)
    has_rural = any(r.area_type == 'RURAL' for r in rows)

    # Mixed day -> SHAHARI
    day_type = 'SHAHARI' if (has_urban or (has_urban and has_rural)) else 'GAVAATIL'
    return total, day_type

def confirm_day(
    db: Session,
    delivery_man_id: int,
    on_date,
    helper_used: bool,
    confirmed_by: str
):
    total, day_type = classify_day(db, delivery_man_id, on_date)

    db.merge(DeliveryDaySummary(
        delivery_man_id=delivery_man_id,
        date=on_date,
        total_cylinders=total,
        day_type=day_type,
        helper_used=helper_used,
        confirmed_by=confirmed_by,
        confirmed_at=datetime.utcnow()
    ))
