from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.services.day_end import run_day_end, DayEndError
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

@router.post('/day-end/run')
def day_end_run(on_date: date | None = None, db: Session = Depends(get_db)):
    try:
        result = run_day_end(db, on_date)
        commit_or_rollback(db)
        return result
    except DayEndError as e:
        raise HTTPException(status_code=400, detail=str(e))
