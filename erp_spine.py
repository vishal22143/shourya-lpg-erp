from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

def build_erp_spine() -> FastAPI:
    app = FastAPI(title="Shourya LPG ERP")

    app.add_middleware(
        SessionMiddleware,
        secret_key="shourya-erp-secret"
    )

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse("/login")

    @app.get("/health", include_in_schema=False)
    def health():
        return {"status": "ERP BOOT OK"}

    return app
