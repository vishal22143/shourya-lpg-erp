from datetime import date
from sqlalchemy.orm import Session
from app.models import OfficeCashDay
from app.models import CashDenomination

def denom_total(d):
    return (
        d.n2000*2000 + d.n500*500 + d.n200*200 + d.n100*100 +
        d.n50*50 + d.n20*20 + d.n10*10 + d.coins
    )

def close_cash_day(db: Session, on_date: date):
    day = db.query(OfficeCashDay).filter(OfficeCashDay.date == on_date).one()
    denom = db.query(CashDenomination).filter(CashDenomination.date == on_date).one()

    day.closing_counted = denom_total(denom)
    day.closing_expected = day.opening_cash + day.cash_in - day.cash_out
    day.difference = day.closing_counted - day.closing_expected

    if day.difference == 0:
        day.status = 'OK'
    elif day.difference < 0:
        day.status = 'SHORT'
    else:
        day.status = 'EXCESS'

    return {
        'expected': day.closing_expected,
        'counted': day.closing_counted,
        'difference': day.difference,
        'status': day.status
    }
