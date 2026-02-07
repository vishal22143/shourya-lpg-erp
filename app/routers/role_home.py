from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def _links(app, prefix):
    return sorted({
        r.path for r in app.routes
        if r.path.startswith(prefix) and "{" not in r.path
    })

@router.get("/owner", response_class=HTMLResponse)
def owner_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "OWNER", "links": _links(request.app, "/owner/")}
    )

@router.get("/office", response_class=HTMLResponse)
def office_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "OFFICE", "links": _links(request.app, "/office/")}
    )

@router.get("/godown", response_class=HTMLResponse)
def godown_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "GODOWN", "links": _links(request.app, "/godown/")}
    )

@router.get("/delivery", response_class=HTMLResponse)
def delivery_home(request: Request):
    return templates.TemplateResponse(
        "role_home.html",
        {"request": request, "role": "DELIVERY", "links": _links(request.app, "/delivery/")}
    )
