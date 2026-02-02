from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.services.stock_atomic import atomic_move, StockError
from app.models.bda import BDASale
from app.models.cash import CashHandover

router = APIRouter(prefix='/bda', tags=['BDA'])

@router.post('/sale')
def bda_sale(
    bda_id: int,
    from_location: int,
    to_location: int,
    payment_mode: str,
    amount: int,
    db: Session = Depends(get_db)
):
    try:
        # 1 filled out, 1 empty in
        atomic_move(
            db=db,
            from_location=from_location,
            to_location=to_location,
            filled_qty=1,
            empty_qty=1,
            reason='SALE',
            ref_type='BDA',
            ref_id=bda_id
        )
        sale = BDASale(
            bda_id=bda_id,
            date=date.today(),
            payment_mode=payment_mode,
            amount=amount
        )
        db.add(sale)
        commit_or_rollback(db)
        return {'status': 'bda sale recorded'}
    except StockError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/cash/handover')
def bda_cash_handover(
    bda_id: int,
    amount: int,
    payment_mode: str,
    receiver_type: str,
    receiver_name: str,
    db: Session = Depends(get_db)
):
    ch = CashHandover(
        source_type='BDA',
        source_id=bda_id,
        amount=amount,
        payment_mode=payment_mode,
        receiver_type=receiver_type,
        receiver_name=receiver_name,
        date=date.today()
    )
    db.add(ch)
    commit_or_rollback(db)
    return {'status': 'handover recorded'}
