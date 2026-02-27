from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.core.database import engine, Base
from app.core.config import SECRET_KEY
from app.routers import auth, godown, delivery, office, owner, bda
import os

# Create all tables on startup (safe — only creates missing tables)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shourya Bharatgas ERP",
    description="BPCL LPG Distributor ERP — Jaysingpur",
    version="1.0.0"
)

# Session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=86400)

# Static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Register all routers
app.include_router(auth.router)
app.include_router(godown.router)
app.include_router(delivery.router)
app.include_router(office.router)
app.include_router(owner.router)
app.include_router(bda.router)


@app.get("/")
def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/login", status_code=302)


@app.get("/health")
def health():
    return {"status": "ok", "service": "Shourya Bharatgas ERP"}
