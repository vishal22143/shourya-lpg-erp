from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles

from data.db import init_db
from routes import dashboard
from routes import delivery
from routes import godown_operational
from routes import delivery
from routes import godown_strict
from routes import delivery

app = FastAPI(title="Shourya LPG ERP – Godown")

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(dashboard.router)
app.include_router(delivery.router)
app.include_router(godown_operational.router)
app.include_router(delivery.router)
app.include_router(godown_strict.router)
app.include_router(delivery.router)

from routes.office_dashboard import router as office_router

app.include_router(office_router)
app.include_router(delivery.router)


from routes import delivery
app.include_router(delivery.router)


from utils.bpcl_csv import read_bpcl_scheduled_list
from fastapi import UploadFile, File

@app.post('/delivery/scheduled')
async def upload_scheduled(request: Request, file: UploadFile = File(...)):
    import os
    os.makedirs('uploads', exist_ok=True)
    path = f'uploads/{file.filename}'
    with open(path,'wb') as f:
        f.write(await file.read())

    deliveries = read_bpcl_scheduled_list(path)
    return templates.TemplateResponse(
        'scheduled_list.html',
        {'request': request, 'deliveries': deliveries}
    )


@app.get('/delivery/upload')
async def upload_page(request: Request):
    return templates.TemplateResponse(
        'upload_scheduled.html',
        {'request': request}
    )


templates = Jinja2Templates(directory='templates')



from routes.delivery_run import router as delivery_run_router
app.include_router(delivery_run_router)


from routes.delivery_actions import router as delivery_actions_router
app.include_router(delivery_actions_router)


from app.routers import delivery, bda, stock, owner

app.include_router(delivery.router)
app.include_router(bda.router)
app.include_router(stock.router)
app.include_router(owner.router)

# ---- DB INIT (SAFE) ----
from app.core.init_db import init_db
init_db()

from app.routers.office_cash import router as office_cash_router
app.include_router(office_cash_router)

from app.routers.delivery_payroll import router as delivery_payroll_router
app.include_router(delivery_payroll_router)
