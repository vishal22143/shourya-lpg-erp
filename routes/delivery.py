from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from services.scheduled_filter import get_pending_scheduled

router = APIRouter(prefix='/delivery', tags=['Delivery'])
templates = Jinja2Templates(directory='templates')

@router.get('/scheduled')
def scheduled_list(request: Request):
    deliveries = get_pending_scheduled('uploads/CashMemoGeneratedList.csv')
    return templates.TemplateResponse(
        'scheduled_list.html',
        {'request': request, 'deliveries': deliveries}
    )
