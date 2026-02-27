from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import StockLedger, GodownPhysicalEntry
from datetime import date


def get_location_stock(db: Session, location: str, erp_date: date = None) -> dict:
    """Returns {product_code: {filled: n, empty: n}} for a location"""
    q = db.query(StockLedger).filter(StockLedger.location == location)
    if erp_date:
        q = q.filter(StockLedger.erp_date <= erp_date)
    entries = q.all()

    stock = {}
    for e in entries:
        if e.product_code not in stock:
            stock[e.product_code] = {"filled": 0, "empty": 0}
        if e.is_filled:
            stock[e.product_code]["filled"] += e.qty
        else:
            stock[e.product_code]["empty"] += e.qty
    return stock


def get_godown_stock_today(db: Session) -> dict:
    return get_location_stock(db, "GODOWN", date.today())


def add_stock_movement(db: Session, erp_date: date, product_code: str,
                       location: str, qty: int, is_filled: bool,
                       reason, ref_type: str, ref_id: int, created_by: int,
                       notes: str = None):
    entry = StockLedger(
        erp_date=erp_date,
        product_code=product_code,
        location=location,
        qty=qty,
        is_filled=is_filled,
        reason=reason,
        ref_type=ref_type,
        ref_id=ref_id,
        created_by=created_by,
        notes=notes
    )
    db.add(entry)
    db.commit()
    return entry


def get_latest_physical_entry(db: Session, erp_date: date = None) -> GodownPhysicalEntry:
    q = db.query(GodownPhysicalEntry)
    if erp_date:
        q = q.filter(GodownPhysicalEntry.erp_date == erp_date)
    return q.order_by(GodownPhysicalEntry.id.desc()).first()
