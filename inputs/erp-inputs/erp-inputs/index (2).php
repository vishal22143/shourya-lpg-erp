<?php
require_once 'config.php';
$currentUser = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shourya Bharatgas ERP v3</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bpcl-blue: #003087; --bpcl-yellow: #FFD100; --bpcl-orange: #F7941D;
  --bg-dark: #0a0e1a; --bg-card: #0f1628; --bg-card2: #141d35;
  --border: #1e2d50; --border-bright: #2a4080;
  --text-primary: #e8eeff; --text-secondary: #8fa3cc; --text-muted: #4a5a80;
  --accent-green: #22c55e; --accent-blue: #4a90e2; --accent-yellow: #FFD100;
  --accent-orange: #f97316; --accent-red: #ef4444;
  --font-main: 'Rajdhani', 'Noto Sans Devanagari', sans-serif;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font-main);
  background: linear-gradient(135deg, #000820 0%, #001a4d 50%, #000c2e 100%);
  color: var(--text-primary); min-height: 100vh; overflow-x: hidden;
}

/* LOGIN */
#loginScreen {
  position: fixed; inset: 0; z-index: 1000;
  background: linear-gradient(135deg, #000820 0%, #001a4d 50%, #000c2e 100%);
  display: flex; align-items: center; justify-content: center; flex-direction: column;
}
.login-card {
  position: relative; width: 420px; max-width: 95vw;
  background: var(--bg-card); border: 1px solid var(--border-bright);
  border-radius: 16px; padding: 40px;
  box-shadow: 0 0 60px rgba(74,144,226,0.2), 0 8px 32px rgba(0,0,0,0.4);
}
.login-logo { text-align: center; margin-bottom: 32px; }
.login-logo .company-icon {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow));
  border-radius: 16px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px; font-size: 36px;
  box-shadow: 0 0 20px rgba(74,144,226,0.3);
}
.login-logo h1 { font-size: 22px; font-weight: 700; color: var(--accent-yellow); letter-spacing: 1px; }
.login-logo p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.login-field { margin-bottom: 16px; }
.login-field label { display: block; font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
.login-field input, .login-field select {
  width: 100%; background: rgba(255,255,255,0.05);
  border: 1px solid var(--border); border-radius: 8px;
  color: var(--text-primary); font-family: var(--font-main); font-size: 16px;
  padding: 12px 16px; transition: all 0.2s;
}
.login-field input:focus, .login-field select:focus {
  outline: none; border-color: var(--accent-blue);
  box-shadow: 0 0 20px rgba(74,144,226,0.3);
  background: rgba(74,144,226,0.05);
}
.btn-login {
  width: 100%; background: linear-gradient(135deg, var(--accent-blue), var(--bpcl-blue));
  color: white; border: none; border-radius: 8px;
  padding: 14px; font-size: 16px; font-weight: 700; cursor: pointer;
}
.btn-login:hover { box-shadow: 0 0 25px rgba(74,144,226,0.4); }

/* APP */
#app { display: none; }
.topnav {
  background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
  border-bottom: 1px solid var(--border-bright);
  padding: 16px 24px; display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.topnav-logo { display: flex; align-items: center; gap: 12px; }
.logo-icon {
  width: 48px; height: 48px; background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow));
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
  font-size: 24px; box-shadow: 0 0 15px rgba(255,209,0,0.2);
}
.logo-text { font-size: 18px; font-weight: 700; color: var(--accent-yellow); }
.logo-sub { font-size: 11px; color: var(--text-muted); }
.topnav-center { display: flex; gap: 8px; }
.nav-btn {
  padding: 10px 18px; background: rgba(255,255,255,0.03);
  border: 1px solid var(--border); border-radius: 8px;
  color: var(--text-secondary); font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.nav-btn:hover { background: rgba(74,144,226,0.1); border-color: var(--accent-blue); color: var(--text-primary); }
.nav-btn.active {
  background: linear-gradient(135deg, rgba(74,144,226,0.2), rgba(0,48,135,0.2));
  border-color: var(--accent-blue); color: var(--accent-yellow);
  box-shadow: 0 0 15px rgba(74,144,226,0.2);
}
.user-badge { display: flex; align-items: center; gap: 10px; }
.user-avatar {
  width: 40px; height: 40px; border-radius: 10px;
  background: var(--accent-blue); color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px;
}
.btn-logout {
  padding: 8px 16px; background: rgba(239,68,68,0.15);
  border: 1px solid rgba(239,68,68,0.3); border-radius: 8px;
  color: var(--accent-red); font-weight: 600; cursor: pointer;
}

.content { padding: 24px; max-width: 1600px; margin: 0 auto; }
.page { display: none; }
.page.active { display: block; animation: fadeIn 0.3s; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.page-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 20px; padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.page-header-title { font-size: 24px; font-weight: 700; color: var(--accent-yellow); }
.page-header-sub { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }

.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

/* DELIVERY CARD */
.delivery-card {
  position: relative; background: var(--bg-card);
  border: 1px solid var(--border); border-radius: 10px;
  padding: 14px 14px 14px 18px; margin-bottom: 10px;
  display: flex; gap: 14px; align-items: center;
  cursor: pointer; transition: all 0.2s;
}
.delivery-card:hover {
  background: var(--bg-card2); border-color: var(--border-bright);
  box-shadow: 0 4px 12px rgba(74,144,226,0.15);
}
.status-bar {
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 4px; border-radius: 10px 0 0 10px;
}
.dcnum {
  font-size: 24px; font-weight: 700; color: var(--text-muted);
  min-width: 40px; text-align: center;
}
.dcinfo { flex: 1; }
.dcname { font-size: 15px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.dcaddress { font-size: 12px; color: var(--text-secondary); margin-bottom: 3px; }
.dcarea { font-size: 11px; color: var(--text-muted); }
.dcactions { text-align: right; }
.dcphone {
  font-size: 13px; color: var(--accent-blue);
  margin-top: 6px; font-weight: 600;
}

.chip {
  display: inline-block; padding: 4px 10px;
  border-radius: 12px; font-size: 11px; font-weight: 700;
}
.chip-blue { background: rgba(59,130,246,0.15); color: #3b82f6; }
.chip-yellow { background: rgba(234,179,8,0.15); color: #eab308; }
.chip-green { background: rgba(34,197,94,0.15); color: #22c55e; }
.chip-orange { background: rgba(249,115,22,0.15); color: #f97316; }
.chip-red { background: rgba(239,68,68,0.15); color: #ef4444; }

.status-dot {
  display: inline-block; width: 8px; height: 8px;
  border-radius: 50%; margin-right: 4px;
}
.status-scheduled { background: #3b82f6; }
.status-intrip { background: #eab308; }
.status-delivered { background: #22c55e; }
.status-emergency { background: #f97316; }
.status-notdelivered { background: #ef4444; }

.search-bar {
  display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;
}
.search-input {
  flex: 1; min-width: 250px; background: rgba(255,255,255,0.05);
  border: 1px solid var(--border); border-radius: 8px;
  padding: 12px 16px; color: var(--text-primary);
  font-family: var(--font-main); font-size: 15px;
}
.search-input:focus {
  outline: none; border-color: var(--accent-blue);
  box-shadow: 0 0 15px rgba(74,144,226,0.2);
}

.btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; }
.btn-primary { background: var(--accent-blue); color: white; }
.btn-success { background: var(--accent-green); color: white; }
.btn-warning { background: var(--accent-yellow); color: var(--bg-dark); }
.btn-sm { padding: 6px 12px; font-size: 13px; }

.stat-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; text-align: center;
}
.stat-value { font-size: 36px; font-weight: 700; color: var(--accent-yellow); }
.stat-label { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }

.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; background: rgba(255,255,255,0.05);
  border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 14px; color: var(--text-primary);
  font-family: var(--font-main);
}

@media (max-width: 768px) {
  .topnav { flex-direction: column; gap: 12px; }
  .content { padding: 12px; }
  .grid-4 { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<!-- LOGIN SCREEN -->
<div id="loginScreen" <?php if($currentUser) echo 'style="display:none"'; ?>>
  <div class="login-card">
    <div class="login-logo">
      <div class="company-icon">🔥</div>
      <h1>SHOURYA BHARATGAS</h1>
      <p>SAP: 187618 · Jaysingpur</p>
      <p style="font-size:11px;margin-top:8px">BPCL Authorized Distributor</p>
    </div>
    <form id="loginForm" onsubmit="return doLogin(event)">
      <div class="login-field">
        <label>वापरकर्ता / USER</label>
        <select name="username" required>
          <option value="">-- Select --</option>
          <option value="owner">Vishal Patil (Owner)</option>
          <option value="owner2">Mrinmayi Patil (Owner)</option>
          <option value="manager">Rajesh Awale (Manager)</option>
          <option value="delivery_bhore">Vishwas Bhore</option>
          <option value="delivery_mahesh">Mahesh Patil</option>
          <option value="delivery_harun">Harun Fakir</option>
          <option value="delivery_magdum">Vishal Magdum</option>
          <option value="bda_kondigre">Kondigre - Sarika</option>
          <option value="bda_nimshirgav1">Nimshirgav - Kumar</option>
          <option value="bda_nimshirgav2">Nimshirgav - Lakhane</option>
          <option value="bda_danoli">Danoli - Manoj</option>
          <option value="bda_kothali">Kothali - Yadav</option>
          <option value="bda_kavatesar">Kavatesar - Sudhakar</option>
          <option value="bda_shirol">Shirol - Vikrant</option>
          <option value="bda_awale">Chipri Beghar - Mrs. Awale</option>
        </select>
      </div>
      <div class="login-field">
        <label>पासवर्ड / PASSWORD</label>
        <input type="password" name="password" required placeholder="Enter password">
      </div>
      <button type="submit" class="btn-login">🔐 लॉगिन करा / LOGIN</button>
    </form>
    <p style="text-align:center;margin-top:16px;font-size:11px;color:var(--text-muted)">Default: 1234</p>
  </div>
</div>

<!-- APP -->
<div id="app" <?php if($currentUser) echo 'style="display:block"'; ?>>
  <nav class="topnav">
    <div class="topnav-logo">
      <div class="logo-icon">🔥</div>
      <div>
        <div class="logo-text">SHOURYA BHARATGAS</div>
        <div class="logo-sub">SAP: 187618 · Jaysingpur</div>
      </div>
    </div>
    <div class="topnav-center" id="navButtons"></div>
    <div class="topnav-right" style="display:flex;align-items:center;gap:16px">
      <div class="user-badge">
        <div class="user-avatar" id="navAvatar">VP</div>
        <div>
          <div style="font-weight:700;font-size:13px" id="navName"><?php echo $currentUser ? $currentUser['name'] : 'User'; ?></div>
          <div style="font-size:11px;color:var(--text-muted)" id="navRole"><?php echo $currentUser ? $currentUser['designation'] : 'Role'; ?></div>
        </div>
      </div>
      <button class="btn-logout" onclick="doLogout()">↩ लॉगआउट</button>
    </div>
  </nav>

  <div class="content" id="mainContent"></div>
</div>

<script>
let currentUser = <?php echo json_encode($currentUser); ?>;
let deliveries = [];
let allAreas = [];

// LOGIN
async function doLogin(e) {
  e.preventDefault();
  const form = new FormData(e.target);
  const res = await fetch('api.php?action=login', { method: 'POST', body: form });
  const data = await res.json();
  if (data.success) location.reload();
  else alert(data.message);
}

async function doLogout() {
  await fetch('api.php?action=logout');
  location.reload();
}

// INIT
if (currentUser) {
  buildNav();
  showPage('dashboard');
  loadDeliveries();
}

function buildNav() {
  const navs = {
    owner: [{p:'dashboard',l:'📊 Dashboard'},{p:'delivery',l:'🚴 Delivery'},{p:'godown',l:'🏭 Godown'},{p:'trip',l:'🚛 Trip'}],
    manager: [{p:'dashboard',l:'📊 Dashboard'},{p:'delivery',l:'🚴 Delivery'},{p:'godown',l:'🏭 Godown'},{p:'trip',l:'🚛 Trip'}],
    delivery: [{p:'dashboard',l:'📊 Dashboard'},{p:'delivery',l:'🚴 Delivery'},{p:'trip',l:'🚛 Trip'}],
    bda: [{p:'dashboard',l:'📊 Dashboard'},{p:'delivery',l:'🚴 Delivery'}]
  };
  const userNavs = navs[currentUser.role] || navs.owner;
  const html = userNavs.map(n => 
    `<button class="nav-btn ${n.p==='dashboard'?'active':''}" data-page="${n.p}" onclick="showPage('${n.p}')">${n.l}</button>`
  ).join('');
  document.getElementById('navButtons').innerHTML = html;
}

function showPage(page) {
  document.querySelectorAll('.nav-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.page === page);
  });
  const content = document.getElementById('mainContent');
  content.innerHTML = buildPage(page);
}

// PAGE BUILDERS
function buildPage(page) {
  switch(page) {
    case 'dashboard': return buildDashboard();
    case 'delivery': return buildDelivery();
    case 'godown': return buildGodown();
    case 'trip': return buildTrip();
    default: return '<div class="card"><p>Page loading...</p></div>';
  }
}

function buildDashboard() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📊 Dashboard / डॅशबोर्ड</div>
        <div class="page-header-sub">आज: ${new Date().toLocaleDateString('mr-IN')}</div>
      </div>
    </div>
    <div class="grid-4">
      <div class="stat-card">
        <div class="stat-value" id="stat-delivered">0</div>
        <div class="stat-label">✅ Delivered Today</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" id="stat-intrip">0</div>
        <div class="stat-label">🚴 In Trip</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" id="stat-scheduled">0</div>
        <div class="stat-label">📋 Scheduled</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" id="stat-notdelivered">0</div>
        <div class="stat-label">❌ Not Delivered</div>
      </div>
    </div>
  `;
}

function buildDelivery() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🚴 Delivery Management / डिलिव्हरी व्यवस्थापन</div>
        <div class="page-header-sub">Total: ${deliveries.length}</div>
      </div>
      <label class="btn btn-primary btn-sm" style="cursor:pointer">
        📤 CSV Upload
        <input type="file" accept=".csv" style="display:none" onchange="handleCSVUpload(event)">
      </label>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:12px">
        <div style="display:flex;align-items:center;gap:6px">
          <span class="status-dot status-scheduled"></span> Scheduled / शेड्युल्ड
        </div>
        <div style="display:flex;align-items:center;gap:6px">
          <span class="status-dot status-intrip"></span> In Trip / रस्त्यावर
        </div>
        <div style="display:flex;align-items:center;gap:6px">
          <span class="status-dot status-delivered"></span> Delivered (OTP)
        </div>
        <div style="display:flex;align-items:center;gap:6px">
          <span class="status-dot status-emergency"></span> Emergency
        </div>
        <div style="display:flex;align-items:center;gap:6px">
          <span class="status-dot status-notdelivered"></span> Not Delivered
        </div>
      </div>
    </div>

    <div class="search-bar">
      <input class="search-input" id="delivSearch" placeholder="🔍 ग्राहक शोधा / Search customer, area, mobile..." oninput="filterDeliveries()">
      <select class="form-group" style="margin:0;width:180px" id="areaFilter" onchange="filterDeliveries()">
        <option value="">All Areas / सर्व भाग</option>
      </select>
      <select class="form-group" style="margin:0;width:160px" id="statusFilter" onchange="filterDeliveries()">
        <option value="">All Status</option>
        <option value="scheduled">Scheduled</option>
        <option value="intrip">In Trip</option>
        <option value="delivered">Delivered</option>
        <option value="emergency">Emergency</option>
        <option value="notdelivered">Not Delivered</option>
      </select>
    </div>

    <div id="deliveryList"></div>
  `;
}

function buildGodown() {
  return `<div class="card"><h2>🏭 Godown Stock</h2><p>Coming soon...</p></div>`;
}

function buildTrip() {
  return `<div class="card"><h2>🚛 Trip Management</h2><p>Coming soon...</p></div>`;
}

// DELIVERIES
async function loadDeliveries() {
  const res = await fetch('api.php?action=get_deliveries');
  const data = await res.json();
  if (data.success) {
    deliveries = data.data.deliveries;
    allAreas = [...new Set(deliveries.map(d => d.area))].sort();
    const areaSelect = document.getElementById('areaFilter');
    if (areaSelect) {
      areaSelect.innerHTML = '<option value="">All Areas / सर्व भाग</option>' +
        allAreas.map(a => `<option value="${a}">${a}</option>`).join('');
    }
    renderDeliveries(deliveries);
    updateDashboardStats();
  }
}

function filterDeliveries() {
  const search = (document.getElementById('delivSearch')?.value || '').toLowerCase();
  const area = document.getElementById('areaFilter')?.value || '';
  const status = document.getElementById('statusFilter')?.value || '';
  const filtered = deliveries.filter(d =>
    (!search || d.consumer_name.toLowerCase().includes(search) || d.mobile.includes(search) || d.area.toLowerCase().includes(search)) &&
    (!area || d.area === area) &&
    (!status || d.status === status)
  );
  renderDeliveries(filtered);
}

function renderDeliveries(list) {
  const byArea = {};
  list.forEach(d => {
    if (!byArea[d.area]) byArea[d.area] = [];
    byArea[d.area].push(d);
  });
  
  const html = Object.entries(byArea).map(([area, items]) => `
    <div style="margin-bottom:16px">
      <div style="font-size:13px;font-weight:700;color:var(--accent-yellow);margin-bottom:8px;display:flex;align-items:center;gap:8px">
        📍 ${area} <span style="font-size:11px;font-weight:400;color:var(--text-muted)">(${items.length} deliveries)</span>
      </div>
      ${items.map(d => renderDeliveryCard(d)).join('')}
    </div>
  `).join('');
  
  const el = document.getElementById('deliveryList');
  if (el) el.innerHTML = html || '<div class="card"><p>No deliveries found</p></div>';
}

function renderDeliveryCard(d) {
  const statusColors = {
    scheduled: '#3b82f6',
    intrip: '#eab308',
    delivered: '#22c55e',
    emergency: '#f97316',
    notdelivered: '#ef4444'
  };
  const statusClasses = {
    scheduled: 'status-scheduled',
    intrip: 'status-intrip',
    delivered: 'status-delivered',
    emergency: 'status-emergency',
    notdelivered: 'status-notdelivered'
  };
  const statusLabels = {
    scheduled: 'शेड्युल्ड',
    intrip: 'रस्त्यावर',
    delivered: 'डिलिव्हर (OTP)',
    emergency: 'डिलिव्हर (आपत्कालीन)',
    notdelivered: 'डिलिव्हर नाही'
  };
  const chipClasses = {
    scheduled: 'chip-blue',
    intrip: 'chip-yellow',
    delivered: 'chip-green',
    emergency: 'chip-orange',
    notdelivered: 'chip-red'
  };
  
  return `
    <div class="delivery-card">
      <div class="status-bar" style="background:${statusColors[d.status]}"></div>
      <div class="dcnum">${d.sl_no}</div>
      <div class="dcinfo">
        <div class="dcname">${d.consumer_name}</div>
        <div class="dcaddress">📍 ${d.address}</div>
        <div class="dcarea">🗂️ ${d.area} | 📄 CM: ${d.cash_memo} | 👤 ${d.operator_name}</div>
      </div>
      <div class="dcactions">
        <span class="chip ${chipClasses[d.status]}">
          <span class="status-dot ${statusClasses[d.status]}"></span> ${statusLabels[d.status]}
        </span>
        <div class="dcphone">📞 ${d.mobile}</div>
        ${d.otp ? `<div style="font-size:11px;color:var(--accent-green);margin-top:4px">OTP: ${d.otp}</div>` : ''}
        ${d.payment_mode ? `<div style="font-size:11px;color:var(--accent-blue);margin-top:2px">💳 ${d.payment_mode}</div>` : ''}
      </div>
    </div>
  `;
}

async function handleCSVUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const form = new FormData();
  form.append('csv_file', file);
  form.append('action', 'upload_csv');
  const res = await fetch('api.php', { method: 'POST', body: form });
  const data = await res.json();
  if (data.success) {
    alert(data.message);
    loadDeliveries();
  } else alert('Upload failed: ' + data.message);
}

function updateDashboardStats() {
  const stats = {
    delivered: deliveries.filter(d => d.status === 'delivered' || d.status === 'emergency').length,
    intrip: deliveries.filter(d => d.status === 'intrip').length,
    scheduled: deliveries.filter(d => d.status === 'scheduled').length,
    notdelivered: deliveries.filter(d => d.status === 'notdelivered').length
  };
  document.getElementById('stat-delivered').textContent = stats.delivered;
  document.getElementById('stat-intrip').textContent = stats.intrip;
  document.getElementById('stat-scheduled').textContent = stats.scheduled;
  document.getElementById('stat-notdelivered').textContent = stats.notdelivered;
}
</script>
</body>
</html>
