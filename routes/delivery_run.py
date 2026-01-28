from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from services.scheduled_filter import get_pending_scheduled

router = APIRouter(prefix='/delivery', tags=['Delivery'])
templates = Jinja2Templates(directory='templates')

@router.get('/run')
def delivery_run(request: Request):
    deliveries = get_pending_scheduled('uploads/CashMemoGeneratedList.csv')
    return templates.TemplateResponse(
        'delivery_run.html',
        {'request': request, 'deliveries': deliveries}
    )
