from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(prefix='/office')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

@router.get('/sales', response_class=HTMLResponse)
async def sales_page(request: Request):
    return templates.TemplateResponse('office_sales.html', {'request': request})

@router.post('/sales')
async def save_sales(
    request: Request,
    refill_cash: int = Form(0),
    refill_online: int = Form(0),
    sv: int = Form(0),
    pipe: int = Form(0),
    book: int = Form(0),
    dpr_paid: int = Form(0),
    dpr_free: int = Form(0),
):
    # Logic already modeled in office_sales.py (hook later)
    return RedirectResponse('/office', status_code=303)
