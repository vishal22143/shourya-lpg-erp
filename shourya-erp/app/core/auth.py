from passlib.context import CryptContext
from starlette.requests import Request
from starlette.responses import RedirectResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ROLE_LANDING = {
    "OWNER":    "/owner/dashboard",
    "PARTNER":  "/owner/dashboard",
    "OFFICE":   "/office/dashboard",
    "DELIVERY": "/delivery/dashboard",
    "LOADER":   "/godown/dashboard",
    "BDA":      "/bda/portal",
}

def hash_pin(pin: str) -> str:
    return pwd_context.hash(pin)

def verify_pin(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_current_user(request: Request):
    return request.session.get("user")

def require_login(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    return user

def require_role(request: Request, allowed_roles: list):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    if user["role"] not in allowed_roles:
        return RedirectResponse("/access-denied", status_code=302)
    return user
