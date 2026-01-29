from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/shell", response_class=HTMLResponse)
def shell_home(request: Request):
    role = request.session.get("role")

    if role == "OFFICE":
        return templates.TemplateResponse(
            "office/dashboard.html",
            {"request": request}
        )

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid role"}
    )
