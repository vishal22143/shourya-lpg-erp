from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.db import conn

router = APIRouter()
tpl = Jinja2Templates(directory="templates")

@router.get("/strict/godown")
def strict_view(request: Request):
    c = conn()
    rows = c.execute(
        """SELECT date,
        SUM(CASE WHEN event_type='INWARD' THEN filled ELSE 0 END) as inward,
        SUM(CASE WHEN event_type='OUTWARD' THEN filled ELSE 0 END) as outward
        FROM godown_events GROUP BY date ORDER BY date"""
    ).fetchall()
    c.close()

    ledger = []
    closing = 0
    for d, inward, outward in rows:
        opening = closing
        closing = opening + inward - outward
        ledger.append({
            "date": d,
            "opening": opening,
            "inward": inward,
            "outward": outward,
            "closing": closing
        })

    return tpl.TemplateResponse(
        "godown_strict.html",
        {"request": request, "ledger": ledger}
    )
