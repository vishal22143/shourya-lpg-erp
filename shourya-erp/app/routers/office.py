from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_login
from app.models.models import (
    CashLedger, OfficeExpense, StaffAdvance, OfficeStock,
    CashReason, PaymentMode, User, Trip, DeliveryPool, DeliveryStatus
)
from app.services.day_service import get_or_create_today
from datetime import date

router = APIRouter(prefix="/office", tags=["office"])
templates = Jinja2Templates(directory="app/templates")

ALLOWED = ["OWNER", "PARTNER", "OFFICE"]


@router.get("/dashboard", response_class=HTMLResponse)
def office_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    cash_entries = db.query(CashLedger).filter(CashLedger.erp_date == today).all()
    expenses     = db.query(OfficeExpense).filter(OfficeExpense.erp_date == today).all()
    advances     = db.query(StaffAdvance).filter(StaffAdvance.erp_date == today).all()
    trips        = db.query(Trip).filter(Trip.erp_date == today).all()
    staff        = db.query(User).filter(User.is_active == True).all()

    total_cash_in    = sum(e.amount for e in cash_entries if e.amount > 0)
    total_cash_out   = sum(e.amount for e in cash_entries if e.amount < 0)
    total_expenses   = sum(e.amount for e in expenses)
    total_deliveries = db.query(DeliveryPool).filter(
        DeliveryPool.erp_date == today,
        DeliveryPool.status.in_([DeliveryStatus.DELIVERED, DeliveryStatus.DELIVERED_EMERGENCY])
    ).count()

    return templates.TemplateResponse("office/dashboard.html", {
        "request": request,
        "user": user,
        "today": today,
        "cash_entries": cash_entries,
        "expenses": expenses,
        "advances": advances,
        "trips": trips,
        "staff": staff,
        "total_cash_in": total_cash_in,
        "total_cash_out": total_cash_out,
        "total_expenses": total_expenses,
        "total_deliveries": total_deliveries,
    })


@router.post("/opening-cash")
def opening_cash(
    request: Request,
    amount: float   = Form(...),
    notes: str      = Form(None),
    db: Session     = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    get_or_create_today(db, user["id"])

    # Check no existing opening cash today
    existing = db.query(CashLedger).filter(
        CashLedger.erp_date == today,
        CashLedger.reason == CashReason.OPENING
    ).first()
    if existing:
        return RedirectResponse("/office/dashboard", 302)

    entry = CashLedger(
        erp_date=today,
        location="OFFICE",
        amount=amount,
        mode=PaymentMode.CASH,
        reason=CashReason.OPENING,
        actor_id=user["id"],
        notes=notes
    )
    db.add(entry)
    db.commit()
    return RedirectResponse("/office/dashboard", 302)


@router.post("/add-expense")
def add_expense(
    request: Request,
    head:   str   = Form(...),
    amount: float = Form(...),
    mode:   str   = Form("CASH"),
    paid_to: str  = Form(None),
    notes:  str   = Form(None),
    db: Session   = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    expense = OfficeExpense(
        erp_date=today,
        head=head,
        amount=amount,
        mode=PaymentMode(mode),
        paid_to=paid_to,
        created_by=user["id"],
        notes=notes
    )
    db.add(expense)

    # Also record in cash ledger as outflow
    cash_out = CashLedger(
        erp_date=today,
        location="OFFICE",
        amount=-amount,
        mode=PaymentMode(mode),
        reason=CashReason.EXPENSE,
        actor_id=user["id"],
        notes=f"{head}: {notes or ''}"
    )
    db.add(cash_out)
    db.commit()
    return RedirectResponse("/office/dashboard", 302)


@router.post("/add-advance")
def add_advance(
    request: Request,
    staff_id: int  = Form(...),
    amount: float  = Form(...),
    notes: str     = Form(None),
    db: Session    = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    advance = StaffAdvance(
        erp_date=today,
        staff_id=staff_id,
        amount=amount,
        source="MANUAL",
        created_by=user["id"],
        notes=notes
    )
    db.add(advance)

    cash_out = CashLedger(
        erp_date=today,
        location="OFFICE",
        amount=-amount,
        mode=PaymentMode.CASH,
        reason=CashReason.ADVANCE,
        ref_id=staff_id,
        actor_id=user["id"],
        notes=notes
    )
    db.add(cash_out)
    db.commit()
    return RedirectResponse("/office/dashboard", 302)


@router.post("/sv-connection")
def sv_new_connection(
    request: Request,
    consumer_name: str = Form(...),
    consumer_no: str   = Form(None),
    amount: float      = Form(4000),
    mode: str          = Form("CASH"),
    notes: str         = Form(None),
    db: Session        = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    entry = CashLedger(
        erp_date=today,
        location="OFFICE",
        amount=amount,
        mode=PaymentMode(mode),
        reason=CashReason.SV_NEW_CONNECTION,
        actor_id=user["id"],
        notes=f"SV: {consumer_name} ({consumer_no or 'no no.'}). {notes or ''}"
    )
    db.add(entry)
    db.commit()
    return RedirectResponse("/office/dashboard", 302)


@router.get("/staff-ledger/{staff_id}", response_class=HTMLResponse)
def staff_ledger(staff_id: int, request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    staff = db.query(User).filter(User.id == staff_id).first()
    advances = db.query(StaffAdvance).filter(StaffAdvance.staff_id == staff_id)\
                .order_by(StaffAdvance.created_at.desc()).all()
    balance = sum(a.amount for a in advances)

    return templates.TemplateResponse("office/staff_ledger.html", {
        "request": request,
        "user": user,
        "staff": staff,
        "advances": advances,
        "balance": balance,
    })


@router.get("/additional-sales", response_class=HTMLResponse)
def additional_sales_page(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)
    today = date.today()
    sales_today = db.query(CashLedger).filter(
        CashLedger.erp_date == today,
        CashLedger.location == "OFFICE",
        CashLedger.reason.in_([
            CashReason.BLUEBOOK_SALE, CashReason.PIPE_SALE,
            CashReason.DPR_SALE, CashReason.SV_NEW_CONNECTION,
            CashReason.NAME_CHANGE, CashReason.CYLINDER_5KG
        ])
    ).order_by(CashLedger.id.desc()).all()
    return templates.TemplateResponse("office/additional_sales.html", {
        "request": request, "user": user, "today": today,
        "sales_today": sales_today, "message": None
    })


@router.post("/additional-sale")
def record_additional_sale(
    request: Request,
    sale_type:    str   = Form(...),
    qty:          int   = Form(1),
    unit_price:   float = Form(0.0),
    mode:         str   = Form("CASH"),
    customer_name: str  = Form(None),
    dpr_type:     str   = Form(None),
    db: Session         = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    total = qty * unit_price

    reason_map = {
        "BLUEBOOK_SALE": CashReason.BLUEBOOK_SALE,
        "PIPE_SALE":     CashReason.PIPE_SALE,
        "DPR_SALE":      CashReason.DPR_SALE,
        "NAME_CHANGE":   CashReason.NAME_CHANGE,
        "CYLINDER_5KG":  CashReason.CYLINDER_5KG,
    }
    reason = reason_map.get(sale_type, CashReason.SALE)

    entry = CashLedger(
        erp_date=today,
        location="OFFICE",
        amount=total,
        mode=PaymentMode(mode),
        reason=reason,
        actor_id=user["id"],
        notes=f"{sale_type} x{qty} @₹{unit_price}" + (f" | {customer_name}" if customer_name else "") + (f" | {dpr_type}" if dpr_type else "")
    )
    db.add(entry)

    # Also update office stock ledger for physical items
    if sale_type in ["BLUEBOOK_SALE", "PIPE_SALE", "DPR_SALE", "CYLINDER_5KG"]:
        stock = OfficeStock(
            item_name=sale_type,
            quantity=-qty,
            unit_price=unit_price,
            erp_date=today,
            reason="SALE",
            created_by=user["id"]
        )
        db.add(stock)

    db.commit()
    return RedirectResponse("/office/additional-sales", 302)


@router.post("/save-denominations")
def save_denominations(
    request: Request,
    d500: int = Form(0), d200: int = Form(0), d100: int = Form(0),
    d50:  int = Form(0), d20:  int = Form(0), d10:  int = Form(0),
    coins: float = Form(0.0),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    denom = {"500": d500, "200": d200, "100": d100, "50": d50, "20": d20, "10": d10, "coins": coins}
    total = d500*500 + d200*200 + d100*100 + d50*50 + d20*20 + d10*10 + coins

    entry = CashLedger(
        erp_date=today,
        location="OFFICE",
        amount=0,  # denomination entry is a check record, not a movement
        mode=PaymentMode.CASH,
        reason=CashReason.ADJUSTMENT,
        denomination=denom,
        actor_id=user["id"],
        notes=f"Denomination count. Total={total}. {notes or ''}"
    )
    db.add(entry)
    db.commit()
    return RedirectResponse("/office/dashboard", 302)
