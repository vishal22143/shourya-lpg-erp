from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import importlib

# ---------- GLOBAL LOGIN MIDDLEWARE ----------
class LoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow public paths
        if path.startswith("/login") or path.startswith("/health") or path.startswith("/static"):
            return await call_next(request)

        # Require session for everything else
        if "user" not in request.session:
            return RedirectResponse("/login")

        return await call_next(request)

# ---------- SAFE IMPORT ----------
def _import_router(path):
    try:
        mod = importlib.import_module(path)
        return getattr(mod, "router", None)
    except Exception:
        return None

def mount_ui(app: FastAPI):
    # Attach middleware ONCE
    app.add_middleware(LoginMiddleware)

    # OWNER
    owner_router = _import_router("app.routers.owner")
    if owner_router:
        app.include_router(owner_router, prefix="/owner")

    # OFFICE
    office_router = _import_router("app.routers.office_cash")
    if office_router:
        app.include_router(office_router, prefix="/office")

    # GODOWN / STOCK
    stock_router = _import_router("app.routers.stock")
    if stock_router:
        app.include_router(stock_router, prefix="/godown")

    # DELIVERY
    delivery_router = _import_router("app.routers.delivery")
    if delivery_router:
        app.include_router(delivery_router, prefix="/delivery")
