#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML Templates - Shourya Bharatgas ERP"""

BASE = r"""<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<meta name="theme-color" content="#003366">
<meta name="mobile-web-app-capable" content="yes">
<title>{% block title %}Shourya ERP{% endblock %}</title>
<style>
:root{--bl:#003366;--b2:#0066cc;--yl:#FFD700;--wh:#fff;--bg:#f0f4f8;--card:#fff;
  --br:#dde3ea;--gr:#28a745;--rd:#dc3545;--or:#fd7e14;--pu:#6f42c1;
  --tx:#1a202c;--mu:#6c757d;--rad:12px;--sh:0 2px 12px rgba(0,0,0,.1);}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--tx);font-size:15px;min-height:100vh;}

/* TOPBAR */
.tb{background:linear-gradient(135deg,#002244,#0055aa);color:#fff;padding:0 14px;height:52px;
  display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:1000;
  box-shadow:0 2px 8px rgba(0,0,0,.4);}
.tb-l{display:flex;align-items:center;gap:10px;}
.logo{width:34px;height:34px;background:var(--yl);border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-weight:900;color:#002244;font-size:17px;flex-shrink:0;}
.tb h1{font-size:15px;font-weight:700;line-height:1.2;}
.tb h1 small{font-size:10px;font-weight:400;opacity:.75;display:block;}
.tb-r{display:flex;align-items:center;gap:6px;}
.rbadge{background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.3);border-radius:20px;padding:2px 9px;font-size:11px;font-weight:700;}
.btn-lo{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);color:#fff;
  padding:4px 10px;border-radius:6px;cursor:pointer;font-size:12px;text-decoration:none;}
.ham{display:none;background:none;border:none;color:#fff;font-size:22px;cursor:pointer;padding:4px;}

/* NAV */
.nav{background:#002244;border-bottom:3px solid var(--yl);overflow-x:auto;display:flex;white-space:nowrap;scrollbar-width:none;}
.nav::-webkit-scrollbar{display:none;}
.nav a{color:rgba(255,255,255,.75);text-decoration:none;padding:9px 14px;font-size:12.5px;
  font-weight:600;display:inline-flex;align-items:center;gap:4px;transition:.2s;border-bottom:3px solid transparent;margin-bottom:-3px;}
.nav a:hover,.nav a.ac{color:#fff;background:rgba(255,255,255,.1);border-bottom-color:var(--yl);}

/* MAIN */
.main{padding:14px;max-width:1200px;margin:0 auto;}

/* CARDS */
.card{background:var(--card);border-radius:var(--rad);box-shadow:var(--sh);padding:18px;margin-bottom:14px;}
.ch{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;
  padding-bottom:10px;border-bottom:2px solid var(--br);}
.ct{font-size:15px;font-weight:700;color:var(--bl);}
.ct small{display:block;font-size:11px;color:var(--mu);font-weight:400;margin-top:2px;}

/* GRID */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
@media(max-width:640px){.g2,.g3,.g4{grid-template-columns:1fr 1fr;}
  .g4{grid-template-columns:1fr 1fr;}}
@media(max-width:380px){.g2,.g3,.g4{grid-template-columns:1fr;}}

/* STAT BOXES */
.sb{background:var(--card);border-radius:10px;padding:14px;text-align:center;
  box-shadow:var(--sh);border-top:4px solid var(--b2);}
.sb.g{border-top-color:var(--gr);} .sb.r{border-top-color:var(--rd);}
.sb.o{border-top-color:var(--or);} .sb.y{border-top-color:var(--yl);}
.sb.p{border-top-color:var(--pu);}
.sv{font-size:26px;font-weight:800;color:var(--bl);}
.sv.g{color:var(--gr);} .sv.r{color:var(--rd);} .sv.o{color:var(--or);}
.sl{font-size:11px;color:var(--mu);margin-top:3px;}
.sl2{font-size:10px;color:#aaa;margin-top:1px;}

/* FORMS */
.fg{margin-bottom:12px;}
.fg label{display:block;font-size:12px;font-weight:700;color:var(--tx);margin-bottom:4px;}
.fg label small{font-size:10px;color:var(--mu);font-weight:400;}
input,select,textarea{width:100%;padding:8px 11px;border:2px solid var(--br);border-radius:8px;
  font-size:14px;color:var(--tx);transition:.15s;background:#fff;font-family:inherit;}
input:focus,select:focus,textarea:focus{border-color:var(--b2);outline:none;box-shadow:0 0 0 3px rgba(0,102,204,.1);}
textarea{resize:vertical;min-height:64px;}

/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:5px;padding:8px 16px;border-radius:8px;
  font-size:13px;font-weight:700;cursor:pointer;border:none;transition:.15s;text-decoration:none;}
.bp{background:var(--b2);color:#fff;} .bp:hover{background:#0052a3;}
.bs{background:var(--gr);color:#fff;} .bs:hover{background:#218838;}
.bd{background:var(--rd);color:#fff;} .bd:hover{background:#c82333;}
.bw{background:#f0ad4e;color:#fff;} .bw:hover{background:#d89b3c;}
.bo{background:transparent;border:2px solid var(--b2);color:var(--b2);}
.bo:hover{background:var(--b2);color:#fff;}
.btn-sm{padding:4px 10px;font-size:11px;}
.btn-bl{width:100%;justify-content:center;}

/* PAYMENT MODE BUTTONS */
.pm-row{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0;}
.pm{padding:6px 12px;border-radius:20px;font-size:12px;font-weight:700;cursor:pointer;
  border:2px solid var(--br);background:#fff;transition:.15s;white-space:nowrap;}
.pm.ac{border-color:var(--b2);background:var(--b2);color:#fff;}

/* DENOM CALCULATOR */
.dc{background:#f8f9fa;border:2px solid var(--br);border-radius:10px;padding:14px;margin-top:10px;}
.dc-row{display:flex;align-items:center;gap:8px;margin-bottom:7px;}
.dc-row label{width:55px;font-size:13px;font-weight:700;color:var(--gr);flex-shrink:0;}
.dc-row input{flex:1;text-align:center;font-size:15px;font-weight:700;}
.dc-row span{width:80px;text-align:right;font-weight:700;font-size:13px;color:var(--bl);}
.dc-tot{border-top:2px solid var(--br);padding-top:8px;margin-top:4px;
  display:flex;justify-content:space-between;font-size:16px;font-weight:900;}

/* TABLES */
.tw{overflow-x:auto;}
table{width:100%;border-collapse:collapse;font-size:12.5px;}
th{background:#f0f4f8;padding:9px 11px;text-align:left;font-weight:700;
  border-bottom:2px solid var(--br);white-space:nowrap;}
td{padding:8px 11px;border-bottom:1px solid var(--br);vertical-align:middle;}
tr:hover td{background:#f8f9fb;}

/* BADGES */
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;}
.bb{background:#e3f2fd;color:#1565c0;} .bg{background:#e8f5e9;color:#2e7d32;}
.br2{background:#ffebee;color:#c62828;} .bo2{background:#fff3e0;color:#e65100;}
.by{background:#fffde7;color:#f57f17;} .bpu{background:#f3e5f5;color:#6a1b9a;}

/* ALERTS */
.al{padding:10px 14px;border-radius:8px;margin-bottom:10px;font-size:13px;}
.als{background:#d4edda;border:1px solid #c3e6cb;color:#155724;}
.ald{background:#f8d7da;border:1px solid #f5c6cb;color:#721c24;}
.alw{background:#fff3cd;border:1px solid #ffeeba;color:#856404;}
.ali{background:#d1ecf1;border:1px solid #bee5eb;color:#0c5460;}

/* EXPAND SECTIONS */
.ex{border:2px solid var(--br);border-radius:var(--rad);margin-bottom:10px;overflow:hidden;}
.exh{background:#f8f9fa;padding:12px 14px;cursor:pointer;display:flex;align-items:center;
  justify-content:space-between;user-select:none;transition:.15s;}
.exh:hover{background:#eef2f7;}
.exh h3{font-size:14px;font-weight:700;color:var(--bl);}
.exh .ar{transition:.25s;font-size:16px;color:var(--b2);}
.exh.op .ar{transform:rotate(180deg);}
.exb{display:none;padding:14px;}
.exb.sh{display:block;}

/* DAY STATUS BAR */
.dsb{background:linear-gradient(135deg,#002244,#0055aa);color:#fff;border-radius:var(--rad);
  padding:12px 16px;margin-bottom:14px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;}
.dsbi .v{font-size:18px;font-weight:800;}
.dsbi .l{font-size:10px;opacity:.65;margin-top:1px;}
.sok{color:#69f0ae;} .swn{color:#FFD700;} .ser{color:#ff5252;}

/* STOCK CARDS */
.sc{background:linear-gradient(135deg,#002244,#0055aa);color:#fff;border-radius:10px;
  padding:14px;text-align:center;}
.sc.em{background:linear-gradient(135deg,#4a148c,#7b1fa2);}
.sc.df{background:linear-gradient(135deg,#b71c1c,#d32f2f);}
.sc .sn{font-size:32px;font-weight:900;}
.sc .sk{font-size:11px;opacity:.8;margin-top:3px;}

/* CUSTOMER LIST */
.ci{display:flex;align-items:center;gap:9px;padding:9px;border:1.5px solid var(--br);
  border-radius:9px;margin-bottom:7px;cursor:pointer;transition:.15s;}
.ci:hover{border-color:var(--b2);background:#f0f6ff;}
.cdot{width:13px;height:13px;border-radius:50%;flex-shrink:0;}
.cif{flex:1;min-width:0;}
.cn{font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.ca{font-size:10px;color:var(--mu);}
.cotp{font-size:11px;color:var(--gr);font-weight:700;}
.otp-in{width:80px!important;text-align:center;font-size:13px;}

/* DELIVERY MAP */
#dmap{height:300px;border-radius:var(--rad);z-index:1;}

/* AREA PILLS */
.ap-row{display:flex;flex-wrap:wrap;gap:5px;margin:7px 0;}
.ap{padding:4px 11px;border-radius:20px;font-size:11px;font-weight:700;cursor:pointer;
  border:1.5px solid #ccc;background:#fff;transition:.15s;}
.ap.ac{background:var(--b2);color:#fff;border-color:var(--b2);}

/* MODAL BOTTOM SHEET */
.mo{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:2000;align-items:flex-end;}
.mo.sh{display:flex;}
.ms{background:#fff;border-radius:18px 18px 0 0;width:100%;max-height:92vh;overflow-y:auto;padding:18px;}
.mh{width:36px;height:4px;background:#ddd;border-radius:2px;margin:0 auto 14px;}

/* CASH BIG */
.cbig{text-align:center;padding:18px;background:linear-gradient(135deg,#1a3a2a,#2d6a4f);
  color:#fff;border-radius:var(--rad);margin-bottom:14px;}
.cbig .cam{font-size:38px;font-weight:900;}

/* COMPARE TABLE */
.cmp{border:1px solid var(--br);border-radius:8px;overflow:hidden;}
.cmpr{display:grid;grid-template-columns:2fr 1fr 1fr;border-bottom:1px solid var(--br);}
.cmpr div{padding:7px 11px;font-size:12px;}
.cmpr:first-child div{background:#f0f4f8;font-weight:700;}
.dok{color:var(--gr);font-weight:700;} .der{color:var(--rd);font-weight:800;}

/* GODOWN STOCK GRID */
.sgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;}

/* PRINT */
@media print{.tb,.nav,.no-print{display:none!important;}
  .main{padding:0;} .card{box-shadow:none;border:1px solid #ddd;}}

/* MOBILE NAV */
@media(max-width:600px){
  .ham{display:block;}
  .nav-links{display:none;position:fixed;top:52px;left:0;right:0;
    background:#002244;z-index:999;flex-direction:column;border-top:1px solid rgba(255,255,255,.2);}
  .nav-links.op{display:flex;}
  .nav-links a{padding:11px 18px;border-bottom:1px solid rgba(255,255,255,.08);}
  .tb h1{font-size:13px;}
}

/* WAGE ROW */
.wr{background:#f8f9fa;border-radius:8px;padding:12px;margin-bottom:8px;border-left:4px solid var(--b2);}
</style>
</head>
<body>
<div class="tb">
  <div class="tb-l">
    <div class="logo">S</div>
    <h1>Shourya Bharatgas Services<small>BPCL Dist: 187618 · Jaysinghpur</small></h1>
  </div>
  <div class="tb-r">
    {% if session.get('uid') %}
    <span class="rbadge">{{ session.get('role','').upper() }}</span>
    <a href="/logout" class="btn-lo">बाहेर पडा</a>
    {% endif %}
    <button class="ham" onclick="navToggle()">☰</button>
  </div>
</div>
{% if session.get('uid') %}
<nav class="nav">
  <div class="nav-links" id="NL">
    {% set r=session.get('role','') %}
    <a href="/dashboard" class="{% if active=='dashboard' %}ac{% endif %}">🏠 मुख्यपृष्ठ</a>
    {% if r in ['owner','manager','office','accountant'] %}
    <a href="/office" class="{% if active=='office' %}ac{% endif %}">🏪 ऑफिस</a>
    {% endif %}
    {% if r in ['delivery','loader','driver','owner','manager'] %}
    <a href="/delivery" class="{% if active=='delivery' %}ac{% endif %}">🚚 डिलिव्हरी</a>
    {% endif %}
    {% if r in ['owner','manager','office','delivery','loader','driver'] %}
    <a href="/godown" class="{% if active=='godown' %}ac{% endif %}">🏭 गोदाम</a>
    {% endif %}
    {% if r=='bda' %}
    <a href="/bda" class="{% if active=='bda' %}ac{% endif %}">🏘️ BDA</a>
    {% endif %}
    {% if r in ['owner','manager','accountant'] %}
    <a href="/wages" class="{% if active=='wages' %}ac{% endif %}">💰 पगार</a>
    <a href="/accounting" class="{% if active=='accounting' %}ac{% endif %}">📊 हिशेब</a>
    {% endif %}
    {% if r in ['owner','manager'] %}
    <a href="/users" class="{% if active=='users' %}ac{% endif %}">👥 कर्मचारी</a>
    {% endif %}
    {% if r=='owner' %}
    <a href="/settings" class="{% if active=='settings' %}ac{% endif %}">⚙️ सेटिंग्ज</a>
    {% endif %}
    <a href="/chat" class="{% if active=='chat' %}ac{% endif %}">💬 चॅट</a>
    <a href="/bpcl-dayend" class="{% if active=='bpcld' %}ac{% endif %}">📊 BPCL</a>
  </div>
</nav>
{% endif %}
<div class="main">
{% with msgs=get_flashed_messages(with_categories=True) %}
  {% for cat,msg in msgs %}
  <div class="al {% if cat=='success' %}als{% elif cat=='danger' %}ald{% elif cat=='warning' %}alw{% else %}ali{% endif %}">{{ msg }}</div>
  {% endfor %}
{% endwith %}
{% block body %}{% endblock %}
</div>
<script>
function navToggle(){document.getElementById('NL').classList.toggle('op');}
function xToggle(h){h.classList.toggle('op');var b=h.nextElementSibling;b.classList.toggle('sh');}
function denom(p){
  var t=0;
  [500,200,100,50,20,10].forEach(function(v){
    var el=document.getElementById(p+'_'+v);
    if(!el)return;
    var q=parseInt(el.value)||0;
    t+=q*v;
    var sub=document.getElementById(p+'_s'+v);
    if(sub)sub.textContent='₹'+(q*v).toLocaleString('en-IN');
  });
  var co=document.getElementById(p+'_coins');
  if(co)t+=parseFloat(co.value)||0;
  var tot=document.getElementById(p+'_tot');
  if(tot)tot.textContent='₹'+t.toLocaleString('en-IN');
  return t;
}
function selPay(btn,pfx){
  btn.closest('.pm-row').querySelectorAll('.pm').forEach(b=>b.classList.remove('ac'));
  btn.classList.add('ac');
  var m=btn.dataset.mode;
  document.getElementById(pfx+'_pm').value=m;
  var cd=document.getElementById(pfx+'_cd'),od=document.getElementById(pfx+'_od');
  if(cd)cd.style.display=(m==='partial')?'block':'none';
  if(od)od.style.display=(m==='partial')?'block':'none';
}
function updAddPrice(sel){
  var op=sel.options[sel.selectedIndex];
  var pi=document.getElementById('add_price');
  if(pi&&op.dataset.price!==undefined)pi.value=op.dataset.price;
}
function calcFill(){
  var r=parseInt(document.getElementById('fr').value)||0;
  var c=parseInt(document.getElementById('fc').value)||0;
  var e=parseInt(document.getElementById('fe').value)||0;
  document.getElementById('ft').value=r*c+e;
}
function calcZone(z){
  var r=parseInt(document.getElementById(z+'r').value)||0;
  var c=parseInt(document.getElementById(z+'c').value)||0;
  var d=parseInt(document.getElementById(z+'d').value)||0;
  var s=parseInt(document.getElementById(z+'s').value)||0;
  var t=(r*c*2)+(d*2)+s;
  var el=document.getElementById(z+'t');
  if(el)el.textContent=t;
  return t;
}
function calcEmpty(){
  var t=calcZone('z1')+calcZone('z2')+calcZone('z3');
  document.getElementById('et').value=t;
}
</script>
{% block scripts %}{% endblock %}
</body>
</html>"""

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="mr"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login — Shourya ERP</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:linear-gradient(135deg,#002244,#0066cc);min-height:100vh;
  display:flex;align-items:center;justify-content:center;padding:20px;font-family:'Segoe UI',Arial,sans-serif;}
.box{background:#fff;border-radius:20px;padding:30px;width:100%;max-width:360px;box-shadow:0 8px 32px rgba(0,0,0,.3);}
.logo{width:56px;height:56px;background:linear-gradient(135deg,#002244,#0066cc);border-radius:50%;
  margin:0 auto 12px;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:900;color:#FFD700;}
h2{text-align:center;color:#003366;font-size:18px;margin-bottom:4px;}
p{text-align:center;color:#666;font-size:12px;margin-bottom:20px;}
.al{padding:9px 12px;border-radius:6px;background:#f8d7da;border:1px solid #f5c6cb;color:#721c24;font-size:13px;margin-bottom:12px;}
.fg{margin-bottom:14px;}
label{display:block;font-size:12px;font-weight:700;color:#333;margin-bottom:4px;}
input{width:100%;padding:9px 12px;border:2px solid #dde3ea;border-radius:8px;font-size:15px;}
input:focus{border-color:#0066cc;outline:none;}
.btn{width:100%;padding:11px;background:#0066cc;color:#fff;border:none;border-radius:8px;
  font-size:15px;font-weight:700;cursor:pointer;margin-top:4px;}
.btn:hover{background:#004fa0;}
small{display:block;text-align:center;color:#999;font-size:11px;margin-top:14px;}
</style></head><body>
<div class="box">
  <div class="logo">S</div>
  <h2>Shourya Bharatgas Services</h2>
  <p>BPCL LPG Distributor · Jaysinghpur · Dist: 187618</p>
  {% if error %}<div class="al">{{ error }}</div>{% endif %}
  <form method="post">
    <div class="fg"><label>📱 मोबाईल नंबर</label>
      <input type="tel" name="mobile" placeholder="10-digit mobile" required pattern="[0-9]{10}" autofocus></div>
    <div class="fg"><label>🔒 PIN</label>
      <input type="password" name="pin" placeholder="Enter PIN" required maxlength="8"></div>
    <button type="submit" class="btn">लॉगिन करा / Login</button>
  </form>
  <small>Default PIN: <strong>1234</strong> (बदलणे आवश्यक आहे)</small>
</div>
</body></html>"""

CHANGE_PIN_PAGE = """
<div style="display:flex;align-items:center;justify-content:center;padding:40px 20px;">
<div class="card" style="max-width:400px;width:100%;">
  <div class="ch"><div class="ct">🔐 PIN बदला <small>Change Your PIN</small></div></div>
  {% if error %}<div class="al ald">{{ error }}</div>{% endif %}
  <div class="al ali">पहिल्यांदा लॉगिन केल्यावर PIN बदलणे अनिवार्य आहे.<br>You must set a new PIN to continue.</div>
  <form method="post">
    <div class="fg"><label>नवीन PIN (min 4 digits)</label>
      <input type="password" name="pin1" required minlength="4" autofocus placeholder="New PIN"></div>
    <div class="fg"><label>PIN confirm करा</label>
      <input type="password" name="pin2" required minlength="4" placeholder="Confirm PIN"></div>
    <button type="submit" class="btn bs btn-bl">✅ PIN सेट करा</button>
  </form>
</div></div>"""
