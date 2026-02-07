from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

ROLE_HOME = {
    "OWNER": "/owner",
    "ADMIN": "/owner",
    "OFFICE": "/office",
    "GODOWN": "/godown",
    "DELIVERY": "/delivery",
}

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_action(
    request: Request,
    username: str = Form(...),
    role: str = Form(...)
):
    request.session["user"] = username
    request.session["role"] = role.upper()
    return RedirectResponse(
        ROLE_HOME.get(role.upper(), "/login"),
        status_code=302
    )

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")
