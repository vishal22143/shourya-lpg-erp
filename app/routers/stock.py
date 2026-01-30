from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.services.stock_atomic import atomic_move, StockError

router = APIRouter(prefix='/stock', tags=['Stock'])

@router.post('/transfer')
def stock_transfer(
    from_location: int,
    to_location: int,
    filled_qty: int,
    empty_qty: int = 0,
    db: Session = Depends(get_db)
):
    try:
        atomic_move(
            db=db,
            from_location=from_location,
            to_location=to_location,
            filled_qty=filled_qty,
            empty_qty=empty_qty,
            reason='TRANSFER'
        )
        commit_or_rollback(db)
        return {'status': 'ok'}
    except StockError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/adjustment')
def stock_adjustment(
    location_id: int,
    filled_delta: int,
    empty_delta: int,
    reason: str,
    db: Session = Depends(get_db)
):
    try:
        atomic_move(
            db=db,
            from_location=location_id if filled_delta < 0 or empty_delta < 0 else None,
            to_location=location_id if filled_delta > 0 or empty_delta > 0 else None,
            filled_qty=abs(filled_delta),
            empty_qty=abs(empty_delta),
            reason=f'ADJUST:{reason}'
        )
        commit_or_rollback(db)
        return {'status': 'ok'}
    except StockError as e:
        raise HTTPException(status_code=400, detail=str(e))
