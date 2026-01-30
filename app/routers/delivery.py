from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.models.trip import DeliveryTrip

router = APIRouter(prefix="/delivery", tags=["Delivery"])

@router.post("/trip/open")
def open_trip(delivery_man_id: int, db: Session = Depends(get_db)):
    trip = DeliveryTrip(
        delivery_man_id=delivery_man_id,
        date=date.today(),
        trip_no=1,
        status="OPEN"
    )
    db.add(trip)
    commit_or_rollback(db)
    return {"status": "trip opened", "delivery_man_id": delivery_man_id}

@router.post("/trip/sale")
def record_sale(trip_id: int, payment_mode: str, amount: int):
    return {"status": "sale recorded", "trip_id": trip_id}

@router.post("/trip/transfer")
def transfer_stock(trip_id: int, to_location_id: int, filled_qty: int, empty_qty: int = 0):
    return {"status": "stock transferred", "trip_id": trip_id}

@router.post("/trip/close")
def close_trip(trip_id: int):
    return {"status": "trip closed", "trip_id": trip_id}

@router.get("/day-summary")
def delivery_day_summary(delivery_man_id: int, on_date: date):
    return {"delivery_man_id": delivery_man_id, "date": str(on_date)}
