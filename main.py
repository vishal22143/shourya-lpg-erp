from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates

# ===============================
# APP INIT
# ===============================
app = FastAPI(title="Shourya LPG ERP")

# ===============================
# MIDDLEWARE
# ===============================
app.add_middleware(
    SessionMiddleware,
    secret_key="shourya-erp-secret"
)

# ===============================
# STATIC & TEMPLATES
# ===============================
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ===============================
# IMPORT ROUTERS (CORRECT PATHS)
# ===============================
from app.routers.auth import router as auth_router
from app.routers.owner import router as owner_router
from app.routers.office import router as office_router
from app.routers.delivery import router as delivery_router
from app.routers.ui import router as ui_router

# ===============================
# REGISTER ROUTERS
# ===============================
app.include_router(auth_router)
app.include_router(ui_router)

app.include_router(owner_router, prefix="/owner")
app.include_router(office_router, prefix="/office")
app.include_router(delivery_router, prefix="/delivery")

# ===============================
# ROOT → LOGIN
# ===============================
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/login")

# ===============================
# HEALTH CHECK
# ===============================
@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ERP BOOT OK"}
