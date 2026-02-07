from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse

def require_login(role: str = None):
    def guard(request: Request):
        if "user" not in request.session:
            return RedirectResponse("/login")
        if role and request.session.get("role") != role:
            return JSONResponse({"error": "Forbidden"}, status_code=403)
    return guard

def mount_ui(app: FastAPI):
    from app.routers.owner import router as owner_router
    from app.routers.office import router as office_router
    from app.routers.phase6_layerB_full import router as godown_router
    from app.routers.delivery import router as delivery_router

    app.include_router(owner_router, prefix="/owner", dependencies=[require_login("OWNER")])
    app.include_router(office_router, prefix="/office", dependencies=[require_login("OFFICE")])
    app.include_router(godown_router, prefix="/godown", dependencies=[require_login("GODOWN")])
    app.include_router(delivery_router, prefix="/delivery", dependencies=[require_login("DELIVERY")])
