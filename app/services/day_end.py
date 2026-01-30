from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.stock import StockLocation, StockOpening, StockMovement
from app.models.stock_day_end import StockDayEnd

class DayEndError(Exception):
    pass

def compute_location_balance(db: Session, location_id: int, on_date: date):
    opening = db.query(StockOpening).filter(
        StockOpening.location_id == location_id,
        StockOpening.date == on_date
    ).first()

    op_f = opening.filled_qty if opening else 0
    op_e = opening.empty_qty if opening else 0

    inflow = db.query(
        func.coalesce(func.sum(StockMovement.filled_qty), 0),
        func.coalesce(func.sum(StockMovement.empty_qty), 0)
    ).filter(
        StockMovement.to_location == location_id,
        StockMovement.date == on_date
    ).one()

    outflow = db.query(
        func.coalesce(func.sum(StockMovement.filled_qty), 0),
        func.coalesce(func.sum(StockMovement.empty_qty), 0)
    ).filter(
        StockMovement.from_location == location_id,
        StockMovement.date == on_date
    ).one()

    filled = op_f + inflow[0] - outflow[0]
    empty = op_e + inflow[1] - outflow[1]

    if filled < 0 or empty < 0:
        raise DayEndError('Negative balance detected')

    return filled, empty

def run_day_end(db: Session, on_date: date | None = None):
    if on_date is None:
        on_date = date.today()

    locations = db.query(StockLocation).all()
    if not locations:
        raise DayEndError('No stock locations found')

    # Clear existing snapshot for the day (idempotent)
    db.query(StockDayEnd).filter(StockDayEnd.date == on_date).delete()

    total_filled = 0
    total_empty = 0

    for loc in locations:
        f, e = compute_location_balance(db, loc.id, on_date)
        total_filled += f
        total_empty += e
        db.add(StockDayEnd(
            date=on_date,
            location_id=loc.id,
            filled_qty=f,
            empty_qty=e
        ))

    return {
        'date': str(on_date),
        'total_filled': total_filled,
        'total_empty': total_empty
    }
