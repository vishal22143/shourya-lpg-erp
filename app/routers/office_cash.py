from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.models.office_cash import OfficeCashDay
from app.models.office_expense import OfficeExpense
from app.models.staff_advance import StaffAdvance
from app.models.cash_denomination import CashDenomination
from app.services.cash_register import close_cash_day

router = APIRouter(prefix='/office-cash', tags=['Office Cash'])

@router.post('/open')
def open_day(opening_cash: int, on_date: date, db: Session = Depends(get_db)):
    day = OfficeCashDay(date=on_date, opening_cash=opening_cash)
    db.add(day); commit_or_rollback(db)
    return {'status': 'opened'}

@router.post('/expense')
def add_expense(head: str, amount: int, remark: str, on_date: date, db: Session = Depends(get_db)):
    db.add(OfficeExpense(date=on_date, head=head, amount=amount, remark=remark))
    day = db.query(OfficeCashDay).filter(OfficeCashDay.date == on_date).one()
    day.cash_out += amount
    commit_or_rollback(db)
    return {'status': 'expense added'}

@router.post('/advance')
def pay_advance(staff_id: int, amount: int, on_date: date, db: Session = Depends(get_db)):
    db.add(StaffAdvance(staff_type='DELIVERY', staff_id=staff_id, date=on_date, amount=amount))
    day = db.query(OfficeCashDay).filter(OfficeCashDay.date == on_date).one()
    day.cash_out += amount
    commit_or_rollback(db)
    return {'status': 'advance paid'}

@router.post('/denomination')
def set_denomination(
    on_date: date, n2000:int=0,n500:int=0,n200:int=0,n100:int=0,n50:int=0,n20:int=0,n10:int=0,coins:int=0,
    db: Session = Depends(get_db)
):
    db.add(CashDenomination(date=on_date,n2000=n2000,n500=n500,n200=n200,n100=n100,n50=n50,n20=n20,n10=n10,coins=coins))
    commit_or_rollback(db)
    return {'status': 'denomination set'}

@router.post('/close')
def close_day(on_date: date, db: Session = Depends(get_db)):
    res = close_cash_day(db, on_date)
    commit_or_rollback(db)
    return res
