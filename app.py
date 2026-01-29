from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import csv, os
from datetime import datetime

from data.db import init_db, get_conn

app = FastAPI()

# ---------------- SESSION ----------------
app.add_middleware(SessionMiddleware, secret_key="SHOURYA_SECRET")

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(UPLOAD_DIR, exist_ok=True)
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# ---------------- DB INIT ----------------
init_db()

# =========================
# LOGIN
# =========================
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    role: str = Form(...)
):
    # role must be: DELIVERY / OFFICE / OWNER / ACCOUNTS
    request.session["user"] = {
        "username": username,
        "role": role
    }
    return RedirectResponse("/shell", status_code=302)


# =========================
# ERP SHELL (ROLE ROUTING)
# =========================
@app.get("/shell")
async def shell(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)

    role = user.get("role")

    if role == "DELIVERY":
        return RedirectResponse("/delivery/upload", status_code=302)

    if role == "OFFICE":
        return RedirectResponse("/office", status_code=302)

    if role == "OWNER":
        return RedirectResponse("/owner", status_code=302)

    if role == "ACCOUNTS":
        return RedirectResponse("/accounts", status_code=302)

    return RedirectResponse("/", status_code=302)


# =========================
# DELIVERY — CSV UPLOAD
# =========================
@app.get("/delivery/upload", response_class=HTMLResponse)
async def delivery_upload_page(request: Request):
    return templates.TemplateResponse("delivery_upload.html", {"request": request})


@app.post("/delivery/upload", response_class=HTMLResponse)
async def handle_delivery_upload(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    deliveries = []

    with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
        rows = list(csv.reader(csvfile))
        for row in rows[10:]:
            if len(row) < 15:
                continue
            name = row[10].strip()
            if not name:
                continue

            address = " ".join([row[11], row[12], row[13]])

            deliveries.append({
                "cashmemo": row[7].strip(),
                "name": name,
                "address": address,
                "mobile": row[14].strip()
            })

    conn = get_conn()
    cur = conn.cursor()

    for d in deliveries:
        cur.execute("SELECT 1 FROM deliveries WHERE cashmemo=?", (d["cashmemo"],))
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO deliveries
                (cashmemo, name, address, mobile, status, otp)
                VALUES (?, ?, ?, ?, 'Pending', '')
            """, (
                d["cashmemo"],
                d["name"],
                d["address"],
                d["mobile"]
            ))

    conn.commit()

    cur.execute("""
        SELECT cashmemo, name, address, mobile, status, otp
        FROM deliveries
    """)
    rows = cur.fetchall()
    conn.close()

    return templates.TemplateResponse(
        "delivery_list.html",
        {
            "request": request,
            "deliveries": [
                {
                    "cashmemo": r[0],
                    "name": r[1],
                    "address": r[2],
                    "mobile": r[3],
                    "status": r[4],
                    "otp": r[5]
                }
                for r in rows
            ],
            "last_refresh": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
    )


@app.post("/delivery/update")
async def update_delivery(
    cashmemo: str = Form(...),
    status: str = Form(...),
    otp: str = Form("")
):
    conn = get_conn()
    conn.execute("""
        UPDATE deliveries
        SET status=?, otp=?, updated_at=CURRENT_TIMESTAMP
        WHERE cashmemo=?
    """, (status, otp, cashmemo))
    conn.commit()
    conn.close()

    return RedirectResponse("/delivery/upload", status_code=303)


# =========================
# OFFICE ROUTES (REGISTERED ONCE)
# =========================
from office.routes.office_router import router as office_router
app.include_router(office_router)


# =========================
# OWNER PLACEHOLDER
# =========================
@app.get("/owner")
async def owner_home():
    return {"status": "Owner dashboard coming"}


# =========================
# ACCOUNTS PLACEHOLDER
# =========================
@app.get("/accounts")
async def accounts_home():
    return {"status": "Accounts dashboard coming"}
