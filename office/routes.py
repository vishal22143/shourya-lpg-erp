from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/office")
templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
def office_dashboard(request: Request):
    return templates.TemplateResponse(
        "office/dashboard.html",
        {"request": request}
    )
