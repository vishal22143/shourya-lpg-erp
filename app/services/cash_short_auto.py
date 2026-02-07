from datetime import date
from app.models.staff_advance import StaffAdvance

def auto_cash_short_advance(db, delivery_man_id: int, amount: int, source_ref: int, approved_by: str):
    if amount <= 0:
        return
    db.add(StaffAdvance(
        staff_type='DELIVERY',
        staff_id=delivery_man_id,
        date=date.today(),
        amount=amount,
        recovered=0,
        advance_type='CASH_SHORT',
        approved_by=approved_by,
        source_ref=source_ref
    ))
