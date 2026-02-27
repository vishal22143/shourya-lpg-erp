from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_pin, ROLE_LANDING
from app.models.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("user"):
        role = request.session["user"]["role"]
        return RedirectResponse(ROLE_LANDING.get(role, "/login"), 302)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def login_submit(
    request: Request,
    mobile: str = Form(...),
    pin: str    = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.mobile == mobile, User.is_active == True).first()
    if not user or not verify_pin(pin, user.pin_hash):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "चुकीचा मोबाईल नंबर किंवा PIN / Wrong mobile or PIN"
        })
    request.session["user"] = {
        "id":    user.id,
        "name":  user.name,
        "role":  user.role.value,
        "mobile": user.mobile
    }
    return RedirectResponse(ROLE_LANDING.get(user.role.value, "/login"), 302)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", 302)


@router.get("/access-denied", response_class=HTMLResponse)
def access_denied(request: Request):
    return templates.TemplateResponse("access_denied.html", {"request": request})
