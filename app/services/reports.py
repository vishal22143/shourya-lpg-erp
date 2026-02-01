from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import DeliveryDaySummary
from app.models import DeliveryPayroll
from app.models import StaffAdvance
from app.models import OfficeCashDay
from app.models import StockDayEnd

# ---------- Delivery Salary (Month Summary) ----------
def report_delivery_salary(db: Session, month: str):
    rows = db.query(
        DeliveryPayroll.delivery_man_id,
        func.sum(DeliveryPayroll.base_wage).label('base_wage'),
        func.sum(DeliveryPayroll.helper_amount).label('helper_amount'),
        func.sum(DeliveryPayroll.gross).label('gross'),
        func.sum(DeliveryPayroll.advance_recovered).label('recovered'),
        func.sum(DeliveryPayroll.net_paid).label('net_paid')
    ).filter(
        DeliveryPayroll.month == month
    ).group_by(DeliveryPayroll.delivery_man_id).all()

    return [{
        'delivery_man_id': r.delivery_man_id,
        'base_wage': r.base_wage or 0,
        'helper_amount': r.helper_amount or 0,
        'gross': r.gross or 0,
        'recovered': r.recovered or 0,
        'net_paid': r.net_paid or 0,
        'labels': {
            'base_wage_mr': 'मूळ मजुरी',
            'helper_mr': 'अतिरिक्त मदतनीस',
            'gross_mr': 'एकूण मिळकत',
            'recovered_mr': 'वसूल',
            'net_mr': 'निव्वळ वेतन'
        }
    } for r in rows]

# ---------- Advance Breakup ----------
def report_advance_breakup(db: Session, delivery_man_id: int):
    rows = db.query(
        StaffAdvance.advance_type,
        func.sum(StaffAdvance.amount).label('amt'),
        func.sum(StaffAdvance.recovered).label('rec')
    ).filter(
        StaffAdvance.staff_type == 'DELIVERY',
        StaffAdvance.staff_id == delivery_man_id
    ).group_by(StaffAdvance.advance_type).all()

    data = []
    total = 0
    for r in rows:
        pending = (r.amt or 0) - (r.rec or 0)
        total += pending
        data.append({
            'type': r.advance_type,
            'amount': r.amt or 0,
            'recovered': r.rec or 0,
            'pending': pending
        })

    return {
        'breakup': data,
        'total_pending': total,
        'labels': {
            'emergency_mr': 'आकस्मिक आगाऊ',
            'cash_short_mr': 'कमी रोकड',
            'total_mr': 'एकूण आगाऊ'
        }
    }

# ---------- Day-end Cash vs Stock ----------
def report_day_end(db: Session, on_date):
    cash = db.query(OfficeCashDay).filter(OfficeCashDay.date == on_date).first()
    stock = db.query(
        func.sum(StockDayEnd.filled_qty).label('filled'),
        func.sum(StockDayEnd.empty_qty).label('empty')
    ).filter(StockDayEnd.date == on_date).one()

    return {
        'date': str(on_date),
        'cash': {
            'opening': cash.opening_cash if cash else 0,
            'expected': cash.closing_expected if cash else 0,
            'counted': cash.closing_counted if cash else 0,
            'difference': cash.difference if cash else 0,
            'status': cash.status if cash else 'N/A',
            'labels': {
                'opening_mr': 'उघडणी रोकड',
                'expected_mr': 'अपेक्षित',
                'counted_mr': 'मोजलेली',
                'diff_mr': 'फरक'
            }
        },
        'stock': {
            'filled': stock.filled or 0,
            'empty': stock.empty or 0,
            'labels': {
                'filled_mr': 'भरलेली',
                'empty_mr': 'रिकामी'
            }
        }
    }
