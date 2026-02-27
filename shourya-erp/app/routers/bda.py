from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_login
from app.models.models import (
    BdaTransaction, BdaMaster, Trip, StockReason,
    DeliveryPool, DeliveryStatus, PaymentMode, User
)
from app.services.stock_service import add_stock_movement
from datetime import date, datetime

router = APIRouter(prefix="/bda", tags=["bda"])
templates = Jinja2Templates(directory="app/templates")


# ── BDA PORTAL (for BDA owners logging in on their mobile) ─────────────────

@router.get("/portal", response_class=HTMLResponse)
def bda_portal(request: Request, db: Session = Depends(get_db)):
    """BDA owner's own mobile portal — see their pending deliveries, capture OTP, spot delivery"""
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["BDA", "OWNER", "PARTNER", "OFFICE"]:
        return RedirectResponse("/access-denied", 302)

    today = date.today()

    # Find the BDA record linked to this user's mobile
    bda_record = db.query(BdaMaster).filter(BdaMaster.mobile == user["mobile"]).first()
    # If owner/office is viewing, show all BDAs
    all_bdas = db.query(BdaMaster).filter(BdaMaster.is_active == True).all()

    # Pending deliveries for this BDA's village/area
    pending = []
    if bda_record:
        pending = db.query(DeliveryPool).filter(
            DeliveryPool.erp_date == today,
            DeliveryPool.status == DeliveryStatus.SCHEDULED,
            DeliveryPool.area.ilike(f"%{bda_record.village}%")
        ).all()
    elif user["role"] in ["OWNER", "PARTNER", "OFFICE"]:
        pending = db.query(DeliveryPool).filter(
            DeliveryPool.erp_date == today,
            DeliveryPool.status == DeliveryStatus.SCHEDULED
        ).limit(50).all()

    # Today's transactions for this BDA
    txns = []
    if bda_record:
        txns = db.query(BdaTransaction).filter(
            BdaTransaction.erp_date == today,
            BdaTransaction.bda_id == bda_record.id
        ).all()

    # BDA current stock (from ledger)
    from app.services.stock_service import get_location_stock
    bda_stock = {}
    if bda_record:
        bda_stock = get_location_stock(db, f"BDA_{bda_record.id}", today)

    return templates.TemplateResponse("bda/portal.html", {
        "request": request,
        "user": user,
        "today": today,
        "bda_record": bda_record,
        "all_bdas": all_bdas,
        "pending": pending,
        "txns": txns,
        "bda_stock": bda_stock,
    })


@router.post("/capture-otp/{delivery_id}")
def bda_capture_otp(
    delivery_id: int,
    request: Request,
    otp: str         = Form(...),
    payment_mode: str = Form("CASH"),
    amount: float    = Form(856.0),
    db: Session      = Depends(get_db)
):
    """BDA captures OTP for a customer who collected from BDA point"""
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["BDA", "OWNER", "PARTNER", "OFFICE", "DELIVERY"]:
        return RedirectResponse("/access-denied", 302)

    delivery = db.query(DeliveryPool).filter(DeliveryPool.id == delivery_id).first()
    if not delivery:
        return RedirectResponse("/bda/portal", 302)

    delivery.status           = DeliveryStatus.DELIVERED
    delivery.otp              = otp
    delivery.payment_mode     = PaymentMode(payment_mode)
    delivery.amount_collected = amount
    delivery.delivered_by     = user["id"]
    delivery.delivered_at     = datetime.now()

    db.commit()
    return RedirectResponse("/bda/portal", 302)


@router.post("/spot-delivery")
def bda_spot_delivery(
    request: Request,
    consumer_name: str = Form(...),
    consumer_no:   str = Form(""),
    mobile:        str = Form(""),
    payment_mode:  str = Form("CASH"),
    cash_amount:   float = Form(0.0),
    online_amount: float = Form(0.0),
    bda_id:        int   = Form(None),
    notes:         str   = Form(None),
    db: Session          = Depends(get_db)
):
    """Spot/urgent delivery from BDA — customer did NOT book via BPCL"""
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["BDA", "DELIVERY", "OWNER", "PARTNER", "OFFICE"]:
        return RedirectResponse("/access-denied", 302)

    today = date.today()

    # Find BDA
    if not bda_id:
        bda = db.query(BdaMaster).filter(BdaMaster.mobile == user["mobile"]).first()
        bda_id = bda.id if bda else None

    # Create an ad-hoc delivery pool entry (no OTP — spot delivery)
    spot = DeliveryPool(
        erp_date=today,
        consumer_no=consumer_no or f"SPOT-{int(datetime.now().timestamp())}",
        consumer_name=consumer_name,
        mobile=mobile,
        area="SPOT",
        booking_type="SPOT",
        product_code="5350",
        status=DeliveryStatus.DELIVERED_EMERGENCY,  # no OTP
        payment_mode=PaymentMode(payment_mode),
        amount_collected=cash_amount + online_amount,
        delivered_by=user["id"],
        delivered_at=datetime.now(),
        remarks=f"Spot delivery via BDA. {notes or ''}".strip(),
        # No lat/lng saved — customer was not at doorstep
    )
    db.add(spot)

    # Record cash in BDA transaction
    if bda_id:
        txn = BdaTransaction(
            erp_date=today,
            bda_id=bda_id,
            filled_issued=1,
            empty_received=0,
            cash_paid=cash_amount,
            online_paid=online_amount,
            created_by=user["id"],
            notes=f"Spot: {consumer_name}. {notes or ''}"
        )
        db.add(txn)
        # Stock movement
        add_stock_movement(db, today, "5350", f"BDA_{bda_id}", -1, True,
                           StockReason.SALE, "BDA_SPOT", 0, user["id"])
        add_stock_movement(db, today, "5370", f"BDA_{bda_id}", 1, False,
                           StockReason.SALE, "BDA_SPOT", 0, user["id"])

    db.commit()
    return RedirectResponse("/bda/portal", 302)


# ── BDA DASHBOARD (for office/delivery staff managing BDA) ──────────────────

@router.get("/dashboard", response_class=HTMLResponse)
def bda_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["OWNER", "PARTNER", "OFFICE", "DELIVERY", "BDA"]:
        return RedirectResponse("/access-denied", 302)

    today    = date.today()
    bdas     = db.query(BdaMaster).filter(BdaMaster.is_active == True).all()
    txns     = db.query(BdaTransaction).filter(BdaTransaction.erp_date == today).all()

    return templates.TemplateResponse("bda/dashboard.html", {
        "request": request,
        "user": user,
        "today": today,
        "bdas": bdas,
        "txns": txns,
    })


@router.post("/transaction")
def add_bda_transaction(
    request: Request,
    bda_id:           int   = Form(...),
    trip_id:          int   = Form(None),
    filled_issued:    int   = Form(0),
    empty_received:   int   = Form(0),
    cash_paid:        float = Form(0.0),
    online_paid:      float = Form(0.0),
    cash_receiver_id: int   = Form(None),
    notes: str              = Form(None),
    db: Session             = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user

    today = date.today()
    bda   = db.query(BdaMaster).filter(BdaMaster.id == bda_id).first()
    if not bda:
        return RedirectResponse("/bda/dashboard", 302)

    txn = BdaTransaction(
        erp_date=today,
        bda_id=bda_id,
        trip_id=trip_id,
        filled_issued=filled_issued,
        empty_received=empty_received,
        cash_paid=cash_paid,
        online_paid=online_paid,
        cash_receiver_id=cash_receiver_id,
        created_by=user["id"],
        notes=notes
    )
    db.add(txn)

    bda_loc = f"BDA_{bda_id}"
    if filled_issued > 0:
        source_loc = f"VEHICLE_{trip_id}" if trip_id else "GODOWN"
        add_stock_movement(db, today, "5350", source_loc, -filled_issued, True,
                           StockReason.BDA_ISSUE, "BDA", 0, user["id"])
        add_stock_movement(db, today, "5350", bda_loc, filled_issued, True,
                           StockReason.BDA_ISSUE, "BDA", 0, user["id"])
    if empty_received > 0:
        add_stock_movement(db, today, "5370", bda_loc, -empty_received, False,
                           StockReason.BDA_RETURN, "BDA", 0, user["id"])
        add_stock_movement(db, today, "5370", "GODOWN", empty_received, False,
                           StockReason.BDA_RETURN, "BDA", 0, user["id"])

    if trip_id:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if trip:
            trip.bda_cash   += cash_paid
            trip.bda_online += online_paid

    db.commit()
    return RedirectResponse("/bda/dashboard", 302)

