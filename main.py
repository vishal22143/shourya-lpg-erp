from fastapi import FastAPI

from app.routers.s3_delivery_router import router as delivery_router
from app.routers.s3_cash_router import router as cash_router
from app.routers.s3_wages_router import router as wages_router
from app.routers.s4_csv_router import router as csv_router
from app.routers.s4_map_router import router as map_router
from app.routers.s5_owner.owner_day_end_router import router as owner_router

app = FastAPI(title="SHOURYA LPG ERP")

app.include_router(delivery_router)
app.include_router(cash_router)
app.include_router(wages_router)
app.include_router(csv_router)
app.include_router(map_router)
app.include_router(owner_router)

@app.get("/")
def root():
    return {
        "status": "ERP RUNNING",
        "modules": [
            "S3.1 DELIVERY",
            "S3.2 CASH & ADVANCE",
            "S3.3 WAGES",
            "S4.1 BPCL CSV",
            "S4.2 MAP & AREA",
            "S5.1 OWNER DAY-END"
        ],
        "state": "LOCKED"
    }
# ---- OWNER DAY-END ROUTER (S5.1-C-2) ----
from routes.owner_dayend import router as owner_dayend_router
app.include_router(owner_dayend_router)
