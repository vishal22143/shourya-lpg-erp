from fastapi import APIRouter
from services.delivery_actions import (
    start_trip,
    deliver_otp,
    deliver_emergency,
    cancel_delivery
)

router = APIRouter(prefix='/delivery', tags=['Delivery Actions'])

@router.post('/start/{cashmemo}')
def api_start_trip(cashmemo: str):
    start_trip(cashmemo)
    return {'ok': True}

@router.post('/deliver/otp/{cashmemo}')
def api_deliver_otp(cashmemo: str):
    deliver_otp(cashmemo)
    return {'ok': True}

@router.post('/deliver/emergency/{cashmemo}')
def api_deliver_emergency(cashmemo: str):
    deliver_emergency(cashmemo)
    return {'ok': True}

@router.post('/cancel/{cashmemo}')
def api_cancel(cashmemo: str):
    cancel_delivery(cashmemo)
    return {'ok': True}
