from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import importlib
import logging

log = logging.getLogger("erp-mount")

def require_login(role: str = None):
    def guard(request: Request):
        if "user" not in request.session:
            return RedirectResponse("/login")
        if role and request.session.get("role") != role:
            return JSONResponse({"error": "Forbidden"}, status_code=403)
    return guard

def _try_import(paths):
    for p in paths:
        try:
            mod = importlib.import_module(p)
            if hasattr(mod, "router"):
                log.info(f"Mounted router from {p}")
                return mod.router
        except ModuleNotFoundError:
            continue
    return None

def mount_ui(app: FastAPI):
    # OWNER (S5)
    owner_router = _try_import([
        "app.ui.s5_owner.router",
        "app.routers.owner",
    ])

    # OFFICE (S2)
    office_router = _try_import([
        "app.ui.s5_office.router",
        "app.routers.office",
    ])

    # GODOWN (S3)
    godown_router = _try_import([
        "app.routers.phase6_layerB_full",
        "app.ui.s3_godown.router",
        "app.routers.godown",
    ])

    # DELIVERY (S4)
    delivery_router = _try_import([
        "app.routers.delivery",
        "app.ui.s4_delivery.router",
    ])

    if owner_router:
        app.include_router(owner_router, prefix="/owner", dependencies=[require_login("OWNER")])
    if office_router:
        app.include_router(office_router, prefix="/office", dependencies=[require_login("OFFICE")])
    if godown_router:
        app.include_router(godown_router, prefix="/godown", dependencies=[require_login("GODOWN")])
    if delivery_router:
        app.include_router(delivery_router, prefix="/delivery", dependencies=[require_login("DELIVERY")])

    log.info("UI mount completed")
