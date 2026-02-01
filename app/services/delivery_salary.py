from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import DeliveryDaySummary
from app.models import StaffAdvance

URBAN_RATE = 8   # SHAHARI
RURAL_RATE = 7   # GAVAATIL
HELPER_PER_DAY = 200

def compute_delivery_salary(db: Session, delivery_man_id: int, month_prefix: str):
    days = db.query(DeliveryDaySummary).filter(
        DeliveryDaySummary.delivery_man_id == delivery_man_id,
        DeliveryDaySummary.confirmed_by != None,
        DeliveryDaySummary.date.like(f'{month_prefix}%')
    ).all()

    base = 0
    helper_days = 0

    for d in days:
        rate = URBAN_RATE if d.day_type == 'SHAHARI' else RURAL_RATE
        base += d.total_cylinders * rate
        if d.helper_used:
            helper_days += 1

    helper_amt = helper_days * HELPER_PER_DAY
    gross = base + helper_amt

    adv = db.query(
        func.coalesce(func.sum(StaffAdvance.amount), 0),
        func.coalesce(func.sum(StaffAdvance.recovered), 0)
    ).filter(
        StaffAdvance.staff_type == 'DELIVERY',
        StaffAdvance.staff_id == delivery_man_id
    ).one()

    pending_advance = adv[0] - adv[1]

    return {
        'base_wage': base,
        'helper_days': helper_days,
        'helper_amount': helper_amt,
        'gross': gross,
        'pending_advance': pending_advance
    }
