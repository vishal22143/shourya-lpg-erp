from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.services.delivery_payroll import apply_recovery_and_pay, PayrollError

router = APIRouter(prefix='/delivery-payroll', tags=['Delivery Payroll'])

@router.post('/pay')
def pay_delivery_salary(
    delivery_man_id: int,
    month: str,
    agreed_recovery: int,
    payment_mode: str,
    pay_date: date,
    db: Session = Depends(get_db)
):
    try:
        res = apply_recovery_and_pay(
            db=db,
            delivery_man_id=delivery_man_id,
            month=month,
            agreed_recovery=agreed_recovery,
            payment_mode=payment_mode,
            pay_date=pay_date
        )
        commit_or_rollback(db)
        return res
    except PayrollError as e:
        raise HTTPException(status_code=400, detail=str(e))
