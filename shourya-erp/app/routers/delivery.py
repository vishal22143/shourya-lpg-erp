from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_login
from app.models.models import (
    Trip, TripStatus, DeliveryPool, DeliveryStatus, Vehicle,
    StockReason, CashReason, PaymentMode, StaffAdvance
)
from app.services.stock_service import add_stock_movement
from app.services.day_service import get_or_create_today
from app.services.wage_service import compute_wages_for_trip
from app.services.csv_service import import_csv, get_deliveries_for_trip
from datetime import date, datetime

router = APIRouter(prefix="/delivery", tags=["delivery"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def delivery_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["DELIVERY", "OWNER", "PARTNER", "OFFICE"]:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    # For DELIVERY role, show only their trips
    if user["role"] == "DELIVERY":
        trips = db.query(Trip).filter(
            Trip.erp_date == today,
            Trip.delivery_man_id == user["id"]
        ).all()
    else:
        trips = db.query(Trip).filter(Trip.erp_date == today).all()

    vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).all()
    open_trip = next((t for t in trips if t.status == TripStatus.OPEN), None)

    return templates.TemplateResponse("delivery/dashboard.html", {
        "request": request,
        "user": user,
        "today": today,
        "trips": trips,
        "vehicles": vehicles,
        "open_trip": open_trip,
    })


@router.post("/open-trip")
def open_trip(
    request: Request,
    vehicle_id:     int = Form(...),
    filled_issued:  int = Form(...),
    db: Session         = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["DELIVERY", "OWNER", "PARTNER"]:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    get_or_create_today(db, user["id"])

    # Check no existing open trip for this delivery man today
    existing = db.query(Trip).filter(
        Trip.erp_date == today,
        Trip.delivery_man_id == user["id"],
        Trip.status == TripStatus.OPEN
    ).first()
    if existing:
        return RedirectResponse("/delivery/dashboard", 302)

    trip = Trip(
        erp_date=today,
        delivery_man_id=user["id"],
        vehicle_id=vehicle_id,
        filled_issued=filled_issued,
        status=TripStatus.OPEN
    )
    db.add(trip)
    db.flush()

    # Stock movement: GODOWN → VEHICLE
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    vehicle_loc = f"VEHICLE_{vehicle_id}"
    add_stock_movement(db, today, "5350", "GODOWN", -filled_issued, True,
                       StockReason.VEHICLE_ISSUE, "TRIP", trip.id, user["id"])
    add_stock_movement(db, today, "5350", vehicle_loc, filled_issued, True,
                       StockReason.VEHICLE_ISSUE, "TRIP", trip.id, user["id"])

    db.commit()
    return RedirectResponse(f"/delivery/trip/{trip.id}", 302)


@router.get("/trip/{trip_id}", response_class=HTMLResponse)
def trip_view(trip_id: int, request: Request, area: str = None, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user

    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return RedirectResponse("/delivery/dashboard", 302)

    today = date.today()
    deliveries = get_deliveries_for_trip(db, today, area)
    areas = db.query(DeliveryPool.area).filter(
        DeliveryPool.erp_date == today
    ).distinct().all()
    areas = [a[0] for a in areas if a[0]]

    return templates.TemplateResponse("delivery/trip.html", {
        "request": request,
        "user": user,
        "trip": trip,
        "deliveries": deliveries,
        "areas": areas,
        "selected_area": area,
        "today": today,
    })


@router.post("/deliver/{delivery_id}")
def mark_delivered(
    delivery_id: int,
    request: Request,
    trip_id:        int  = Form(...),
    otp:            str  = Form(None),
    payment_mode:   str  = Form("CASH"),
    amount:         float = Form(0.0),
    emergency:      bool = Form(False),
    db: Session          = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user

    delivery = db.query(DeliveryPool).filter(DeliveryPool.id == delivery_id).first()
    trip     = db.query(Trip).filter(Trip.id == trip_id).first()

    if not delivery or not trip:
        return RedirectResponse(f"/delivery/trip/{trip_id}", 302)

    delivery.status       = DeliveryStatus.DELIVERED_EMERGENCY if emergency else DeliveryStatus.DELIVERED
    delivery.otp          = otp
    delivery.payment_mode = PaymentMode(payment_mode)
    delivery.amount_collected = amount
    delivery.delivered_by = user["id"]
    delivery.delivered_at = datetime.now()
    delivery.trip_id      = trip_id

    # Update trip totals
    trip.total_sales += 1
    if payment_mode == "CASH":
        trip.cash_collected += amount
    elif payment_mode == "ONLINE":
        trip.online_collected += amount
    elif payment_mode == "MIXED":
        trip.cash_collected += amount  # caller should split — simplified

    # Stock movement: VEHICLE → CUSTOMER (one filled out, one empty in)
    vehicle_loc = f"VEHICLE_{trip.vehicle_id}"
    add_stock_movement(db, date.today(), "5350", vehicle_loc, -1, True,
                       StockReason.SALE, "TRIP", trip_id, user["id"])
    add_stock_movement(db, date.today(), "5370", vehicle_loc, 1, False,
                       StockReason.SALE, "TRIP", trip_id, user["id"])

    db.commit()
    return RedirectResponse(f"/delivery/trip/{trip_id}", 302)


@router.post("/close-trip/{trip_id}")
def close_trip(
    trip_id: int,
    request: Request,
    empty_returned: int = Form(0),
    cash_collected: float = Form(0),
    online_collected: float = Form(0),
    db: Session = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user

    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip or trip.status != TripStatus.OPEN:
        return RedirectResponse("/delivery/dashboard", 302)

    trip.status          = TripStatus.CLOSED
    trip.empty_returned  = empty_returned
    trip.cash_collected  = cash_collected
    trip.online_collected = online_collected
    trip.closed_at       = datetime.now()

    # Stock: empty cylinders back to godown
    if empty_returned > 0:
        vehicle_loc = f"VEHICLE_{trip.vehicle_id}"
        add_stock_movement(db, date.today(), "5370", vehicle_loc, -empty_returned, False,
                           StockReason.VEHICLE_RETURN, "TRIP", trip_id, user["id"])
        add_stock_movement(db, date.today(), "5370", "GODOWN", empty_returned, False,
                           StockReason.VEHICLE_RETURN, "TRIP", trip_id, user["id"])

    # Check cash shortage → auto advance
    expected_cash = trip.total_sales * 998  # approx, real check should be per delivery
    if cash_collected < (trip.cash_collected - 100):  # tolerance ₹100
        shortage = trip.cash_collected - cash_collected
        advance = StaffAdvance(
            erp_date=date.today(),
            staff_id=trip.delivery_man_id,
            amount=shortage,
            source="CASH_SHORT_ADJUSTMENT",
            created_by=user["id"],
            notes=f"Auto: cash short on trip {trip_id}"
        )
        db.add(advance)

    db.commit()

    # Auto-compute wages
    compute_wages_for_trip(db, trip)

    return RedirectResponse("/delivery/dashboard", 302)


@router.get("/upload-csv", response_class=HTMLResponse)
def upload_csv_page(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["OWNER", "PARTNER", "OFFICE"]:
        return RedirectResponse("/access-denied", 302)
    return templates.TemplateResponse("delivery/upload_csv.html", {
        "request": request, "user": user, "result": None
    })


@router.post("/upload-csv")
async def upload_csv(
    request: Request,
    csv_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ["OWNER", "PARTNER", "OFFICE"]:
        return RedirectResponse("/access-denied", 302)

    content = await csv_file.read()
    result  = import_csv(db, content, date.today(), user["id"])

    return templates.TemplateResponse("delivery/upload_csv.html", {
        "request": request, "user": user, "result": result
    })
