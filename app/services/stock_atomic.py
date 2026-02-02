from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.stock import StockMovement as StockMovement, StockOpening

class StockError(Exception):
    pass

def _get_opening(db: Session, location_id: int, on_date: date):
    row = db.query(StockOpening).filter(
        StockOpening.location_id == location_id,
        StockOpening.date == on_date
    ).first()
    if not row:
        row = StockOpening(
            location_id=location_id,
            date=on_date,
            filled_qty=0,
            empty_qty=0
        )
        db.add(row)
        db.flush()
    return row

def _current_balance(db: Session, location_id: int, on_date: date):
    op = _get_opening(db, location_id, on_date)

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

    filled = op.filled_qty + inflow[0] - outflow[0]
    empty = op.empty_qty + inflow[1] - outflow[1]
    return filled, empty

def atomic_move(
    db: Session,
    from_location: int | None,
    to_location: int | None,
    filled_qty: int,
    empty_qty: int,
    reason: str,
    ref_type: str | None = None,
    ref_id: int | None = None,
    on_date: date | None = None
):
    if on_date is None:
        on_date = date.today()

    if filled_qty < 0 or empty_qty < 0:
        raise StockError('Negative quantities not allowed')

    if from_location is not None:
        cur_f, cur_e = _current_balance(db, from_location, on_date)
        if cur_f - filled_qty < 0 or cur_e - empty_qty < 0:
            raise StockError('Insufficient stock at source')

    mv = StockMovement(
        date=on_date,
        from_location=from_location,
        to_location=to_location,
        filled_qty=filled_qty,
        empty_qty=empty_qty,
        reason=reason,
        ref_type=ref_type,
        ref_id=ref_id
    )
    db.add(mv)
    db.flush()
    return mv
