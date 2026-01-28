from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date
from data.db import get_conn

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/accounting")
def accounting(request: Request):
    return templates.TemplateResponse("accounting.html", {"request": request})

@router.post("/accounting/save")
def save(cash: float = Form(...), digital: float = Form(...), denomination: str = Form(...)):
    c = get_conn()
    c.execute(
        "INSERT INTO accounting_day(date,cash,digital,denomination) VALUES (?,?,?,?)",
        (date.today().isoformat(), cash, digital, denomination)
    )
    c.commit()
    c.close()
    return {"status": "saved"}
