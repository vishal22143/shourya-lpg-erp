from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.delivery import router as delivery_router
from app.routers.bda import router as bda_router
from app.routers.office_cash import router as office_cash_router
from app.routers.owner import router as owner_router
from app.routers.stock import router as stock_router
from app.routers.delivery_payroll import router as delivery_payroll_router
from app.routers.day_end import router as day_end_router
from app.routers.reports import router as reports_router
from app.routers.ui import router as ui_router

app = FastAPI(title='Shourya LPG ERP')

app.include_router(auth_router)
app.include_router(owner_router)
app.include_router(delivery_router)
app.include_router(bda_router)
app.include_router(office_cash_router)
app.include_router(stock_router)
app.include_router(delivery_payroll_router)
app.include_router(day_end_router)
app.include_router(reports_router)
app.include_router(ui_router)

@app.get('/')
def root():
    return {'status': 'ERP running'}
