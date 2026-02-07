from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import importlib

def mount_ui(app: FastAPI):

    def _import_router(path):
        try:
            mod = importlib.import_module(path)
            return getattr(mod, "router", None)
        except Exception:
            return None

    # OWNER (S5)
    owner_router = _import_router("app.routers.owner")
    if owner_router:
        app.include_router(owner_router, prefix="/owner")

    # OFFICE (S2)
    office_router = _import_router("app.routers.office_cash")
    if office_router:
        app.include_router(office_router, prefix="/office")

    # GODOWN / STOCK (S3)
    stock_router = _import_router("app.routers.stock")
    if stock_router:
        app.include_router(stock_router, prefix="/godown")

    # DELIVERY (S4)
    delivery_router = _import_router("app.routers.delivery")
    if delivery_router:
        app.include_router(delivery_router, prefix="/delivery")

    # LANDING ROUTES
    from app.routers.landing import router as landing_router
    app.include_router(landing_router)

    from app.routers.role_home import router as role_home_router
    app.include_router(role_home_router)

    from app.routers.role_home import router as role_home_router
    app.include_router(role_home_router)
