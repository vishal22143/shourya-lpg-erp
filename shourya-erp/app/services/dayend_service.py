from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import (
    Trip, DeliveryPool, StockLedger, CashLedger, GodownPhysicalEntry,
    BdaTransaction, WageEntry, DeliveryStatus, TripStatus, DayEndSnapshot
)
from datetime import date


def generate_day_end(db: Session, erp_date: date, created_by: int) -> dict:
    """Generate complete day-end summary — read-only, no modifications"""

    # 1. DELIVERY SUMMARY
    all_deliveries = db.query(DeliveryPool).filter(DeliveryPool.erp_date == erp_date).all()
    delivered = [d for d in all_deliveries if d.status in [DeliveryStatus.DELIVERED, DeliveryStatus.DELIVERED_EMERGENCY]]
    pending   = [d for d in all_deliveries if d.status == DeliveryStatus.SCHEDULED]
    cancelled = [d for d in all_deliveries if d.status == DeliveryStatus.CANCELLED]

    # 2. TRIP SUMMARY
    trips = db.query(Trip).filter(Trip.erp_date == erp_date).all()
    trip_summaries = []
    for t in trips:
        trip_summaries.append({
            "trip_id": t.id,
            "delivery_man": t.delivery_man.name if t.delivery_man else "",
            "vehicle": t.vehicle.name if t.vehicle else "",
            "status": t.status.value,
            "filled_issued": t.filled_issued,
            "total_sales": t.total_sales,
            "cash_collected": t.cash_collected,
            "online_collected": t.online_collected,
            "bda_cash": t.bda_cash,
            "bda_online": t.bda_online,
        })

    # 3. STOCK SUMMARY
    # Godown stock from ledger
    godown_stock = _calc_stock(db, "GODOWN", erp_date)

    # Latest physical entry
    physical = db.query(GodownPhysicalEntry).filter(
        GodownPhysicalEntry.erp_date == erp_date
    ).order_by(GodownPhysicalEntry.id.desc()).first()

    # 4. CASH SUMMARY
    cash_entries = db.query(CashLedger).filter(CashLedger.erp_date == erp_date).all()
    total_cash_in   = sum(e.amount for e in cash_entries if e.amount > 0)
    total_cash_out  = sum(e.amount for e in cash_entries if e.amount < 0)

    # 5. BDA SUMMARY
    bda_txns = db.query(BdaTransaction).filter(BdaTransaction.erp_date == erp_date).all()
    bda_total_filled  = sum(t.filled_issued for t in bda_txns)
    bda_total_cash    = sum(t.cash_paid for t in bda_txns)
    bda_total_online  = sum(t.online_paid for t in bda_txns)

    # 6. WAGES
    wages = db.query(WageEntry).filter(WageEntry.erp_date == erp_date).all()
    total_wages = sum(w.net_wage for w in wages)

    snapshot = {
        "erp_date": erp_date.isoformat(),
        "delivery_summary": {
            "scheduled":  len(all_deliveries),
            "delivered":  len(delivered),
            "pending":    len(pending),
            "cancelled":  len(cancelled),
        },
        "trip_summaries": trip_summaries,
        "stock_summary": {
            "godown_ledger": godown_stock,
            "physical_count": {
                "filled_14_2": physical.filled_14_2 if physical else None,
                "empty_14_2":  physical.empty_14_2  if physical else None,
            } if physical else None
        },
        "cash_summary": {
            "total_in":  total_cash_in,
            "total_out": total_cash_out,
            "net":       total_cash_in + total_cash_out,
        },
        "bda_summary": {
            "filled_issued": bda_total_filled,
            "cash_collected": bda_total_cash,
            "online_collected": bda_total_online,
        },
        "wages_total": total_wages,
    }

    # Save snapshot
    existing = db.query(DayEndSnapshot).filter(DayEndSnapshot.erp_date == erp_date).first()
    if existing:
        existing.snapshot_json = snapshot
        existing.created_by = created_by
    else:
        snap = DayEndSnapshot(
            erp_date=erp_date,
            snapshot_json=snapshot,
            created_by=created_by
        )
        db.add(snap)
    db.commit()
    return snapshot


def _calc_stock(db: Session, location: str, erp_date: date) -> dict:
    entries = db.query(StockLedger).filter(
        StockLedger.location == location,
        StockLedger.erp_date <= erp_date
    ).all()
    result = {}
    for e in entries:
        if e.product_code not in result:
            result[e.product_code] = {"filled": 0, "empty": 0}
        key = "filled" if e.is_filled else "empty"
        result[e.product_code][key] += e.qty
    return result
