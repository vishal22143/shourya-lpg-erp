# =====================================================
# SHOURYA LPG ERP
# S5.1-C-2 — Owner Day-End Top Panel (READ ONLY)
# Source of Truth: ERP_FREEZE.md
# NO INSERT / UPDATE / DELETE
# =====================================================

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from data.db import get_conn

router = APIRouter(prefix="/owner")
templates = Jinja2Templates(directory="templates")


@router.get("/day-end", response_class=HTMLResponse)
def owner_day_end_today(request: Request):
    today = date.today().strftime("%Y-%m-%d")
    return owner_day_end_by_date(request, today)


@router.get("/day-end/{day}", response_class=HTMLResponse)
def owner_day_end_by_date(request: Request, day: str):
    conn = get_conn()
    cur = conn.cursor()

    # ---------------- DAY STATUS ----------------
    # Default assumptions (safe)
    day_status = "PENDING"
    bpcl_status = "PENDING"

    # ---------------- DELIVERY COUNTS ----------------
    cur.execute("""
        SELECT COUNT(DISTINCT cashmemo)
        FROM deliveries
        WHERE DATE(updated_at) = ?
    """, (day,))
    total_deliveries = cur.fetchone()[0] or 0

    # ---------------- CASH (DELIVERY) ----------------
    cur.execute("""
        SELECT
            COALESCE(SUM(
                d500*500 + d200*200 + d100*100 +
                d50*50 + d20*20 + d10*10 + coins
            ),0)
        FROM trip_cash_denomination
        JOIN delivery_trips
          ON delivery_trips.id = trip_cash_denomination.trip_id
        WHERE delivery_trips.trip_date = ?
    """, (day,))
    delivery_cash = cur.fetchone()[0] or 0

    # ---------------- OFFICE CASH ----------------
    cur.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM office_additional_items
        WHERE entry_date = ? AND cash_direction = 'CREDIT'
    """, (day,))
    office_cash = cur.fetchone()[0] or 0

    # ---------------- EXPENSES ----------------
    cur.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM office_expenses
        WHERE entry_date = ?
    """, (day,))
    expenses = cur.fetchone()[0] or 0

    total_cash = delivery_cash + office_cash - expenses

    conn.close()

    return templates.TemplateResponse(
        "owner_dayend.html",
        {
            "request": request,
            "day": day,
            "day_status": day_status,
            "bpcl_status": bpcl_status,
            "total_deliveries": total_deliveries,
            "delivery_cash": delivery_cash,
            "office_cash": office_cash,
            "expenses": expenses,
            "total_cash": total_cash
        }
    )
