from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_login
from app.models.models import (
    User, Vehicle, BdaMaster, Trip, WageEntry,
    DayEndSnapshot, ErpDay, DayStatus
)
from app.services.dayend_service import generate_day_end
from app.services.day_service import lock_day
from app.core.auth import hash_pin
from datetime import date

router = APIRouter(prefix="/owner", tags=["owner"])
templates = Jinja2Templates(directory="app/templates")

ALLOWED = ["OWNER", "PARTNER"]


@router.get("/dashboard", response_class=HTMLResponse)
def owner_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today = date.today()
    trips    = db.query(Trip).filter(Trip.erp_date == today).all()
    erp_day  = db.query(ErpDay).filter(ErpDay.date == today).first()
    wages    = db.query(WageEntry).filter(WageEntry.erp_date == today).all()
    snapshot = db.query(DayEndSnapshot).filter(DayEndSnapshot.erp_date == today).first()

    total_delivered = sum(t.total_sales for t in trips)
    total_cash      = sum(t.cash_collected + t.bda_cash for t in trips)
    total_online    = sum(t.online_collected + t.bda_online for t in trips)

    return templates.TemplateResponse("owner/dashboard.html", {
        "request": request,
        "user": user,
        "today": today,
        "trips": trips,
        "erp_day": erp_day,
        "wages": wages,
        "snapshot": snapshot,
        "total_delivered": total_delivered,
        "total_cash": total_cash,
        "total_online": total_online,
    })


@router.post("/generate-dayend")
def generate_dayend(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)
    generate_day_end(db, date.today(), user["id"])
    return RedirectResponse("/owner/dayend", 302)


@router.get("/dayend", response_class=HTMLResponse)
def dayend_view(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    today    = date.today()
    snapshot = db.query(DayEndSnapshot).filter(DayEndSnapshot.erp_date == today).first()
    erp_day  = db.query(ErpDay).filter(ErpDay.date == today).first()

    return templates.TemplateResponse("owner/dayend.html", {
        "request": request,
        "user": user,
        "today": today,
        "snapshot": snapshot,
        "erp_day": erp_day,
    })


@router.post("/lock-day")
def lock_day_route(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)
    lock_day(db, user["id"])
    return RedirectResponse("/owner/dayend", 302)


# ── ADMIN: User management ────────────────────────────────────────────────────

@router.get("/users", response_class=HTMLResponse)
def user_list(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)
    users = db.query(User).order_by(User.role).all()
    return templates.TemplateResponse("owner/users.html", {
        "request": request, "user": user, "users": users
    })


@router.post("/users/add")
def add_user(
    request: Request,
    name:       str   = Form(...),
    mobile:     str   = Form(...),
    role:       str   = Form(...),
    pin:        str   = Form(...),
    rate_urban: float = Form(5.0),
    rate_rural: float = Form(7.0),
    db: Session       = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)

    new_user = User(
        name=name,
        mobile=mobile,
        role=role,
        pin_hash=hash_pin(pin),
        rate_urban=rate_urban,
        rate_rural=rate_rural,
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse("/owner/users", 302)


@router.get("/vehicles", response_class=HTMLResponse)
def vehicles_list(request: Request, db: Session = Depends(get_db)):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)
    vehicles = db.query(Vehicle).all()
    drivers  = db.query(User).filter(User.role == "DELIVERY").all()
    return templates.TemplateResponse("owner/vehicles.html", {
        "request": request, "user": user, "vehicles": vehicles, "drivers": drivers
    })


@router.post("/vehicles/add")
def add_vehicle(
    request: Request,
    name:         str = Form(...),
    reg_number:   str = Form(None),
    capacity:     int = Form(55),
    extra_cap:    int = Form(10),
    default_driver_id: int = Form(None),
    db: Session       = Depends(get_db)
):
    user = require_login(request)
    if isinstance(user, RedirectResponse):
        return user
    if user["role"] not in ALLOWED:
        return RedirectResponse("/access-denied", 302)
    v = Vehicle(
        name=name, reg_number=reg_number, capacity=capacity,
        extra_cap=extra_cap, default_driver_id=default_driver_id
    )
    db.add(v)
    db.commit()
    return RedirectResponse("/owner/vehicles", 302)
