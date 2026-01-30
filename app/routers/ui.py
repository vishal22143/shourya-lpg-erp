from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.reports import report_delivery_salary, report_advance_breakup, report_day_end

templates = Jinja2Templates(directory='app/templates')
router = APIRouter(prefix='/ui', tags=['UI'])

@router.get('/owner')
def owner_dashboard(request: Request, month: str, on_date: date, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        'dashboard/owner.html',
        {
            'request': request,
            'title': 'Owner / Partner Dashboard',
            'salary': report_delivery_salary(db, month),
            'day': report_day_end(db, on_date)
        }
    )

@router.get('/accounts')
def accounts_dashboard(request: Request, delivery_man_id: int, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        'dashboard/accounts.html',
        {
            'request': request,
            'title': 'Accounts Dashboard',
            'adv': report_advance_breakup(db, delivery_man_id)
        }
    )
