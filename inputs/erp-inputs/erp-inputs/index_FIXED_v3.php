<?php
require_once 'config.php';
$currentUser = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shourya Bharatgas ERP v3 - Complete</title>
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
  font-family: var(--font-main);
  background: linear-gradient(135deg, #000820 0%, #001a4d 50%, #000c2e 100%);
  color: var(--text-primary); min-height: 100vh;
}

#loginScreen {
  position: fixed; inset: 0; z-index: 1000;
  background: linear-gradient(135deg, #000820 0%, #001a4d 50%, #000c2e 100%);
  display: flex; align-items: center; justify-content: center;
}
.login-card {
  width: 420px; max-width: 95vw; background: var(--bg-card);
  border: 1px solid var(--border-bright); border-radius: 16px; padding: 40px;
  box-shadow: 0 0 60px rgba(74,144,226,0.2), 0 8px 32px rgba(0,0,0,0.4);
}
.login-logo { text-align: center; margin-bottom: 32px; }
.company-icon {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow));
  border-radius: 16px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px; font-size: 36px; box-shadow: 0 0 20px rgba(74,144,226,0.3);
}
.login-logo h1 { font-size: 22px; font-weight: 700; color: var(--accent-yellow); }
.login-logo p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.login-field { margin-bottom: 16px; }
.login-field label { display: block; font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
.login-field input, .login-field select {
  width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border);
  border-radius: 8px; color: var(--text-primary); font-size: 16px; padding: 12px 16px;
  font-family: var(--font-main);
}
.login-field select option {
  background: #1a1f35;
  color: #ffffff;
  padding: 8px;
}
.login-field input:focus, .login-field select:focus {
  outline: none; border-color: var(--accent-blue); box-shadow: 0 0 20px rgba(74,144,226,0.3);
}
.btn-login {
  width: 100%; background: linear-gradient(135deg, var(--accent-blue), var(--bpcl-blue));
  color: white; border: none; border-radius: 8px; padding: 14px; font-size: 16px; font-weight: 700; cursor: pointer;
}

#app { display: none; }
.topnav {
  background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
  border-bottom: 1px solid var(--border-bright); padding: 16px 24px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.topnav-logo { display: flex; align-items: center; gap: 12px; }
.logo-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow));
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
  font-size: 24px; box-shadow: 0 0 15px rgba(255,209,0,0.2);
}
.logo-text { font-size: 18px; font-weight: 700; color: var(--accent-yellow); }
.logo-sub { font-size: 11px; color: var(--text-muted); }
.topnav-center { display: flex; gap: 8px; flex-wrap: wrap; }
.nav-btn {
  padding: 10px 18px; background: rgba(255,255,255,0.03);
  border: 1px solid var(--border); border-radius: 8px;
  color: var(--text-secondary); font-weight: 600; cursor: pointer;
}
.nav-btn:hover { background: rgba(74,144,226,0.1); border-color: var(--accent-blue); }
.nav-btn.active {
  background: linear-gradient(135deg, rgba(74,144,226,0.2), rgba(0,48,135,0.2));
  border-color: var(--accent-blue); color: var(--accent-yellow);
}
.user-badge { display: flex; align-items: center; gap: 10px; }
.user-avatar {
  width: 40px; height: 40px; border-radius: 10px; background: var(--accent-blue);
  color: white; display: flex; align-items: center; justify-content: center;
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
  margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border);
}
.page-header-title { font-size: 24px; font-weight: 700; color: var(--accent-yellow); }
.page-header-sub { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }

.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border);
}
.card-title { font-size: 16px; font-weight: 700; color: var(--accent-yellow); }

.section-title {
  font-size: 14px; font-weight: 700; color: var(--accent-yellow);
  margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border);
}

.delivery-card {
  position: relative; background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 14px 14px 18px; margin-bottom: 10px;
  display: flex; gap: 14px; align-items: center; cursor: pointer; transition: all 0.2s;
}
.delivery-card:hover {
  background: var(--bg-card2); border-color: var(--border-bright);
  box-shadow: 0 4px 12px rgba(74,144,226,0.15);
}
.status-bar { position: absolute; left: 0; top: 0; bottom: 0; width: 4px; border-radius: 10px 0 0 10px; }
.dcnum { font-size: 24px; font-weight: 700; color: var(--text-muted); min-width: 40px; text-align: center; }
.dcinfo { flex: 1; }
.dcname { font-size: 15px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.dcaddress { font-size: 12px; color: var(--text-secondary); margin-bottom: 3px; }
.dcarea { font-size: 11px; color: var(--text-muted); }
.dcactions { text-align: right; }
.dcphone { font-size: 13px; color: var(--accent-blue); margin-top: 6px; font-weight: 600; }

.chip {
  display: inline-block; padding: 4px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 700;
}
.chip-blue { background: rgba(59,130,246,0.15); color: #3b82f6; }
.chip-yellow { background: rgba(234,179,8,0.15); color: #eab308; }
.chip-green { background: rgba(34,197,94,0.15); color: #22c55e; }
.chip-orange { background: rgba(249,115,22,0.15); color: #f97316; }
.chip-red { background: rgba(239,68,68,0.15); color: #ef4444; }

.status-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px;
}
.status-scheduled { background: #3b82f6; }
.status-intrip { background: #eab308; }
.status-delivered { background: #22c55e; }
.status-emergency { background: #f97316; }
.status-notdelivered { background: #ef4444; }

.search-bar { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.search-input {
  flex: 1; min-width: 250px; background: rgba(255,255,255,0.05);
  border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px;
  color: var(--text-primary); font-size: 15px;
}

.btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; }
.btn-primary { background: var(--accent-blue); color: white; }
.btn-success { background: var(--accent-green); color: white; }
.btn-warning { background: var(--accent-yellow); color: var(--bg-dark); }
.btn-danger { background: var(--accent-red); color: white; }
.btn-sm { padding: 6px 12px; font-size: 13px; }

.stat-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; text-align: center;
}
.stat-value { font-size: 36px; font-weight: 700; color: var(--accent-yellow); }
.stat-label { font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
.stat-sub { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.stat-icon { font-size: 32px; margin-bottom: 8px; }

.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 600; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 14px; color: var(--text-primary);
}
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }

.trip-row {
  display: flex; justify-content: space-between; padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.tabs {
  display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;
  border-bottom: 2px solid var(--border);
}
.tab-btn {
  padding: 12px 20px; background: rgba(255,255,255,0.03);
  border: none; border-bottom: 3px solid transparent;
  color: var(--text-secondary); font-weight: 600; cursor: pointer;
  border-radius: 8px 8px 0 0;
}
.tab-btn:hover { background: rgba(74,144,226,0.1); color: var(--text-primary); }
.tab-btn.active {
  background: rgba(74,144,226,0.15); border-bottom-color: var(--accent-blue);
  color: var(--accent-yellow);
}
.tab-content { display: none; }
.tab-content.active { display: block; }

.alert {
  padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;
  border-left: 4px solid; font-size: 13px;
}
.alert-info { background: rgba(59,130,246,0.1); border-color: #3b82f6; color: var(--accent-blue); }
.alert-warning { background: rgba(234,179,8,0.1); border-color: #eab308; color: var(--accent-yellow); }
.alert-success { background: rgba(34,197,94,0.1); border-color: #22c55e; color: var(--accent-green); }

table { width: 100%; border-collapse: collapse; }
th {
  background: var(--bg-card2); padding: 12px; text-align: left;
  border-bottom: 2px solid var(--border); font-weight: 700; font-size: 13px;
}
td { padding: 12px; border-bottom: 1px solid var(--border); font-size: 13px; }

@media (max-width: 768px) {
  .topnav { flex-direction: column; gap: 12px; }
  .content { padding: 12px; }
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
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
        <input type="password" name="password" required>
      </div>
      <button type="submit" class="btn-login">🔐 लॉगिन / LOGIN</button>
    </form>
  </div>
</div>

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
          <div style="font-weight:700;font-size:13px" id="navName"><?php echo $currentUser ? $currentUser['name'] : ''; ?></div>
          <div style="font-size:11px;color:var(--text-muted)" id="navRole"><?php echo $currentUser ? $currentUser['designation'] : ''; ?></div>
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
      {p:'staff',l:'👥 Staff'},
      {p:'notices',l:'📢 Notices'}
    ],
    manager: [
      {p:'dashboard',l:'📊 Dashboard'},
      {p:'delivery',l:'🚴 Delivery'},
      {p:'trip',l:'🚛 Trip'},
      {p:'godown',l:'🏭 Godown'},
      {p:'office',l:'🏢 Office'},
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
  if (page === 'delivery' && deliveries.length > 0) setTimeout(() => renderDeliveries(deliveries), 50);
}

function switchTab(btn, tabId) {
  const parent = btn.parentElement;
  parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  parent.parentElement.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.getElementById(tabId)?.classList.add('active');
}

function buildPage(page) {
  switch(page) {
    case 'dashboard': return buildDashboard();
    case 'delivery': return buildDelivery();
    case 'trip': return buildTrip();
    case 'godown': return buildGodown();
    case 'office': return buildOffice();
    case 'bpcl': return buildBpcl();
    case 'payroll': return buildPayroll();
    case 'staff': return buildStaff();
    case 'notices': return buildNotices();
    default: return '<div class="card"><p>Loading...</p></div>';
  }
}

// Continuing in next part due to length...

function buildDashboard() {
  return `
    <div class="page-header">
      <div><div class="page-header-title">📊 Dashboard / डॅशबोर्ड</div><div class="page-header-sub">आज: ${new Date().toLocaleDateString('mr-IN')}</div></div>
    </div>
    <div class="grid-4">
      <div class="stat-card"><div class="stat-value" id="stat-delivered">0</div><div class="stat-label">✅ Delivered Today</div></div>
      <div class="stat-card"><div class="stat-value" id="stat-intrip">0</div><div class="stat-label">🚴 In Trip</div></div>
      <div class="stat-card"><div class="stat-value" id="stat-scheduled">0</div><div class="stat-label">📋 Scheduled</div></div>
      <div class="stat-card"><div class="stat-value" id="stat-notdelivered">0</div><div class="stat-label">❌ Not Delivered</div></div>
    </div>
  `;
}

function buildDelivery() {
  return `
    <div class="page-header">
      <div><div class="page-header-title">🚴 Delivery Management / डिलिव्हरी व्यवस्थापन</div><div class="page-header-sub">Total: ${deliveries.length}</div></div>
      <label class="btn btn-primary btn-sm" style="cursor:pointer">📤 CSV Upload<input type="file" accept=".csv" style="display:none" onchange="handleCSVUpload(event)"></label>
    </div>
    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:12px">
        <div style="display:flex;align-items:center;gap:6px"><span class="status-dot status-scheduled"></span> Scheduled / शेड्युल्ड</div>
        <div style="display:flex;align-items:center;gap:6px"><span class="status-dot status-intrip"></span> In Trip / रस्त्यावर</div>
        <div style="display:flex;align-items:center;gap:6px"><span class="status-dot status-delivered"></span> Delivered (OTP)</div>
        <div style="display:flex;align-items:center;gap:6px"><span class="status-dot status-emergency"></span> Emergency</div>
        <div style="display:flex;align-items:center;gap:6px"><span class="status-dot status-notdelivered"></span> Not Delivered</div>
      </div>
    </div>
    <div class="search-bar">
      <input class="search-input" id="delivSearch" placeholder="🔍 ग्राहक शोधा / Search..." oninput="filterDeliveries()">
      <select class="form-group" style="margin:0;width:180px" id="areaFilter" onchange="filterDeliveries()"><option value="">All Areas / सर्व भाग</option></select>
      <select class="form-group" style="margin:0;width:160px" id="statusFilter" onchange="filterDeliveries()">
        <option value="">All Status</option><option value="scheduled">Scheduled</option><option value="intrip">In Trip</option>
        <option value="delivered">Delivered</option><option value="emergency">Emergency</option><option value="notdelivered">Not Delivered</option>
      </select>
    </div>
    <div id="deliveryList"></div>
  `;
}

function buildTrip() {
  const bdas = [{area:'Kondigre',owner:'Sarika Waghmode'},{area:'Nimshirgav',owner:'Kumar Thomake'},{area:'Nimshirgav',owner:'Lakhane'},{area:'Danoli',owner:'Manoj'}];
  return `<div class="page-header"><div><div class="page-header-title">🚛 ट्रिप / Trip Management</div><div class="page-header-sub">${currentUser.name}</div></div></div>
    <div class="card"><div style="font-size:16px;font-weight:700;color:var(--accent-yellow);margin-bottom:12px">📦 गोदाऊन स्टॉक — सकाळची मोजणी</div>
    <div style="background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.2);border-radius:8px;padding:12px;margin-bottom:16px;font-size:12px">⚠️ <strong>पहिल्या येणाऱ्याने मोजणी करावी</strong></div>
    <div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.2);border-radius:10px;padding:16px;margin-bottom:16px">
      <div style="font-size:14px;font-weight:700;color:var(--accent-green);margin-bottom:10px">🟢 14.2 KG भरलेले</div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center">
        <div style="text-align:center"><div style="font-size:11px;color:var(--text-muted);margin-bottom:4px">उभी ओळ</div>
        <input type="number" id="full_r" placeholder="10" oninput="calcGodownGrid()" style="width:70px;padding:8px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:6px;color:var(--text-primary);font-size:18px;font-weight:700;text-align:center"></div>
        <span style="font-size:20px;color:var(--text-muted)">×</span>
        <div style="text-align:center"><div style="font-size:11px;color:var(--text-muted);margin-bottom:4px">आडवी ओळ</div>
        <input type="number" id="full_c" placeholder="12" oninput="calcGodownGrid()" style="width:70px;padding:8px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:6px;color:var(--text-primary);font-size:18px;font-weight:700;text-align:center"></div>
        <span style="font-size:20px;color:var(--text-muted)">+</span>
        <div style="text-align:center"><div style="font-size:11px;color:var(--text-muted);margin-bottom:4px">अधिक ओळ</div>
        <input type="number" id="full_e" placeholder="8" oninput="calcGodownGrid()" style="width:70px;padding:8px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:6px;color:var(--text-primary);font-size:18px;font-weight:700;text-align:center"></div>
        <span style="font-size:20px;color:var(--text-muted)">=</span>
        <div style="text-align:center"><div style="font-size:11px;color:var(--text-muted);margin-bottom:4px">एकूण</div>
        <div id="full_total" style="font-size:28px;font-weight:700;min-width:70px;text-align:center;background:rgba(34,197,94,0.15);border-radius:8px;padding:6px;color:var(--accent-green)">—</div></div>
      </div>
    </div>
    ${['e1','e2','e3'].map((p,i)=>{const l=['फुडून उजवीकडे','दरवाज्याच्या उजवीकडे','दरवाज्याच्या डावीकडे'][i];return`<div style="margin-bottom:14px;padding:10px;background:rgba(255,255,255,0.03);border-radius:8px">
      <div style="font-size:12px;font-weight:700;color:var(--accent-blue);margin-bottom:8px">📍 ${l}</div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:14px">
        <span>(</span><input type="number" id="${p}_r" placeholder="6" oninput="calcGodownGrid()" style="width:60px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);font-size:16px;text-align:center">
        <span>×</span><input type="number" id="${p}_c" placeholder="5" oninput="calcGodownGrid()" style="width:60px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);font-size:16px;text-align:center">
        <span>+</span><input type="number" id="${p}_a" placeholder="3" oninput="calcGodownGrid()" style="width:60px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);font-size:16px;text-align:center">
        <span>)×2+</span><input type="number" id="${p}_s" placeholder="4" oninput="calcGodownGrid()" style="width:60px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);font-size:16px;text-align:center">
        <span>=</span><span id="${p}_total" style="font-size:20px;font-weight:700;padding:6px 12px;background:rgba(148,163,184,0.1);border-radius:6px;min-width:60px;text-align:center;color:var(--text-secondary)">—</span>
      </div></div>`}).join('')}
    <div style="margin-top:12px;display:flex;align-items:center;justify-content:space-between;padding:10px 16px;background:rgba(148,163,184,0.1);border-radius:8px">
      <span style="font-weight:700;font-size:14px">एकूण रिकामे</span><span id="empty_total" style="font-size:28px;font-weight:700;color:var(--text-secondary)">—</span>
    </div>
    <button class="btn btn-success" style="width:100%;margin-top:16px" onclick="alert('✅ Stock saved!')">✅ Save Morning Count</button>
    </div>
    <div class="card"><div style="font-size:16px;font-weight:700;color:var(--accent-yellow);margin-bottom:12px">📋 ट्रिप सारांश / Trip Summary</div>
    <div style="background:var(--bg-card2);padding:16px;border-radius:8px">
      <div class="trip-row"><span>ग्राहकांना दिलेले सिलेंडर</span><span style="font-weight:700;color:var(--accent-green)" id="trip_delivered">0</span></div>
      <div style="margin:12px 0;font-size:12px;font-weight:700;color:var(--accent-blue)">💳 पैसे प्रकार</div>
      ${['Cash','QR Code','GPay','Paytm','Advance','Partial'].map((m,i)=>`<div class="trip-row" style="padding-left:16px"><span style="color:var(--text-secondary)">${m}</span><span id="trip_${['cash','qr','gpay','paytm','advance','partial'][i]}">0</span></div>`).join('')}
      <div class="trip-row" style="border-top:2px solid var(--border);margin-top:4px;padding-top:8px"><span style="font-weight:700">एकूण</span><span style="font-weight:700;color:var(--accent-yellow)" id="trip_total">0</span></div>
      <div style="margin:12px 0;font-size:12px;font-weight:700;color:var(--accent-orange)">📦 स्टॉक ट्रान्सफर</div>
      <table style="width:100%;font-size:12px"><tr><th>ठिकाण</th><th>भरलेले</th><th>रिकामे</th></tr>
        <tr><td>Office</td><td><input type="number" id="office_given" style="width:60px;padding:4px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);text-align:center"></td>
        <td><input type="number" id="office_taken" style="width:60px;padding:4px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);text-align:center"></td></tr>
      </table>
      <div style="font-size:15px;font-weight:700;color:var(--accent-yellow);margin:16px 0 12px">💵 नोट मोजणी</div>
      <table style="width:100%">
        ${[500,200,100,50,20,10].map(n=>`<tr><td style="width:80px;color:var(--accent-yellow);font-weight:700">₹${n}</td><td>×</td>
        <td><input type="number" id="d${n}" placeholder="0" oninput="calcDenom()" style="width:70px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);text-align:center"></td>
        <td>=</td><td><span id="dt${n}" style="color:var(--accent-green);font-weight:700">₹0</span></td></tr>`).join('')}
        <tr><td colspan="2" style="font-weight:700">Coins</td><td><input type="number" id="dcoins" placeholder="0" oninput="calcDenom()" style="width:70px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);text-align:center"></td></tr>
        <tr style="border-top:2px solid var(--border)"><td colspan="4" style="font-weight:700">एकूण</td><td><span id="denomTotal" style="color:var(--accent-yellow);font-weight:700">₹0</span></td></tr>
      </table>
      <div style="font-size:15px;font-weight:700;color:var(--accent-yellow);margin:16px 0 12px">🏪 BDA Cash</div>
      ${bdas.map(b=>`<div class="trip-row"><span>${b.area} — ${b.owner}</span><input type="number" placeholder="₹0" style="width:80px;padding:6px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:4px;color:var(--text-primary);text-align:center"></div>`).join('')}
    </div></div>
    <button class="btn btn-success" style="width:100%;font-size:16px;padding:14px" onclick="alert('✅ Trip closed!')">✅ ट्रिप बंद करा</button>`;
}

function buildGodown() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🏭 गोदाम / Godown Stock</div>
        <div class="page-header-sub">SAP Code: 187618 · BPCL Authorized Godown</div>
      </div>
      <button class="btn btn-warning btn-sm" onclick="showPage('bpcl')">📋 BPCL Verify</button>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'g-main')">🏭 मुख्य साठा / Main Stock</button>
      <button class="tab-btn" onclick="switchTab(this,'g-entry')">📥 Stock Entry</button>
      <button class="tab-btn" onclick="switchTab(this,'g-defective')">⚠️ खराब / Defective</button>
      <button class="tab-btn" onclick="switchTab(this,'g-accessories')">📦 Accessories</button>
      <button class="tab-btn" onclick="switchTab(this,'g-transfer')">🔄 Transfer</button>
    </div>
    
    <div class="tab-content active" id="g-main">
      <div class="section-title">🔵 14.2 kg Domestic Cylinder (5350 / 5370)</div>
      <div class="grid-4" style="margin-bottom:24px">
        <div class="stat-card">
          <div class="stat-icon">🟢</div>
          <div class="stat-label">FULL / भरलेले</div>
          <div class="stat-value" style="color:var(--accent-green)">801</div>
          <div class="stat-sub">BPCL Closing: 801</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⚪</div>
          <div class="stat-label">EMPTY / रिकामे</div>
          <div class="stat-value" style="color:var(--text-secondary)">429</div>
          <div class="stat-sub">BPCL: 338</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🚐</div>
          <div class="stat-label">VEHICLE STOCK</div>
          <div class="stat-value" style="color:var(--accent-purple)">390</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏪</div>
          <div class="stat-label">BDA FILLED</div>
          <div class="stat-value" style="color:var(--accent-orange)">21</div>
        </div>
      </div>
      
      <div class="section-title">🟡 5 kg Cylinder (5240 / 5250 / 5260)</div>
      <div class="grid-3" style="margin-bottom:24px">
        <div class="stat-card">
          <div class="stat-icon">🟡</div>
          <div class="stat-label">COMMERCIAL FULL (5240)</div>
          <div class="stat-value" style="color:var(--accent-yellow)">66</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🟡</div>
          <div class="stat-label">DOMESTIC FULL (5250)</div>
          <div class="stat-value" style="color:var(--accent-yellow)">20</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🟡</div>
          <div class="stat-label">COMMERCIAL (5260)</div>
          <div class="stat-value" style="color:var(--accent-yellow)">23</div>
        </div>
      </div>
      
      <div class="section-title">🔴 19 kg Commercial Cylinder (5400 / 5450)</div>
      <div class="grid-3" style="margin-bottom:24px">
        <div class="stat-card">
          <div class="stat-icon">🔴</div>
          <div class="stat-label">19 KG FULL (5400)</div>
          <div class="stat-value" style="color:var(--accent-orange)">64</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⚪</div>
          <div class="stat-label">19 KG EMPTY</div>
          <div class="stat-value" style="color:var(--text-secondary)">9</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✂️</div>
          <div class="stat-label">19 KG CUTTING (5450)</div>
          <div class="stat-value" style="color:var(--accent-red)">4</div>
        </div>
      </div>
      
      <div class="section-title">🔧 DPR — De-Pressure Regulator</div>
      <div class="grid-2">
        <div class="stat-card">
          <div class="stat-icon">🔧</div>
          <div class="stat-label">14.2 KG DPR (BPCDPR)</div>
          <div class="stat-value" style="color:var(--accent-blue)">338</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🔧</div>
          <div class="stat-label">5 KG DPR (BPCDPRF)</div>
          <div class="stat-value" style="color:var(--accent-blue)">62</div>
        </div>
      </div>
    </div>
    
    <div class="tab-content" id="g-entry">
      <div class="card">
        <div class="card-title">📥 स्टॉक एंट्री / Stock Entry (Morning Physical Count)</div>
        <div class="alert alert-warning">⚠️ सकाळी भौतिक मोजणी / Physical morning count — मागील दिवसाचा क्लोजिंग स्टॉकशी जुळले पाहिजे</div>
        <div class="form-row">
          <div class="form-group"><label>14.2 kg भरलेले / Full</label><input type="number" value="801"></div>
          <div class="form-group"><label>14.2 kg रिकामे / Empty</label><input type="number" value="429"></div>
          <div class="form-group"><label>5 kg Full</label><input type="number" value="109"></div>
          <div class="form-group"><label>19 kg Full</label><input type="number" value="64"></div>
        </div>
        <button class="btn btn-success">✅ Save Morning Stock</button>
      </div>
    </div>
    
    <div class="tab-content" id="g-defective">
      <div class="card">
        <div class="card-title">⚠️ खराब सिलेंडर / Defective Cylinders</div>
        <div class="grid-3" style="margin-bottom:16px">
          <div class="stat-card">
            <div class="stat-icon">⚠️</div>
            <div class="stat-label">14.2 kg Defective</div>
            <div class="stat-value" style="color:var(--accent-red)">0</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="tab-content" id="g-accessories">
      <div class="card"><p>Blue Book, Suraksha Pipe, DPR stock...</p></div>
    </div>
    
    <div class="tab-content" id="g-transfer">
      <div class="card"><p>Stock transfer records...</p></div>
    </div>
  `;
}

function buildOffice() {
  const deliveryMenStock = [
    {name:'Vishwas Bhore', filled:68, empty:40, cash:38500, online:3200},
    {name:'Mahesh Patil', filled:47, empty:0, cash:0, online:0},
    {name:'Harun Fakir', filled:31, empty:28, cash:28900, online:0},
    {name:'Vishal Magdum', filled:35, empty:15, cash:16200, online:1400}
  ];
  
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🏢 Office Summary / ऑफिस सारांश</div>
        <div class="page-header-sub">Wednesday, 18 February 2026</div>
      </div>
      <button class="btn btn-primary btn-sm">📤 Day End</button>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'office-sales')">💰 Sales/विक्री</button>
      <button class="tab-btn" onclick="switchTab(this,'office-stock')">📦 Stock/साठा</button>
      <button class="tab-btn" onclick="switchTab(this,'office-expenses')">💸 Expenses/खर्च</button>
      <button class="tab-btn" onclick="switchTab(this,'office-dayend')">📋 Day End</button>
      <button class="tab-btn" onclick="switchTab(this,'office-additional')">➕ Additional Sales</button>
    </div>
    
    <div class="tab-content active" id="office-sales">
      <div class="card">
        <div class="card-title">📊 Opening Stock / उघडणारा साठा</div>
        <div class="opening-stock-grid">
          <div class="opening-stock-box">
            <div class="opening-stock-value" style="color:var(--accent-green)">801</div>
            <div class="opening-stock-label">14.2 kg Full Opening</div>
          </div>
          <div class="opening-stock-box">
            <div class="opening-stock-value" style="color:var(--text-secondary)">429</div>
            <div class="opening-stock-label">14.2 kg Empty Opening</div>
          </div>
          <div class="opening-stock-box">
            <div class="opening-stock-value" style="color:var(--accent-yellow)">109</div>
            <div class="opening-stock-label">5 kg Full Opening</div>
          </div>
          <div class="opening-stock-box">
            <div class="opening-stock-value" style="color:var(--accent-orange)">64</div>
            <div class="opening-stock-label">19 kg Full Opening</div>
          </div>
        </div>
      </div>
      
      <div class="card">
        <div class="card-title">🛒 ग्राहकांना दिलेले / Refills to Customers</div>
        <table>
          <tr><td>Cash / रोख</td><td style="text-align:right"><strong>39 × ₹856 = ₹33,384</strong></td></tr>
          <tr><td>QR Code</td><td style="text-align:right"><strong>2 × ₹856 = ₹1,712</strong></td></tr>
          <tr><td>GPay</td><td style="text-align:right"><strong>2</strong></td></tr>
          <tr><td>Paytm</td><td style="text-align:right"><strong>0</strong></td></tr>
          <tr><td>Advance (BPCL)</td><td style="text-align:right"><strong>2</strong></td></tr>
          <tr><td>Partial Cash+Online</td><td style="text-align:right"><strong>1 (₹500 cash + ₹350 QR)</strong></td></tr>
          <tr style="border-top:2px solid var(--border)"><td><strong>एकूण / Total Refills</strong></td><td style="text-align:right"><strong style="color:var(--accent-yellow)">48</strong></td></tr>
        </table>
      </div>
      
      <div class="card">
        <div class="card-title">🔄 सिलेंडर हस्तांतरण / Stock Transfer Summary</div>
        <table>
          <thead>
            <tr>
              <th>डिलिव्हरी मॅन</th>
              <th style="text-align:center">भरलेले दिले</th>
              <th style="text-align:center">रिकामे घेतले</th>
              <th style="text-align:right">CASH</th>
              <th style="text-align:right">ONLINE</th>
            </tr>
          </thead>
          <tbody>
            ${deliveryMenStock.map(dm => `
              <tr>
                <td>${dm.name}</td>
                <td style="text-align:center;color:var(--accent-green)">${dm.filled}</td>
                <td style="text-align:center;color:var(--text-secondary)">${dm.empty}</td>
                <td style="text-align:right">₹${dm.cash.toLocaleString()}</td>
                <td style="text-align:right">₹${dm.online.toLocaleString()}</td>
              </tr>
            `).join('')}
            <tr style="border-top:2px solid var(--border);font-weight:700">
              <td>एकूण Total</td>
              <td style="text-align:center;color:var(--accent-green)">181</td>
              <td style="text-align:center;color:var(--text-secondary)">83</td>
              <td style="text-align:right">₹83,600</td>
              <td style="text-align:right">₹4,600</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="tab-content" id="office-stock">
      <div class="card"><p>Stock movements tracking...</p></div>
    </div>
    
    <div class="tab-content" id="office-expenses">
      <div class="card"><p>Daily expenses...</p></div>
    </div>
    
    <div class="tab-content" id="office-dayend">
      <div class="card"><p>Day end reconciliation...</p></div>
    </div>
    
    <div class="tab-content" id="office-additional">
      <div class="card"><p>SV, Suraksha Pipe, Blue Book sales...</p></div>
    </div>
  `;
}

function buildBpcl() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📋 BPCL Verification / BPCL पडताळणी</div>
        <div class="page-header-sub">SAP: 187618 · Day End: 15-Feb-2026</div>
      </div>
      <div style="display:flex;gap:8px">
        <label class="btn btn-primary btn-sm" style="cursor:pointer">📤 Day End PDF Upload<input type="file" accept=".pdf" style="display:none"></label>
        <label class="btn btn-success btn-sm" style="cursor:pointer">📊 SOA Excel Upload<input type="file" accept=".xls,.xlsx" style="display:none"></label>
      </div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'bpcl-dayend')">📋 Day End Report</button>
      <button class="tab-btn" onclick="switchTab(this,'bpcl-compare')">🔍 ERP vs BPCL</button>
      <button class="tab-btn" onclick="switchTab(this,'bpcl-soa')">📑 SOA (Jan 2026)</button>
      <button class="tab-btn" onclick="switchTab(this,'bpcl-codes')">🏷 Product Codes</button>
    </div>
    
    <div class="tab-content active" id="bpcl-dayend">
      <div class="card">
        <div class="card-header">
          <div class="card-title">📋 BPCL Day End — 15 Feb 2026</div>
          <div style="font-size:12px;color:var(--text-muted)">Distributor: 187618 | 07:45 PM</div>
        </div>
        
        <div style="font-weight:700;margin-bottom:12px">Transaction Summary</div>
        <table>
          <thead>
            <tr>
              <th>PRODUCT CODE</th>
              <th style="text-align:center">REFILLS</th>
              <th style="text-align:center">SV REFILLS</th>
              <th style="text-align:center">OPENING BOOKINGS</th>
              <th style="text-align:center">CURRENT BOOKINGS</th>
              <th style="text-align:center">CLOSING BOOKINGS</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>5350 + 5370</strong><br><span style="font-size:11px;color:var(--accent-yellow)">14.2 kg Domestic Cylinder</span><br><span style="font-size:10px;color:var(--text-muted)">(एकच उत्पादन — Full & Empty same product)</span></td>
              <td style="text-align:center;color:var(--accent-green);font-weight:700">89</td>
              <td style="text-align:center">0</td>
              <td style="text-align:center">634+148=782</td>
              <td style="text-align:center">94+8=102</td>
              <td style="text-align:center">639+156=795</td>
            </tr>
            <tr>
              <td>5300, 5400, 5450</td>
              <td colspan="5" style="text-align:center;color:var(--text-muted)">No transactions</td>
            </tr>
          </tbody>
        </table>
        
        <div style="font-weight:700;margin:20px 0 12px">Product-Wise Stock at Day-End</div>
        <table>
          <thead>
            <tr>
              <th>CODE</th>
              <th>PRODUCT</th>
              <th style="text-align:center">CLOSING FULL</th>
              <th style="text-align:center">CLOSING EMPTY</th>
              <th style="text-align:center">FULL DEFECTIVE</th>
              <th style="text-align:center">BDA FILLED</th>
              <th style="text-align:center">VEHICLE STOCK</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>5240</td><td>5 kg Commercial</td><td style="text-align:center">66</td><td style="text-align:center">0</td><td style="text-align:center">0</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
            <tr><td>5250</td><td>5 kg Domestic</td><td style="text-align:center">20</td><td style="text-align:center">0</td><td style="text-align:center">0</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
            <tr><td>5260</td><td>5 kg Commercial (alt)</td><td style="text-align:center">23</td><td style="text-align:center">0</td><td style="text-align:center">0</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
            <tr style="background:rgba(34,197,94,0.05)"><td><strong>5350+5370</strong></td><td><strong>14.2 kg Domestic</strong></td><td style="text-align:center;color:var(--accent-green);font-weight:700">801</td><td style="text-align:center">338</td><td style="text-align:center">0</td><td style="text-align:center">21</td><td style="text-align:center">390</td></tr>
            <tr><td>5400</td><td>19 kg Commercial</td><td style="text-align:center">64</td><td style="text-align:center">9</td><td style="text-align:center">0</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
            <tr><td>5450</td><td>19 kg Cutting</td><td style="text-align:center">4</td><td style="text-align:center">0</td><td style="text-align:center">0</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
            <tr><td>BPCDPR</td><td>14.2 kg DPR</td><td style="text-align:center">338</td><td style="text-align:center">0</td><td style="text-align:center">15</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
            <tr><td>BPCDPRF</td><td>5 kg DPR</td><td style="text-align:center">62</td><td style="text-align:center">0</td><td style="text-align:center">0</td><td style="text-align:center">—</td><td style="text-align:center">—</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="tab-content" id="bpcl-compare">
      <div class="card"><p>ERP vs BPCL comparison...</p></div>
    </div>
    
    <div class="tab-content" id="bpcl-soa">
      <div class="card"><p>Statement of Account...</p></div>
    </div>
    
    <div class="tab-content" id="bpcl-codes">
      <div class="card">
        <div class="card-title">🏷 BPCL Product Codes (for reference in system)</div>
        <table>
          <tr><th>Product Code</th><th>Day to Day plain name</th></tr>
          <tr><td>5240</td><td>5 kg commercial Cylinder</td></tr>
          <tr><td>5250</td><td>5 kg Domestic Cylinder</td></tr>
          <tr><td>5260</td><td>5 kg commercial Cylinder</td></tr>
          <tr><td><strong>5350</strong></td><td><strong>14.2 kg Domestic Cylinder (Full or Empty - same code)</strong></td></tr>
          <tr><td><strong>5370</strong></td><td><strong>14.2 kg Domestic Cylinder (Full or Empty - same code)</strong></td></tr>
          <tr><td>5400</td><td>19 kg commercial Cylinder</td></tr>
          <tr><td>5450</td><td>19 kg cutting Cylinder</td></tr>
          <tr><td>BPCDPR</td><td>14.2 kg DPR (De-pressure Regulator)</td></tr>
          <tr><td>BPCDPRF</td><td>5 kg DPR (De-pressure Regulator)</td></tr>
        </table>
      </div>
    </div>
  `;
}

function buildPayroll() {
  const deliveryMen = [
    {name:'Vishwas Bhore', urban:50, rural:0, pairDays:4, cashExpected:41200, cashGiven:40000, advanceTotal:20000, advanceDeduct:5000},
    {name:'Mahesh Patil', urban:47, rural:0, pairDays:0, cashExpected:40232, cashGiven:40000, advanceTotal:0, advanceDeduct:0},
    {name:'Harun Fakir', urban:31, rural:8, pairDays:2, cashExpected:28900, cashGiven:28900, advanceTotal:0, advanceDeduct:0},
    {name:'Vishal Magdum', urban:35, rural:5, pairDays:3, cashExpected:34500, cashGiven:32000, advanceTotal:5000, advanceDeduct:5000}
  ];
  
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">💰 Payroll / पगार व्यवस्थापन</div>
        <div class="page-header-sub">Wage calculation · Advances · Monthly settlement</div>
      </div>
      <button class="chip chip-yellow">👑 Owner — Approve Access</button>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'pay-delivery')">🚴 Delivery Men</button>
      <button class="tab-btn" onclick="switchTab(this,'pay-office')">🏢 Office Staff</button>
      <button class="tab-btn" onclick="switchTab(this,'pay-godown')">🏭 Godown Crew</button>
      <button class="tab-btn" onclick="switchTab(this,'pay-advances')">💳 Advances</button>
    </div>
    
    <div class="tab-content active" id="pay-delivery">
      <div class="alert alert-info" style="margin-bottom:16px">
        <strong>वेतन नियम / Wage Rules:</strong> Urban (Jaysingpur): ₹8/cylinder | Rural (Villages): ₹7/cylinder | Pair Bonus: ₹200/day | Cash Difference: deducted at once | Advance: ₹5000/month deduction
      </div>
      
      ${deliveryMen.map(dm => {
        const urbanWage = dm.urban * 8;
        const ruralWage = dm.rural * 7;
        const pairBonus = dm.pairDays * 200;
        const grossWage = urbanWage + ruralWage + pairBonus;
        const cashDiff = dm.cashExpected - dm.cashGiven;
        const netPayable = grossWage - cashDiff - dm.advanceDeduct;
        const remainingAdvance = dm.advanceTotal - dm.advanceDeduct;
        
        return `
        <div class="payroll-card">
          <div class="payroll-header">
            <div>
              <div class="payroll-name">👤 ${dm.name}</div>
            </div>
            <span class="payroll-role">Delivery Man</span>
          </div>
          
          <div class="payroll-grid">
            <div class="payroll-section">
              <div class="payroll-section-title">📊 Cylinder Sales (This Month)</div>
              <div class="payroll-row">
                <span>Urban (Jaysingpur) × ₹8</span>
                <span style="color:var(--accent-green)">${dm.urban} × ₹8 = <strong>₹${urbanWage}</strong></span>
              </div>
              <div class="payroll-row">
                <span>Rural (Villages) × ₹7</span>
                <span style="color:var(--accent-green)">${dm.rural} × ₹7 = <strong>₹${ruralWage}</strong></span>
              </div>
              <div class="payroll-row">
                <span>Pair Bonus (${dm.pairDays} days)</span>
                <span style="color:var(--accent-yellow)"><strong>₹${pairBonus}</strong></span>
              </div>
              <div class="payroll-row payroll-total">
                <span><strong>Gross Wage</strong></span>
                <span style="color:var(--accent-green)"><strong>₹${grossWage.toLocaleString()}</strong></span>
              </div>
            </div>
            
            <div class="payroll-section">
              <div class="payroll-section-title">📉 Deductions</div>
              <div class="payroll-row">
                <span>Cash Difference (₹${dm.cashExpected}-₹${dm.cashGiven})</span>
                <span style="color:var(--accent-red)"><strong>-₹${cashDiff.toLocaleString()}</strong></span>
              </div>
              <div class="payroll-row">
                <span>Advance Deduction</span>
                <span style="color:var(--accent-red)"><strong>-₹${dm.advanceDeduct.toLocaleString()}</strong></span>
              </div>
              <div class="payroll-row payroll-total">
                <span><strong>Net Payable / देय पगार</strong></span>
                <span style="color:${netPayable >= 0 ? 'var(--accent-yellow)' : 'var(--accent-red)'}"><strong>₹${netPayable.toLocaleString()}</strong></span>
              </div>
              <div class="payroll-row">
                <span>Remaining Advance</span>
                <span style="color:var(--accent-orange)"><strong>₹${remainingAdvance.toLocaleString()}</strong></span>
              </div>
            </div>
          </div>
          
          <div class="payroll-actions">
            <button class="btn btn-sm btn-warning">✏️ Edit</button>
            <button class="btn btn-sm btn-primary">💳 Add Cash Difference</button>
            <button class="btn btn-sm btn-success">✅ Approve & Pay</button>
          </div>
        </div>
        `;
      }).join('')}
    </div>
    
    <div class="tab-content" id="pay-office">
      <div class="card"><p>Office staff payroll coming soon...</p></div>
    </div>
    
    <div class="tab-content" id="pay-godown">
      <div class="card"><p>Godown crew payroll coming soon...</p></div>
    </div>
    
    <div class="tab-content" id="pay-advances">
      <div class="card"><p>Advances tracking coming soon...</p></div>
    </div>
  `;
}

function buildTracking() {
  const vehicles = [
    {name:'Vishwas Bhore', status:'On Route', location:'Shahunagar', icon:'🚐', time:'2 min ago'},
    {name:'Mahesh Patil', status:'At Godown', location:'Loading', icon:'🏍', time:'2 min ago'},
    {name:'Harun Fakir', status:'Returned', location:'Jambhali', icon:'🚐', time:'2 min ago'},
    {name:'Vishal Magdum', status:'On Route', location:'Patel Chouk', icon:'🏍', time:'2 min ago'}
  ];
  
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📍 Live Tracking / थेट ट्रॅकिंग</div>
        <div class="page-header-sub">All delivery vehicles — real-time location</div>
      </div>
      <span class="chip chip-green" style="animation: pulse 2s infinite">LIVE</span>
    </div>
    
    <div class="grid-2" style="margin-bottom:24px">
      ${vehicles.map(v => `
        <div class="vehicle-card">
          <div class="vehicle-icon">${v.icon}</div>
          <div class="vehicle-info">
            <div class="vehicle-name">${v.name}</div>
            <div class="vehicle-status" style="color:${v.status === 'On Route' ? 'var(--accent-green)' : v.status === 'Returned' ? 'var(--text-muted)' : 'var(--accent-yellow)'}">
              ${v.status}
            </div>
            <div class="vehicle-location">📍 ${v.location}</div>
            <div class="vehicle-update">Last update: ${v.time}</div>
          </div>
        </div>
      `).join('')}
    </div>
    
    <div class="card">
      <div class="card-title">🗺 Live Map — Jaysingpur & Rural Areas</div>
      <div style="border:2px dashed var(--border);border-radius:12px;padding:60px;text-align:center;background:rgba(255,255,255,0.02)">
        <div style="font-size:48px;margin-bottom:16px">🗺️</div>
        <div style="font-size:18px;font-weight:700;margin-bottom:8px">Live GPS Tracking Map</div>
        <div style="font-size:13px;color:var(--text-secondary);margin-bottom:4px">🚐 Delivery van icons on route</div>
        <div style="font-size:13px;color:var(--text-secondary);margin-bottom:4px">📍 Customer pin drops (known addresses)</div>
        <div style="font-size:13px;color:var(--text-secondary);margin-bottom:16px">🔵 Scheduled · 🟡 In Trip · 🟢 Delivered</div>
        <div class="alert alert-info" style="max-width:600px;margin:16px auto 0;text-align:left">
          Server required for live GPS. Connect to local WiFi or upgrade to internet server for real-time tracking.
        </div>
      </div>
    </div>
  `;
}

function buildStaff() {
  const staff = [{name:'Vishal Patil',role:'Owner',mobile:'7887456789'},{name:'Vishwas Bhore',role:'Delivery',mobile:'7643982982'}];
  return `<div class="page-header"><div><div class="page-header-title">👥 Staff Management</div></div></div>
    <div class="card"><table><thead><tr><th>Name</th><th>Role</th><th>Mobile</th></tr></thead><tbody>
    ${staff.map(s=>`<tr><td>${s.name}</td><td>${s.role}</td><td>${s.mobile}</td></tr>`).join('')}</tbody></table></div>`;
}

function buildNotices() {
  return `<div class="page-header"><div><div class="page-header-title">📢 Notices / सूचना</div></div><button class="btn btn-success btn-sm">+ New Notice</button></div>
    <div class="card"><div style="padding:16px;border-left:4px solid var(--accent-blue);background:rgba(59,130,246,0.1);border-radius:8px">
    <div style="font-weight:700;margin-bottom:8px">🔴 URGENT: Price Update</div><p style="font-size:13px">14.2 kg = ₹856 effective today</p></div></div>`;
}

async function loadDeliveries() {
  const res = await fetch('api.php?action=get_deliveries');
  const data = await res.json();
  if (data.success) {
    deliveries = data.data.deliveries;
    allAreas = [...new Set(deliveries.map(d => d.area))].sort();
    const areaSelect = document.getElementById('areaFilter');
    if (areaSelect) areaSelect.innerHTML = '<option value="">All Areas</option>' + allAreas.map(a => `<option value="${a}">${a}</option>`).join('');
    renderDeliveries(deliveries);
    updateDashboardStats();
    updateTripSummary();
  }
}

function filterDeliveries() {
  const search = (document.getElementById('delivSearch')?.value || '').toLowerCase();
  const area = document.getElementById('areaFilter')?.value || '';
  const status = document.getElementById('statusFilter')?.value || '';
  const filtered = deliveries.filter(d =>
    (!search || d.consumer_name.toLowerCase().includes(search) || d.mobile.includes(search) || d.area.toLowerCase().includes(search)) &&
    (!area || d.area === area) && (!status || d.status === status)
  );
  renderDeliveries(filtered);
}

function renderDeliveries(list) {
  const byArea = {};
  list.forEach(d => { if (!byArea[d.area]) byArea[d.area] = []; byArea[d.area].push(d); });
  const html = Object.entries(byArea).map(([area, items]) => `
    <div style="margin-bottom:16px">
      <div style="font-size:13px;font-weight:700;color:var(--accent-yellow);margin-bottom:8px">📍 ${area} <span style="font-size:11px;font-weight:400;color:var(--text-muted)">(${items.length})</span></div>
      ${items.map(d => renderDeliveryCard(d)).join('')}
    </div>
  `).join('');
  const el = document.getElementById('deliveryList');
  if (el) el.innerHTML = html || '<div class="card"><p style="text-align:center;padding:40px">No deliveries</p></div>';
}

function renderDeliveryCard(d) {
  const sc = {scheduled: '#3b82f6', intrip: '#eab308', delivered: '#22c55e', emergency: '#f97316', notdelivered: '#ef4444'};
  const sd = {scheduled: 'status-scheduled', intrip: 'status-intrip', delivered: 'status-delivered', emergency: 'status-emergency', notdelivered: 'status-notdelivered'};
  const sl = {scheduled: 'शेड्युल्ड', intrip: 'रस्त्यावर', delivered: 'डिलिव्हर (OTP)', emergency: 'आपत्कालीन', notdelivered: 'डिलिव्हर नाही'};
  const cc = {scheduled: 'chip-blue', intrip: 'chip-yellow', delivered: 'chip-green', emergency: 'chip-orange', notdelivered: 'chip-red'};
  return `<div class="delivery-card"><div class="status-bar" style="background:${sc[d.status]}"></div><div class="dcnum">${d.sl_no}</div>
    <div class="dcinfo"><div class="dcname">${d.consumer_name}</div><div class="dcaddress">📍 ${d.address}</div><div class="dcarea">🗂️ ${d.area} | 📄 ${d.cash_memo} | 👤 ${d.operator_name}</div></div>
    <div class="dcactions"><span class="chip ${cc[d.status]}"><span class="status-dot ${sd[d.status]}"></span> ${sl[d.status]}</span><div class="dcphone">📞 ${d.mobile}</div>
    ${d.otp?`<div style="font-size:11px;color:var(--accent-green);margin-top:4px">OTP: ${d.otp}</div>`:''}
    ${d.payment_mode?`<div style="font-size:11px;color:var(--accent-blue);margin-top:2px">💳 ${d.payment_mode}</div>`:''}</div></div>`;
}

async function handleCSVUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const form = new FormData();
  form.append('csv_file', file);
  form.append('action', 'upload_csv');
  const res = await fetch('api.php', { method: 'POST', body: form });
  const data = await res.json();
  if (data.success) { alert(data.message); loadDeliveries(); }
  else alert('Upload failed: ' + data.message);
}

function updateDashboardStats() {
  const s = {
    delivered: deliveries.filter(d => d.status === 'delivered' || d.status === 'emergency').length,
    intrip: deliveries.filter(d => d.status === 'intrip').length,
    scheduled: deliveries.filter(d => d.status === 'scheduled').length,
    notdelivered: deliveries.filter(d => d.status === 'notdelivered').length
  };
  if (document.getElementById('stat-delivered')) {
    document.getElementById('stat-delivered').textContent = s.delivered;
    document.getElementById('stat-intrip').textContent = s.intrip;
    document.getElementById('stat-scheduled').textContent = s.scheduled;
    document.getElementById('stat-notdelivered').textContent = s.notdelivered;
  }
}

function updateTripSummary() {
  const delivered = deliveries.filter(d => d.status === 'delivered' || d.status === 'emergency');
  const p = {Cash:0, 'QR Code':0, GPay:0, Paytm:0, 'Advance (BPCL)':0, 'Partial':0};
  delivered.forEach(d => { if (d.payment_mode && p[d.payment_mode] !== undefined) p[d.payment_mode]++; });
  if (document.getElementById('trip_delivered')) {
    document.getElementById('trip_delivered').textContent = delivered.length;
    document.getElementById('trip_cash').textContent = p.Cash || 0;
    document.getElementById('trip_qr').textContent = p['QR Code'] || 0;
    document.getElementById('trip_gpay').textContent = p.GPay || 0;
    document.getElementById('trip_paytm').textContent = p.Paytm || 0;
    document.getElementById('trip_advance').textContent = p['Advance (BPCL)'] || 0;
    document.getElementById('trip_partial').textContent = p.Partial || 0;
    document.getElementById('trip_total').textContent = delivered.length;
  }
}

function calcGodownGrid() {
  const fr = parseFloat(document.getElementById('full_r')?.value) || 0;
  const fc = parseFloat(document.getElementById('full_c')?.value) || 0;
  const fe = parseFloat(document.getElementById('full_e')?.value) || 0;
  const fullTotal = fr * fc + fe;
  const ftEl = document.getElementById('full_total');
  if (ftEl) ftEl.textContent = fullTotal || '—';
  let emptyGrandTotal = 0;
  ['e1','e2','e3'].forEach(prefix => {
    const r = parseFloat(document.getElementById(prefix+'_r')?.value) || 0;
    const c = parseFloat(document.getElementById(prefix+'_c')?.value) || 0;
    const a = parseFloat(document.getElementById(prefix+'_a')?.value) || 0;
    const s = parseFloat(document.getElementById(prefix+'_s')?.value) || 0;
    const sectionTotal = (r * c + a) * 2 + s;
    const el = document.getElementById(prefix+'_total');
    if (el) el.textContent = sectionTotal || '—';
    emptyGrandTotal += sectionTotal;
  });
  const etEl = document.getElementById('empty_total');
  if (etEl) etEl.textContent = emptyGrandTotal || '—';
}

function calcDenom() {
  let total = 0;
  [500,200,100,50,20,10].forEach(n => {
    const qty = parseFloat(document.getElementById('d'+n)?.value) || 0;
    const amt = qty * n;
    const el = document.getElementById('dt'+n);
    if (el) el.textContent = '₹' + amt;
    total += amt;
  });
  const coins = parseFloat(document.getElementById('dcoins')?.value) || 0;
  total += coins;
  const totalEl = document.getElementById('denomTotal');
  if (totalEl) totalEl.textContent = '₹' + total;
}
</script>
</body>
</html>
