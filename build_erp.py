from pathlib import Path
from textwrap import dedent

BASE = Path("C:/SHOURYA_ERP")

def write(rel, content):
    path = BASE / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")

# ================= data/db.py =================
write("data/db.py", """
import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "erp.db"

def conn():
    return sqlite3.connect(DB)

def init_db():
    c = conn()
    cur = c.cursor()

    # Event table (operational input)
    cur.execute(\"\"\"
    CREATE TABLE IF NOT EXISTS godown_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        event_type TEXT,
        filled INTEGER,
        empty INTEGER,
        defective INTEGER,
        remark TEXT
    )
    \"\"\")

    # Derived strict ledger (append-only)
    cur.execute(\"\"\"
    CREATE TABLE IF NOT EXISTS godown_ledger(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        opening_filled INTEGER,
        inward_filled INTEGER,
        outward_filled INTEGER,
        closing_filled INTEGER
    )
    \"\"\")

    c.commit()
    c.close()
""")

# ================= main.py =================
write("main.py", """
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from data.db import init_db
from routes import dashboard, godown_operational, godown_strict

app = FastAPI(title="Shourya LPG ERP – Hybrid")

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(dashboard.router)
app.include_router(godown_operational.router)
app.include_router(godown_strict.router)
""")

# ================= routes/dashboard.py =================
write("routes/dashboard.py", """
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
tpl = Jinja2Templates(directory="templates")

@router.get("/")
def dash(request: Request):
    return tpl.TemplateResponse("dashboard.html", {"request": request})
""")

# ================= routes/godown_operational.py =================
write("routes/godown_operational.py", """
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date
from data.db import conn

router = APIRouter()
tpl = Jinja2Templates(directory="templates")

@router.get("/godown")
def page(request: Request):
    return tpl.TemplateResponse("godown_operational.html", {"request": request})

@router.post("/godown/save")
def save(
    event_type: str = Form(...),
    filled: int = Form(0),
    empty: int = Form(0),
    defective: int = Form(0),
    remark: str = Form("")
):
    c = conn()
    c.execute(
        \"\"\"INSERT INTO godown_events
        (date,event_type,filled,empty,defective,remark)
        VALUES (?,?,?,?,?,?)\"\"\",
        (date.today().isoformat(), event_type, filled, empty, defective, remark)
    )
    c.commit()
    c.close()
    return {"status": "saved"}
""")

# ================= routes/godown_strict.py =================
write("routes/godown_strict.py", """
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.db import conn

router = APIRouter()
tpl = Jinja2Templates(directory="templates")

@router.get("/strict/godown")
def strict_view(request: Request):
    c = conn()
    rows = c.execute(
        \"\"\"SELECT date,
        SUM(CASE WHEN event_type='INWARD' THEN filled ELSE 0 END) as inward,
        SUM(CASE WHEN event_type='OUTWARD' THEN filled ELSE 0 END) as outward
        FROM godown_events GROUP BY date ORDER BY date\"\"\"
    ).fetchall()
    c.close()

    ledger = []
    closing = 0
    for d, inward, outward in rows:
        opening = closing
        closing = opening + inward - outward
        ledger.append({
            "date": d,
            "opening": opening,
            "inward": inward,
            "outward": outward,
            "closing": closing
        })

    return tpl.TemplateResponse(
        "godown_strict.html",
        {"request": request, "ledger": ledger}
    )
""")

# ================= templates =================
write("templates/dashboard.html", """
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="/static/app.css"></head>
<body>
<header>SHOURYA LPG ERP</header>
<div class="grid">
  <a class="card" href="/godown">🏭 गोडाऊन (Operational)</a>
  <a class="card" href="/strict/godown">📒 Godown Ledger (Strict)</a>
</div>
</body>
</html>
""")

write("templates/godown_operational.html", """
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="/static/app.css"></head>
<body>
<h2>गोडाऊन – दैनंदिन नोंद</h2>
<form method="post" action="/godown/save">
<select name="event_type">
  <option value="INWARD">आवक (Inward)</option>
  <option value="OUTWARD">जावक (Outward)</option>
</select>
<input type="number" name="filled" placeholder="भरलेले सिलेंडर">
<input type="number" name="empty" placeholder="रिकामे सिलेंडर">
<input type="number" name="defective" placeholder="डिफेक्टिव">
<input name="remark" placeholder="Remark">
<button class="btn">Save</button>
</form>
</body>
</html>
""")

write("templates/godown_strict.html", """
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="/static/app.css"></head>
<body>
<h2>Godown Stock Ledger (Strict)</h2>
<table border="1" width="100%">
<tr>
<th>Date</th><th>Opening</th><th>Inward</th><th>Outward</th><th>Closing</th>
</tr>
{% for r in ledger %}
<tr>
<td>{{r.date}}</td>
<td>{{r.opening}}</td>
<td>{{r.inward}}</td>
<td>{{r.outward}}</td>
<td>{{r.closing}}</td>
</tr>
{% endfor %}
</table>
</body>
</html>
""")

# ================= static =================
write("static/app.css", """
body{font-family:Arial;margin:0;background:#f5f7fa}
header{background:#003A8F;color:#fff;padding:14px;text-align:center}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;padding:20px}
.card{background:#fff;padding:20px;border-radius:12px;text-align:center;text-decoration:none;color:#000;font-size:18px}
.btn{padding:14px;background:#FDB913;border:none;border-radius:8px;width:100%;font-size:18px}
""")

print("✅ HYBRID GODOWN ERP BUILD COMPLETE")
