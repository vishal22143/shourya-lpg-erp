from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from office.routes.office_sales import router as sales_router

router = APIRouter(prefix='/office')
router.include_router(sales_router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

@router.get('', response_class=HTMLResponse)
async def office_home(request: Request):
    return templates.TemplateResponse('office_home.html', {'request': request})
