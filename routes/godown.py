from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date
from data.db import get_conn

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/godown")
def godown(request: Request):
    return templates.TemplateResponse("godown.html", {"request": request})

@router.post("/godown/save")
def save(user: str = Form(...), filled: int = Form(...), empty: int = Form(...)):
    c = get_conn()
    c.execute(
        "INSERT INTO godown_physical(date,user,filled,empty) VALUES (?,?,?,?)",
        (date.today().isoformat(), user, filled, empty)
    )
    c.commit()
    c.close()
    return {"status": "saved"}
