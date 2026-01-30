from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.tx import commit_or_rollback
from app.services.stock_atomic import atomic_move, StockError
from app.models.trip import DeliveryTrip, DeliverySale

router = APIRouter(prefix='/delivery', tags=['Delivery'])

@router.post('/trip/open')
def open_trip(delivery_man_id: int, db: Session = Depends(get_db)):
    trip = DeliveryTrip(
        delivery_man_id=delivery_man_id,
        date=date.today(),
        trip_no=1,
        status='OPEN'
    )
    db.add(trip)
    commit_or_rollback(db)
    return {'status': 'trip opened', 'trip_id': trip.id}

@router.post('/trip/sale')
def record_sale(
    trip_id: int,
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
            ref_type='DELIVERY',
            ref_id=trip_id
        )
        sale = DeliverySale(
            trip_id=trip_id,
            payment_mode=payment_mode,
            amount=amount
        )
        db.add(sale)
        commit_or_rollback(db)
        return {'status': 'sale recorded', 'trip_id': trip_id}
    except StockError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/trip/transfer')
def transfer_stock(
    trip_id: int,
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
            reason='TRANSFER',
            ref_type='DELIVERY',
            ref_id=trip_id
        )
        commit_or_rollback(db)
        return {'status': 'transfer recorded'}
    except StockError as e:
        raise HTTPException(status_code=400, detail=str(e))
