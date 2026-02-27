<?php
require_once 'config.php';
$currentUser = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shourya Bharatgas ERP v5 - Complete</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bpcl-blue: #003087; --bpcl-yellow: #FFD100; --bpcl-orange: #F7941D;
  --bg-dark: #0a0e1a; --bg-card: #0f1628; --bg-card2: #141d35;
  --border: #1e2d50; --border-bright: #2a4080;
  --text-primary: #e8eeff; --text-secondary: #8fa3cc; --text-muted: #4a5a80;
  --accent-green: #22c55e; --accent-blue: #4a90e2; --accent-yellow: #FFD100;
  --accent-orange: #f97316; --accent-red: #ef4444; --accent-purple: #a855f7;
  --font-main: 'Rajdhani', 'Noto Sans Devanagari', sans-serif;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font-main); background: linear-gradient(135deg, #000820 0%, #001a4d 50%, #000c2e 100%);
  color: var(--text-primary); min-height: 100vh;
}

#loginScreen { position: fixed; inset: 0; z-index: 1000; background: linear-gradient(135deg, #000820 0%, #001a4d 50%, #000c2e 100%); display: flex; align-items: center; justify-content: center; }
.login-card { width: 420px; max-width: 95vw; background: var(--bg-card); border: 1px solid var(--border-bright); border-radius: 16px; padding: 40px; box-shadow: 0 0 60px rgba(74,144,226,0.2), 0 8px 32px rgba(0,0,0,0.4); }
.login-logo { text-align: center; margin-bottom: 32px; }
.company-icon { width: 72px; height: 72px; background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow)); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 36px; box-shadow: 0 0 20px rgba(74,144,226,0.3); }
.login-logo h1 { font-size: 22px; font-weight: 700; color: var(--accent-yellow); }
.login-logo p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.login-field { margin-bottom: 16px; }
.login-field label { display: block; font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
.login-field input, .login-field select { width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 8px; color: var(--text-primary); font-size: 16px; padding: 12px 16px; font-family: var(--font-main); }
.login-field input:focus, .login-field select:focus { outline: none; border-color: var(--accent-blue); box-shadow: 0 0 20px rgba(74,144,226,0.3); }
.btn-login { width: 100%; background: linear-gradient(135deg, var(--accent-blue), var(--bpcl-blue)); color: white; border: none; border-radius: 8px; padding: 14px; font-size: 16px; font-weight: 700; cursor: pointer; font-family: var(--font-main); }

#app { display: none; }
.topnav { background: white; border-bottom: 1px solid #e5e7eb; padding: 12px 24px; display: flex; flex-direction: column; align-items: center; gap: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.topnav-row { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.topnav-logo { display: flex; align-items: center; gap: 12px; }
.logo-icon { width: 48px; height: 48px; background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow)); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.logo-text { font-size: 18px; font-weight: 700; color: var(--bpcl-blue); }
.logo-sub { font-size: 11px; color: #6b7280; }
.topnav-center { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
.nav-btn { padding: 10px 20px; background: white; border: 1px solid #d1d5db; border-radius: 20px; color: #374151; font-weight: 600; cursor: pointer; font-family: var(--font-main); transition: all 0.2s; font-size: 14px; }
.nav-btn:hover { background: #f3f4f6; border-color: #9ca3af; }
.nav-btn.active { background: #dbeafe; border-color: #3b82f6; color: #1e40af; }
.user-badge { display: flex; align-items: center; gap: 10px; }
.user-avatar { width: 40px; height: 40px; border-radius: 10px; background: var(--accent-blue); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; }
.btn-logout { padding: 8px 16px; background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3); border-radius: 8px; color: var(--accent-red); font-weight: 600; cursor: pointer; font-family: var(--font-main); }

.content { padding: 24px; max-width: 1600px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border); flex-wrap: wrap; gap: 16px; }
.page-header-title { font-size: 24px; font-weight: 700; color: var(--accent-yellow); }
.page-header-sub { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }

.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.2); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.card-title { font-size: 16px; font-weight: 700; color: var(--accent-yellow); }

.section-title { font-size: 14px; font-weight: 700; color: var(--accent-yellow); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }

.delivery-card { position: relative; background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 14px 14px 18px; margin-bottom: 10px; display: flex; gap: 14px; align-items: center; cursor: pointer; transition: all 0.2s; }
.delivery-card:hover { background: var(--bg-card2); border-color: var(--border-bright); box-shadow: 0 4px 12px rgba(74,144,226,0.15); }
.status-bar { position: absolute; left: 0; top: 0; bottom: 0; width: 4px; border-radius: 10px 0 0 10px; }
.dcnum { font-size: 24px; font-weight: 700; color: var(--text-muted); min-width: 40px; text-align: center; }
.dcinfo { flex: 1; }
.dcname { font-size: 15px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.dcaddress { font-size: 12px; color: var(--text-secondary); margin-bottom: 3px; }
.dcarea { font-size: 11px; color: var(--text-muted); }
.dcactions { text-align: right; }
.dcphone { font-size: 13px; color: var(--accent-blue); margin-top: 6px; font-weight: 600; }

.chip { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }
.chip-blue { background: rgba(59,130,246,0.15); color: #3b82f6; }
.chip-yellow { background: rgba(234,179,8,0.15); color: #eab308; }
.chip-green { background: rgba(34,197,94,0.15); color: #22c55e; }
.chip-orange { background: rgba(249,115,22,0.15); color: #f97316; }
.chip-red { background: rgba(239,68,68,0.15); color: #ef4444; }

.search-bar { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.search-input { flex: 1; min-width: 250px; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; color: var(--text-primary); font-size: 15px; font-family: var(--font-main); }

.btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; font-family: var(--font-main); }
.btn-primary { background: var(--accent-blue); color: white; }
.btn-success { background: var(--accent-green); color: white; }
.btn-warning { background: var(--accent-yellow); color: var(--bg-dark); }
.btn-danger { background: var(--accent-red); color: white; }
.btn-sm { padding: 6px 12px; font-size: 13px; }

.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; text-align: center; }
.stat-value { font-size: 48px; font-weight: 700; color: var(--accent-yellow); margin: 8px 0; }
.stat-label { font-size: 13px; color: var(--text-secondary); margin-top: 8px; }
.stat-sub { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.stat-icon { font-size: 40px; margin-bottom: 12px; }

.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 600; }
.form-group input, .form-group select, .form-group textarea { width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; color: var(--text-primary); font-family: var(--font-main); }
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }

.tabs { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; border-bottom: 2px solid var(--border); }
.tab-btn { padding: 12px 20px; background: rgba(255,255,255,0.03); border: none; border-bottom: 3px solid transparent; color: var(--text-secondary); font-weight: 600; cursor: pointer; border-radius: 8px 8px 0 0; font-family: var(--font-main); }
.tab-btn:hover { background: rgba(74,144,226,0.1); color: var(--text-primary); }
.tab-btn.active { background: rgba(74,144,226,0.15); border-bottom-color: var(--accent-blue); color: var(--accent-yellow); }
.tab-content { display: none; }
.tab-content.active { display: block; }

.alert { padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; border-left: 4px solid; font-size: 13px; }
.alert-info { background: rgba(59,130,246,0.1); border-color: #3b82f6; color: var(--accent-blue); }
.alert-warning { background: rgba(234,179,8,0.1); border-color: #eab308; color: var(--accent-yellow); }
.alert-success { background: rgba(34,197,94,0.1); border-color: #22c55e; color: var(--accent-green); }

table { width: 100%; border-collapse: collapse; }
th { background: var(--bg-card2); padding: 12px; text-align: left; border-bottom: 2px solid var(--border); font-weight: 700; font-size: 13px; }
td { padding: 12px; border-bottom: 1px solid var(--border); font-size: 13px; }

.payroll-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.payroll-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.payroll-name { font-size: 18px; font-weight: 700; color: var(--text-primary); }
.payroll-role { font-size: 12px; color: var(--text-secondary); padding: 4px 10px; background: rgba(74,144,226,0.15); border-radius: 12px; }
.payroll-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 16px; }
.payroll-section-title { font-size: 13px; font-weight: 700; color: var(--accent-blue); margin-bottom: 12px; }
.payroll-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; }
.payroll-total { border-top: 2px solid var(--border); padding-top: 12px; margin-top: 12px; }
.payroll-total .payroll-row { font-size: 16px; font-weight: 700; }
.payroll-actions { display: flex; gap: 8px; flex-wrap: wrap; }

.opening-stock-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }
.opening-stock-box { background: var(--bg-card2); border: 1px solid var(--border); border-radius: 12px; padding: 20px; text-align: center; }
.opening-stock-value { font-size: 48px; font-weight: 700; margin: 8px 0; }
.opening-stock-label { font-size: 12px; color: var(--text-secondary); }

.vehicle-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; display: flex; align-items: center; gap: 16px; }
.vehicle-icon { font-size: 32px; }
.vehicle-info { flex: 1; }
.vehicle-name { font-size: 16px; font-weight: 700; color: var(--text-primary); }
.vehicle-status { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.vehicle-location { font-size: 12px; color: var(--accent-blue); margin-top: 4px; }
.vehicle-update { font-size: 11px; color: var(--text-muted); margin-top: 4px; }

.empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
.empty-state-icon { font-size: 64px; margin-bottom: 16px; opacity: 0.3; }
.empty-state-text { font-size: 16px; margin-bottom: 8px; }
.empty-state-sub { font-size: 13px; }

@media (max-width: 768px) {
  .topnav { padding: 8px 12px; }
  .topnav-row { flex-direction: column; gap: 12px; }
  .content { padding: 12px; }
  .grid-2, .grid-3, .grid-4, .payroll-grid, .opening-stock-grid { grid-template-columns: 1fr; }
  .nav-btn { padding: 8px 14px; font-size: 13px; }
}
</style>
</head>
<body>

<div id="loginScreen" <?php if($currentUser) echo 'style="display:none"'; ?>>
  <div class="login-card">
    <div class="login-logo">
      <div class="company-icon">🔥</div>
      <h1>SHOURYA BHARATGAS</h1>
      <p>SAP: 187618 · Jaysingpur</p>
    </div>
    <form id="loginForm" onsubmit="return doLogin(event)">
      <div class="login-field">
        <label>वापरकर्ता / USER</label>
        <select name="username" required>
          <option value="">-- निवडा / Select --</option>
          <option value="owner">Vishal Patil (Owner)</option>
          <option value="owner2">Mrinmayi Patil (Owner)</option>
          <option value="manager">Rajesh Awale (Manager)</option>
          <option value="delivery_bhore">Vishwas Bhore</option>
          <option value="delivery_mahesh">Mahesh Patil</option>
          <option value="delivery_harun">Harun Fakir</option>
          <option value="delivery_magdum">Vishal Magdum</option>
        </select>
      </div>
      <div class="login-field">
        <label>पासवर्ड / PASSWORD</label>
        <input type="password" name="password" required value="1234">
      </div>
      <button type="submit" class="btn-login">🔐 लॉगिन / LOGIN</button>
    </form>
  </div>
</div>

<div id="app" <?php if($currentUser) echo 'style="display:block"'; ?>>
  <nav class="topnav">
    <div class="topnav-row">
      <div class="topnav-logo">
        <div class="logo-icon">🔥</div>
        <div>
          <div class="logo-text">SHOURYA BHARATGAS</div>
          <div class="logo-sub">SAP: 187618 · Jaysingpur</div>
        </div>
      </div>
      <div class="user-badge">
        <div class="user-avatar" id="navAvatar">VP</div>
        <div>
          <div style="font-weight:700;font-size:13px;color:#374151" id="navName"><?php echo $currentUser ? $currentUser['name'] : ''; ?></div>
          <div style="font-size:11px;color:#6b7280" id="navRole"><?php echo $currentUser ? $currentUser['designation'] : ''; ?></div>
        </div>
        <button class="btn-logout" onclick="doLogout()">↩ लॉगआउट</button>
      </div>
    </div>
    <div class="topnav-center" id="navButtons"></div>
  </nav>
  <div class="content" id="mainContent"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script>
let currentUser = <?php echo json_encode($currentUser); ?>;
let deliveries = [];
let allAreas = [];

async function doLogin(e) {
  e.preventDefault();
  const form = new FormData(e.target);
  const res = await fetch('api.php?action=login', { method: 'POST', body: form });
  const data = await res.json();
  if (data.success) location.reload();
  else alert(data.message);
  return false;
}

async function doLogout() {
  await fetch('api.php?action=logout');
  location.reload();
}

if (currentUser) {
  buildNav();
  showPage('dashboard');
  loadDeliveries();
}

function buildNav() {
  const navs = {
    owner: [
      {p:'dashboard',l:'📊 Dashboard'},
      {p:'delivery',l:'🚴 Delivery'},
      {p:'trip',l:'🚛 Trip'},
      {p:'godown',l:'🏭 Godown'},
      {p:'office',l:'🏢 Office'},
      {p:'bpcl',l:'📋 BPCL'},
      {p:'payroll',l:'💰 Payroll'},
      {p:'tracking',l:'📍 Tracking'},
      {p:'staff',l:'👥 Staff'},
      {p:'notices',l:'📢 Notices'}
    ],
    manager: [
      {p:'dashboard',l:'📊 Dashboard'},
      {p:'delivery',l:'🚴 Delivery'},
      {p:'trip',l:'🚛 Trip'},
      {p:'godown',l:'🏭 Godown'},
      {p:'office',l:'🏢 Office'},
      {p:'tracking',l:'📍 Tracking'},
      {p:'notices',l:'📢 Notices'}
    ],
    delivery: [
      {p:'dashboard',l:'📊 Dashboard'},
      {p:'delivery',l:'🚴 Delivery'},
      {p:'trip',l:'🚛 Trip'},
      {p:'notices',l:'📢 Notices'}
    ],
    bda: [
      {p:'dashboard',l:'📊 Dashboard'},
      {p:'delivery',l:'🚴 Delivery'},
      {p:'notices',l:'📢 Notices'}
    ]
  };
  const userNavs = navs[currentUser.role] || navs.owner;
  document.getElementById('navButtons').innerHTML = userNavs.map(n => 
    `<button class="nav-btn ${n.p==='dashboard'?'active':''}" data-page="${n.p}" onclick="showPage('${n.p}')">${n.l}</button>`
  ).join('');
}

function showPage(page) {
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.page === page));
  document.getElementById('mainContent').innerHTML = buildPage(page);
  if (page === 'delivery' && deliveries.length > 0) {
    setTimeout(() => renderDeliveries(deliveries), 50);
  }
}

function switchTab(btn, tabId) {
  const parent = btn.closest('.tabs');
  parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const nextEl = parent.nextElementSibling;
  if (nextEl) {
    nextEl.querySelectorAll('.tab-content').forEach(t => {
      t.classList.toggle('active', t.id === tabId);
    });
  }
}

function buildPage(page) {
  const pages = {
    dashboard: buildDashboard,
    delivery: buildDelivery,
    trip: buildTrip,
    godown: buildGodown,
    office: buildOffice,
    bpcl: buildBpcl,
    payroll: buildPayroll,
    tracking: buildTracking,
    staff: buildStaff,
    notices: buildNotices
  };
  return pages[page] ? pages[page]() : '<div class="card"><p>Loading...</p></div>';
}

// CONTINUED IN NEXT MESSAGE DUE TO LENGTH...

function buildDashboard() {
  const delivered = deliveries.filter(d => d.status === 'delivered' || d.status === 'emergency').length;
  const intrip = deliveries.filter(d => d.status === 'intrip').length;
  const scheduled = deliveries.filter(d => d.status === 'scheduled').length;
  const notdelivered = deliveries.filter(d => d.status === 'notdelivered').length;
  
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📊 Dashboard / डॅशबोर्ड</div>
        <div class="page-header-sub">आज: ${new Date().toLocaleDateString('mr-IN')}</div>
      </div>
    </div>
    
    <div class="grid-4">
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-value" style="color:var(--accent-green)">${delivered}</div>
        <div class="stat-label">Delivered Today</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🚛</div>
        <div class="stat-value" style="color:var(--accent-yellow)">${intrip}</div>
        <div class="stat-label">In Trip</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-value" style="color:var(--accent-blue)">${scheduled}</div>
        <div class="stat-label">Scheduled</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">❌</div>
        <div class="stat-value" style="color:var(--accent-red)">${notdelivered}</div>
        <div class="stat-label">Not Delivered</div>
      </div>
    </div>
    
    ${deliveries.length === 0 ? `
      <div class="empty-state">
        <div class="empty-state-icon">📦</div>
        <div class="empty-state-text">No deliveries yet</div>
        <div class="empty-state-sub">Upload CSV file in Delivery page to get started</div>
      </div>
    ` : ''}
  `;
}

function buildDelivery() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🚴 Delivery Management / डिलिव्हरी व्यवस्थापन</div>
        <div class="page-header-sub">Total: ${deliveries.length} | Delivered: ${deliveries.filter(d => d.status === 'delivered' || d.status === 'emergency').length}</div>
      </div>
      <div style="display:flex;gap:8px">
        <label class="btn btn-primary btn-sm" style="cursor:pointer">
          📤 CSV Upload
          <input type="file" accept=".csv" onchange="handleCSVUpload(event)" style="display:none">
        </label>
      </div>
    </div>
    
    ${deliveries.length > 0 ? `
      <div class="search-bar">
        <input type="text" class="search-input" placeholder="🔍 ग्राहक शोधा / Search customer, area, mobile..." oninput="filterDeliveries()" id="searchInput">
        <select class="search-input" style="flex:0.5" onchange="filterDeliveries()" id="areaFilter">
          <option value="">All Areas / सर्व भाग</option>
          ${allAreas.map(a => `<option value="${a}">${a}</option>`).join('')}
        </select>
        <select class="search-input" style="flex:0.5" onchange="filterDeliveries()" id="statusFilter">
          <option value="">All Status</option>
          <option value="scheduled">Scheduled</option>
          <option value="intrip">In Trip</option>
          <option value="delivered">Delivered (OTP)</option>
          <option value="emergency">Delivered (Emergency)</option>
          <option value="notdelivered">Not Delivered</option>
        </select>
      </div>
      
      <div id="deliveryList"></div>
    ` : `
      <div class="empty-state">
        <div class="empty-state-icon">📄</div>
        <div class="empty-state-text">No deliveries loaded</div>
        <div class="empty-state-sub">Click "CSV Upload" above to upload delivery list</div>
      </div>
    `}
  `;
}

function buildTrip() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🗺 ट्रिप / Trip Management</div>
        <div class="page-header-sub">${currentUser.name} — आजचा ट्रिप सारांश</div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-title">📦 गोदाऊन स्टॉक — सकाळची मोजणी / Morning Stock Count</div>
      <div class="alert alert-warning">
        ⚠️ पहिल्या येणाऱ्याने मोजणी करावी — मागील दिवसाच्या BPCL स्टॉकशी जुळवा<br>
        First arrival enters count — must match previous BPCL closing stock.
      </div>
      
      <div class="section-title">🟢 14.2 KG भरलेले (FILLED)</div>
      <div style="background:rgba(34,197,94,0.05);padding:16px;border-radius:8px;margin-bottom:20px">
        <div style="margin-bottom:8px;font-size:12px;color:var(--accent-green)">फॉर्म्युला: उभी ओळ × आडवी ओळ + अधिक ओळ = एकूण संख्या</div>
        <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
          <div class="form-group" style="margin:0;flex:1;min-width:100px">
            <label>उभी ओळ</label>
            <input type="number" id="full_r" value="0" oninput="calcGodownGrid()" style="text-align:center">
          </div>
          <span style="font-size:20px">×</span>
          <div class="form-group" style="margin:0;flex:1;min-width:100px">
            <label>आडवी ओळ</label>
            <input type="number" id="full_c" value="0" oninput="calcGodownGrid()" style="text-align:center">
          </div>
          <span style="font-size:20px">+</span>
          <div class="form-group" style="margin:0;flex:1;min-width:100px">
            <label>अधिक ओळ</label>
            <input type="number" id="full_e" value="0" oninput="calcGodownGrid()" style="text-align:center">
          </div>
          <span style="font-size:20px">=</span>
          <div style="flex:1;min-width:100px;text-align:center">
            <div style="font-size:11px;color:var(--text-muted)">एकूण संख्या</div>
            <div style="font-size:32px;font-weight:700;color:var(--accent-green)" id="fullTotal">0</div>
          </div>
        </div>
      </div>
      
      <button class="btn btn-success">✅ सकाळचा साठा जतन करा / Save Morning Count</button>
    </div>
  `;
}

function calcGodownGrid() {
  const fr = parseInt(document.getElementById('full_r')?.value || 0);
  const fc = parseInt(document.getElementById('full_c')?.value || 0);
  const fe = parseInt(document.getElementById('full_e')?.value || 0);
  const fullTotal = (fr * fc) + fe;
  document.getElementById('fullTotal').textContent = fullTotal;
}

function buildGodown() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🏭 गोदाम / Godown Stock</div>
        <div class="page-header-sub">SAP Code: 187618 · BPCL Authorized Godown</div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-title">📊 Current Stock</div>
      <div class="grid-4">
        <div class="stat-card">
          <div class="stat-icon">🟢</div>
          <div class="stat-label">14.2 kg Full</div>
          <div class="stat-value" style="color:var(--accent-green)">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⚪</div>
          <div class="stat-label">14.2 kg Empty</div>
          <div class="stat-value" style="color:var(--text-secondary)">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🟡</div>
          <div class="stat-label">5 kg Full</div>
          <div class="stat-value" style="color:var(--accent-yellow)">0</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🔴</div>
          <div class="stat-label">19 kg Full</div>
          <div class="stat-value" style="color:var(--accent-orange)">0</div>
        </div>
      </div>
    </div>
  `;
}

function buildOffice() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🏢 Office Summary / ऑफिस सारांश</div>
        <div class="page-header-sub">${new Date().toLocaleDateString('en-GB')}</div>
      </div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'office-sales')">💰 Sales</button>
      <button class="tab-btn" onclick="switchTab(this,'office-stock')">📦 Stock</button>
      <button class="tab-btn" onclick="switchTab(this,'office-expenses')">💸 Expenses</button>
      <button class="tab-btn" onclick="switchTab(this,'office-dayend')">📋 Day End</button>
    </div>
    
    <div>
      <div class="tab-content active" id="office-sales">
        <div class="card">
          <div class="card-title">💰 Today's Sales</div>
          <table>
            <tr><th>Payment Mode</th><th style="text-align:right">Count</th><th style="text-align:right">Amount</th></tr>
            <tr><td>Cash</td><td style="text-align:right">0</td><td style="text-align:right">₹0</td></tr>
            <tr><td>Online</td><td style="text-align:right">0</td><td style="text-align:right">₹0</td></tr>
            <tr style="font-weight:700"><td>Total</td><td style="text-align:right">0</td><td style="text-align:right">₹0</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="office-stock">
        <div class="card">
          <div class="card-title">📦 Office Stock</div>
          <div class="grid-4">
            <div class="stat-card"><div class="stat-value" style="color:var(--accent-green)">0</div><div class="stat-label">14.2 kg Full</div></div>
            <div class="stat-card"><div class="stat-value" style="color:var(--text-secondary)">0</div><div class="stat-label">14.2 kg Empty</div></div>
            <div class="stat-card"><div class="stat-value" style="color:var(--accent-yellow)">0</div><div class="stat-label">5 kg Full</div></div>
            <div class="stat-card"><div class="stat-value" style="color:var(--accent-orange)">0</div><div class="stat-label">19 kg Full</div></div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="office-expenses">
        <div class="card">
          <div class="card-title">💸 Expenses</div>
          <div class="form-row">
            <div class="form-group"><label>Category</label><input type="text"></div>
            <div class="form-group"><label>Amount</label><input type="number"></div>
            <div class="form-group"><label>Paid To</label><input type="text"></div>
          </div>
          <button class="btn btn-primary">Add Expense</button>
        </div>
      </div>
      
      <div class="tab-content" id="office-dayend">
        <div class="card">
          <div class="card-title">📋 Day End</div>
          <p>Day end reconciliation coming soon</p>
        </div>
      </div>
    </div>
  `;
}

function buildBpcl() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📋 BPCL Verification</div>
      </div>
      <label class="btn btn-primary btn-sm" style="cursor:pointer">
        📤 Upload Day End PDF
        <input type="file" accept=".pdf" style="display:none">
      </label>
    </div>
    
    <div class="card">
      <div class="card-title">📊 Product Codes Reference</div>
      <table>
        <tr><th>Code</th><th>Description</th></tr>
        <tr><td>5350+5370</td><td>14.2 kg Domestic (Full & Empty)</td></tr>
        <tr><td>5240/5250/5260</td><td>5 kg Cylinders</td></tr>
        <tr><td>5400</td><td>19 kg Commercial</td></tr>
        <tr><td>5450</td><td>19 kg Cutting</td></tr>
        <tr><td>BPCDPR</td><td>14.2 kg DPR</td></tr>
      </table>
    </div>
  `;
}

function buildPayroll() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">💰 Payroll / पगार व्यवस्थापन</div>
      </div>
    </div>
    
    <div class="alert alert-info">
      <strong>वेतन नियम:</strong> Urban: ₹8/cylinder | Rural: ₹7/cylinder | Pair Bonus: ₹200/day
    </div>
    
    <div class="card">
      <div class="card-title">🚴 Delivery Men Wages</div>
      <div class="empty-state">
        <div class="empty-state-icon">💰</div>
        <div class="empty-state-text">No wage data available</div>
        <div class="empty-state-sub">Wages calculated after trip closures</div>
      </div>
    </div>
  `;
}

function buildTracking() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📍 Live Tracking</div>
      </div>
      <span class="chip chip-green">LIVE</span>
    </div>
    
    <div class="grid-2">
      <div class="vehicle-card">
        <div class="vehicle-icon">🚐</div>
        <div class="vehicle-info">
          <div class="vehicle-name">Vishwas Bhore</div>
          <div class="vehicle-status">At Godown</div>
          <div class="vehicle-location">📍 Godown</div>
          <div class="vehicle-update">Last update: Just now</div>
        </div>
      </div>
      <div class="vehicle-card">
        <div class="vehicle-icon">🏍</div>
        <div class="vehicle-info">
          <div class="vehicle-name">Mahesh Patil</div>
          <div class="vehicle-status">At Godown</div>
          <div class="vehicle-location">📍 Godown</div>
          <div class="vehicle-update">Last update: Just now</div>
        </div>
      </div>
    </div>
  `;
}

function buildStaff() {
  return `
    <div class="page-header">
      <div class="page-header-title">👥 Staff Management</div>
    </div>
    <div class="card">
      <table>
        <thead><tr><th>Name</th><th>Role</th><th>Mobile</th></tr></thead>
        <tbody>
          <tr><td>Vishal Patil</td><td>Owner</td><td>7887456789</td></tr>
          <tr><td>Mrinmayi Patil</td><td>Owner</td><td>8080802880</td></tr>
          <tr><td>Rajesh Awale</td><td>Manager</td><td>8007183197</td></tr>
          <tr><td>Vishwas Bhore</td><td>Delivery</td><td>7643982982</td></tr>
          <tr><td>Mahesh Patil</td><td>Delivery</td><td>8830669611</td></tr>
          <tr><td>Harun Fakir</td><td>Delivery</td><td>9970660901</td></tr>
          <tr><td>Vishal Magdum</td><td>Delivery</td><td>9096853954</td></tr>
        </tbody>
      </table>
    </div>
  `;
}

function buildNotices() {
  return `
    <div class="page-header">
      <div class="page-header-title">📢 Notices</div>
      <button class="btn btn-primary btn-sm">+ New Notice</button>
    </div>
    <div class="empty-state">
      <div class="empty-state-icon">📢</div>
      <div class="empty-state-text">No notices yet</div>
    </div>
  `;
}

async function loadDeliveries() {
  try {
    const res = await fetch('api.php?action=get_deliveries');
    const data = await res.json();
    if (data.success && data.deliveries) {
      deliveries = data.deliveries;
      allAreas = [...new Set(deliveries.map(d => d.area))].sort();
      if (document.getElementById('deliveryList')) {
        renderDeliveries(deliveries);
      }
    }
  } catch (e) {
    console.error('Load error:', e);
  }
}

function renderDeliveries(list) {
  const container = document.getElementById('deliveryList');
  if (!container) return;
  
  const byArea = {};
  list.forEach(d => {
    if (!byArea[d.area]) byArea[d.area] = [];
    byArea[d.area].push(d);
  });
  
  const statusColors = {
    scheduled: '#3b82f6',
    intrip: '#eab308',
    delivered: '#22c55e',
    emergency: '#f97316',
    notdelivered: '#ef4444'
  };
  
  let html = '';
  Object.keys(byArea).sort().forEach(area => {
    html += `<div style="margin-bottom:20px">`;
    html += `<div style="font-weight:700;color:var(--accent-yellow);margin-bottom:8px">📍 ${area} (${byArea[area].length} deliveries)</div>`;
    byArea[area].forEach((d, i) => {
      html += `
        <div class="delivery-card">
          <div class="status-bar" style="background:${statusColors[d.status] || '#666'}"></div>
          <div class="dcnum">${i + 1}</div>
          <div class="dcinfo">
            <div class="dcname">${d.consumer_name}</div>
            <div class="dcaddress">📍 ${d.address}</div>
            <div class="dcarea">🗂 ${d.area} | 📄 CM: ${d.cash_memo_no} | 👤 ${d.delivery_man || 'Unassigned'}</div>
          </div>
          <div class="dcactions">
            <span class="chip chip-${d.status === 'scheduled' ? 'blue' : d.status === 'intrip' ? 'yellow' : d.status === 'delivered' ? 'green' : d.status === 'emergency' ? 'orange' : 'red'}">${d.status}</span>
            <div class="dcphone">📞 ${d.mobile}</div>
            ${d.otp ? `<div style="font-size:11px;color:var(--accent-green);margin-top:4px">OTP: ${d.otp}</div>` : ''}
          </div>
        </div>
      `;
    });
    html += `</div>`;
  });
  
  container.innerHTML = html;
}

function filterDeliveries() {
  const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
  const areaFilter = document.getElementById('areaFilter')?.value || '';
  const statusFilter = document.getElementById('statusFilter')?.value || '';
  
  const filtered = deliveries.filter(d => {
    const matchesSearch = !searchTerm || 
      d.consumer_name.toLowerCase().includes(searchTerm) ||
      d.mobile.includes(searchTerm) ||
      d.area.toLowerCase().includes(searchTerm);
    const matchesArea = !areaFilter || d.area === areaFilter;
    const matchesStatus = !statusFilter || d.status === statusFilter;
    return matchesSearch && matchesArea && matchesStatus;
  });
  
  renderDeliveries(filtered);
}

async function handleCSVUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: async function(results) {
      const rows = results.data.filter(r => r.ConsumerName && r.CashMemoNo);
      
      const formData = new FormData();
      formData.append('csv_data', JSON.stringify(rows));
      
      try {
        const res = await fetch('api.php?action=upload_csv', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        
        if (data.success) {
          alert(`✅ Loaded ${data.count} deliveries!`);
          await loadDeliveries();
          showPage('delivery');
        } else {
          alert('❌ Error: ' + data.message);
        }
      } catch (err) {
        alert('❌ Upload failed: ' + err.message);
      }
    }
  });
}
</script>
</body>
</html>
