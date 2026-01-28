from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
tpl = Jinja2Templates(directory="templates")

@router.get("/")
def dash(request: Request):
    return tpl.TemplateResponse("dashboard.html", {"request": request})
