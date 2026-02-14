from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

ROLE_PREFIX = {
    "OWNER": "/owner",
    "ADMIN": "/owner",
    "OFFICE": "/office",
    "GODOWN": "/godown",
    "DELIVERY": "/delivery",
}

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

def _find_valid_route(app, prefix):
    for r in app.routes:
        if hasattr(r, "path") and r.path.startswith(prefix):
            if r.path != prefix:
                return r.path
    return prefix  # fallback

@router.post("/login")
def login_action(
    request: Request,
    username: str = Form(...),
    role: str = Form(...)
):
    request.session["user"] = username
    request.session["role"] = role.upper()

    app = request.app
    prefix = ROLE_PREFIX.get(role.upper(), "/login")
    target = _find_valid_route(app, prefix)

    return RedirectResponse(\1, status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
