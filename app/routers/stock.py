from fastapi import APIRouter
from datetime import date

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/transfer")
def stock_transfer(from_location: int, to_location: int, filled_qty: int, empty_qty: int = 0):
    return {"status": "stock transferred"}

@router.post("/adjustment")
def stock_adjustment(location_id: int, filled_delta: int, empty_delta: int, reason: str):
    return {"status": "adjustment recorded"}

@router.get("/location-summary")
def location_summary(location_id: int, on_date: date):
    return {"location_id": location_id, "date": str(on_date)}

@router.get("/day-end")
def stock_day_end(on_date: date):
    return {"date": str(on_date)}
