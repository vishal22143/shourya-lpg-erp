from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/office")
def office(request: Request):
    return templates.TemplateResponse("office.html", {"request": request})
