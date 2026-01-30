from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.delivery_payroll import DeliveryPayroll
from app.models.staff_advance import StaffAdvance
from app.models.office_cash import OfficeCashDay
from app.services.delivery_salary import compute_delivery_salary

class PayrollError(Exception):
    pass

def apply_recovery_and_pay(
    db: Session,
    delivery_man_id: int,
    month: str,
    agreed_recovery: int,
    payment_mode: str,
    pay_date: date
):
    calc = compute_delivery_salary(db, delivery_man_id, month)

    pending = calc['pending_advance']
    recover = min(agreed_recovery, pending, calc['gross'])
    net = calc['gross'] - recover

    # Recover advances FIFO
    to_recover = recover
    advances = db.query(StaffAdvance).filter(
        StaffAdvance.staff_type == 'DELIVERY',
        StaffAdvance.staff_id == delivery_man_id,
        StaffAdvance.amount > StaffAdvance.recovered
    ).order_by(StaffAdvance.date).all()

    for a in advances:
        if to_recover <= 0:
            break
        can = min(a.amount - a.recovered, to_recover)
        a.recovered += can
        to_recover -= can

    # Office cash impact
    if payment_mode == 'CASH':
        day = db.query(OfficeCashDay).filter(OfficeCashDay.date == pay_date).one()
        day.cash_out += net

    # Record payroll snapshot
    db.add(DeliveryPayroll(
        delivery_man_id=delivery_man_id,
        month=month,
        base_wage=calc['base_wage'],
        helper_days=calc['helper_days'],
        helper_amount=calc['helper_amount'],
        gross=calc['gross'],
        advance_recovered=recover,
        net_paid=net,
        payment_mode=payment_mode,
        payment_date=pay_date
    ))

    return {
        'gross': calc['gross'],
        'recovered': recover,
        'net_paid': net,
        'pending_advance_after': pending - recover
    }
