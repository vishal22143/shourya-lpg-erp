from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.reports import (
    report_delivery_salary,
    report_advance_breakup,
    report_day_end
)

router = APIRouter(prefix='/reports', tags=['Reports'])

@router.get('/delivery-salary')
def delivery_salary(month: str, db: Session = Depends(get_db)):
    return report_delivery_salary(db, month)

@router.get('/advance-breakup')
def advance_breakup(delivery_man_id: int, db: Session = Depends(get_db)):
    return report_advance_breakup(db, delivery_man_id)

@router.get('/day-end')
def day_end(on_date: date, db: Session = Depends(get_db)):
    return report_day_end(db, on_date)
