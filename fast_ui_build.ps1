# ================= FAST UI BUILD SCRIPT =================
# Writes UI + routing safely (NO multiline console paste)
# =======================================================

$Base = "C:\SHOURYA_ERP"
$VB   = "$Base\scripts\write_file.vbs"

if (!(Test-Path $VB)) {
    Write-Error "VB writer not found at $VB"
    exit 1
}

function WriteFile($relativePath, $content) {
    $full = Join-Path $Base $relativePath
    cscript //nologo $VB $full $content | Out-Null
}

# ---------------- main.py ----------------
WriteFile "main.py" @"
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from data.db import init
from routes import delivery, godown, accounting

app = FastAPI(title='Shourya LPG ERP')

init()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

app.include_router(delivery.router)
app.include_router(godown.router)
app.include_router(accounting.router)

@app.get('/')
def dashboard(request: Request):
    return templates.TemplateResponse('dashboard.html', {'request': request})

@app.get('/godown')
def godown_page(request: Request):
    return templates.TemplateResponse('godown.html', {'request': request})

@app.get('/delivery')
def delivery_page(request: Request):
    return templates.TemplateResponse('delivery.html', {'request': request})

@app.get('/accounting')
def accounting_page(request: Request):
    return templates.TemplateResponse('accounting.html', {'request': request})
"@

# ---------------- dashboard.html ----------------
WriteFile "templates\dashboard.html" @"
{% extends 'base.html' %}
{% block body %}
<h2>Dashboard / डॅशबोर्ड</h2>

<div class='grid'>
  <a class='card' href='/godown'>🏭 गोडाऊन<br><small>Godown Stock</small></a>
  <a class='card' href='/delivery'>🚚 डिलिव्हरी<br><small>Delivery</small></a>
  <a class='card' href='/accounting'>💰 हिशेब<br><small>Accounting</small></a>
</div>
{% endblock %}
"@

# ---------------- godown.html ----------------
WriteFile "templates\godown.html" @"
{% extends 'base.html' %}
{% block body %}
<h2>गोडाऊन – भौतिक स्टॉक (14.2 KG)</h2>

<form method='post' action='/godown/physical' class='card'>
<label>वापरकर्ता (User)</label>
<input name='user' required>

<label>भरलेले सिलेंडर</label>
<input type='number' name='filled' required>

<label>रिकामे सिलेंडर</label>
<input type='number' name='empty' required>

<button class='btn'>सेव्ह करा / Save</button>
</form>

<p class='note'>※ प्रत्येक वेळेस स्वतंत्र मोजणी</p>
{% endblock %}
"@

# ---------------- delivery.html ----------------
WriteFile "templates\delivery.html" @"
{% extends 'base.html' %}
{% block body %}
<h2>डिलिव्हरी – BPCL CSV Upload</h2>

<form method='post' action='/delivery/upload' enctype='multipart/form-data' class='card'>
<input type='file' name='file' required>
<button class='btn'>Upload CSV</button>
</form>
{% endblock %}
"@

# ---------------- accounting.html ----------------
WriteFile "templates\accounting.html" @"
{% extends 'base.html' %}
{% block body %}
<h2>दैनंदिन हिशेब</h2>

<form method='post' action='/accounting/day' class='card'>
<label>Cash (₹)</label>
<input type='number' step='0.01' name='cash' required>

<label>Digital (GPay / Online)</label>
<input type='number' step='0.01' name='digital' required>

<label>Denomination</label>
<textarea name='denom' placeholder='₹500 x 10, ₹200 x 5'></textarea>

<button class='btn'>सेव्ह करा / Save</button>
</form>
{% endblock %}
"@

# ---------------- app.css ----------------
WriteFile "static\app.css" @"
body {
  font-family: Arial, sans-serif;
  margin: 0;
  background: #f5f7fa;
}

header {
  background: #003A8F;
  color: white;
  padding: 14px;
  text-align: center;
  font-size: 20px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px,1fr));
  gap: 15px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  text-decoration: none;
  color: black;
  font-size: 18px;
}

.card:hover { background: #e8f0ff; }

.btn {
  width: 100%;
  padding: 14px;
  background: #FDB913;
  border: none;
  border-radius: 8px;
  font-size: 18px;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  font-size: 16px;
}

.note {
  font-size: 13px;
  color: #555;
}
"@

Write-Host "✅ FAST UI FILES GENERATED SUCCESSFULLY" -ForegroundColor Green
Write-Host "➡ Refresh browser: http://127.0.0.1:8000"
