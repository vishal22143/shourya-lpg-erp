from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from auth.login import router as login_router
from shell.routes import router as shell_router
from office.routes import router as office_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="shourya-secret-key"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(login_router)
app.include_router(shell_router)
app.include_router(office_router)

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/login")
