from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_login
from app.models.models import GodownPhysicalEntry, BpclMovement, StockReason
from app.services.stock_service import get_godown_stock_today, add_stock_movement, get_latest_physical_entry
from app.services.day_service import get_or_create_today
from datetime import date

router = APIRouter(prefix="/godown", tags=["godown"])
templates = Jinja2Templates(directory="app/templates")

ALLOWED = ["OWNER", "PARTNER", "OFFICE", "DELIVERY", "LOADER"]


@router.get("/dashboard", response_class=HTMLResponse)
def godown_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    physical = get_latest_physical_entry(db, today)
    ledger_stock = get_godown_stock_today(db)
    bpcl_movements = db.query(BpclMovement).filter(BpclMovement.erp_date == today).all()

    return templates.TemplateResponse("godown/dashboard.html", {
        "request": request,
        "user": user,
        "today": today,
        "physical": physical,
        "ledger_stock": ledger_stock,
        "bpcl_movements": bpcl_movements,
    })


@router.post("/physical-stock")
def save_physical_stock(
    request: Request,
    filled_14_2: int = Form(0),
    empty_14_2:  int = Form(0),
    filled_19:   int = Form(0),
    empty_19:    int = Form(0),
    filled_5:    int = Form(0),
    empty_5:     int = Form(0),
    notes: str       = Form(None),
    db: Session      = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user

    today = date.today()
    get_or_create_today(db, user["id"])

    entry = GodownPhysicalEntry(
        erp_date=today,
        filled_14_2=filled_14_2,
        empty_14_2=empty_14_2,
        filled_19=filled_19,
        empty_19=empty_19,
        filled_5=filled_5,
        empty_5=empty_5,
        entered_by=user["id"],
        notes=notes
    )
    db.add(entry)
    db.commit()
    return RedirectResponse("/godown/dashboard", 302)


@router.post("/bpcl-movement")
def save_bpcl_movement(
    request: Request,
    product_code:    str = Form("5350"),
    filled_received: int = Form(0),
    empty_returned:  int = Form(0),
    notes: str           = Form(None),
    db: Session          = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["OWNER", "PARTNER", "OFFICE", "LOADER"]:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    movement = BpclMovement(
        erp_date=today,
        product_code=product_code,
        filled_received=filled_received,
        empty_returned=empty_returned,
        entered_by=user["id"],
        notes=notes
    )
    db.add(movement)

    # Also record in stock ledger
    if filled_received > 0:
        add_stock_movement(db, today, product_code, "GODOWN",
                           filled_received, True, StockReason.BPCL_RECEIPT,
                           "BPCL", movement.id if movement.id else 0, user["id"])
    if empty_returned > 0:
        add_stock_movement(db, today, product_code, "GODOWN",
                           -empty_returned, False, StockReason.BPCL_RETURN,
                           "BPCL", 0, user["id"])

    db.commit()
    return RedirectResponse("/godown/dashboard", 302)
