from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/owner", response_class=HTMLResponse)
def owner_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "OWNER"}
    )

@router.get("/office", response_class=HTMLResponse)
def office_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "OFFICE"}
    )

@router.get("/godown", response_class=HTMLResponse)
def godown_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "GODOWN"}
    )

@router.get("/delivery", response_class=HTMLResponse)
def delivery_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "DELIVERY"}
    )
