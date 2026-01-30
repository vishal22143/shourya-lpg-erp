from fastapi import APIRouter
from datetime import date

router = APIRouter(prefix="/bda", tags=["BDA"])

@router.post("/stock/receive")
def receive_stock(bda_id: int, filled_qty: int):
    return {"status": "stock received", "bda_id": bda_id}

@router.post("/sale")
def bda_sale(bda_id: int, payment_mode: str, amount: int):
    return {"status": "sale recorded", "bda_id": bda_id}

@router.post("/cash/handover")
def bda_cash_handover(
    bda_id: int,
    amount: int,
    payment_mode: str,
    receiver_type: str,
    receiver_id: int | None = None
):
    return {
        "status": "handover recorded",
        "bda_id": bda_id,
        "receiver": receiver_type
    }

@router.get("/day-summary")
def bda_day_summary(bda_id: int, on_date: date):
    return {"bda_id": bda_id, "date": str(on_date)}
