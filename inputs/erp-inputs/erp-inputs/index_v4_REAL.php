<?php
session_start();
require_once 'config.php';

// Get current user
function getCurrentUser() {
    if (!isset($_SESSION['user_id'])) return null;
    global $conn;
    $stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->bind_param("i", $_SESSION['user_id']);
    $stmt->execute();
    return $stmt->get_result()->fetch_assoc();
}

$currentUser = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shourya Bharatgas ERP v4 - Real System</title>
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
.login-field input:focus, .login-field select:focus {
  outline: none; border-color: var(--accent-blue); box-shadow: 0 0 20px rgba(74,144,226,0.3);
}
.btn-login {
  width: 100%; background: linear-gradient(135deg, var(--accent-blue), var(--bpcl-blue));
  color: white; border: none; border-radius: 8px; padding: 14px; font-size: 16px; font-weight: 700; cursor: pointer;
  font-family: var(--font-main);
}

#app { display: none; }
.topnav {
  background: white; border-bottom: 1px solid #e5e7eb; padding: 12px 24px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.topnav-row { display: flex; justify-content: space-between; align-items: center; width: 100%; }
.topnav-logo { display: flex; align-items: center; gap: 12px; }
.logo-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow));
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
  font-size: 24px;
}
.logo-text { font-size: 18px; font-weight: 700; color: var(--bpcl-blue); }
.logo-sub { font-size: 11px; color: #6b7280; }
.topnav-center { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
.nav-btn {
  padding: 10px 20px; background: white;
  border: 1px solid #d1d5db; border-radius: 20px;
  color: #374151; font-weight: 600; cursor: pointer; font-family: var(--font-main);
  transition: all 0.2s; font-size: 14px;
}
.nav-btn:hover { background: #f3f4f6; border-color: #9ca3af; }
.nav-btn.active { background: #dbeafe; border-color: #3b82f6; color: #1e40af; }
.user-badge { display: flex; align-items: center; gap: 10px; }
.user-avatar {
  width: 40px; height: 40px; border-radius: 10px; background: var(--accent-blue);
  color: white; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px;
}
.btn-logout {
  padding: 8px 16px; background: rgba(239,68,68,0.15);
  border: 1px solid rgba(239,68,68,0.3); border-radius: 8px;
  color: var(--accent-red); font-weight: 600; cursor: pointer; font-family: var(--font-main);
}

.content { padding: 24px; max-width: 1600px; margin: 0 auto; }

.page-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border); flex-wrap: wrap; gap: 16px;
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

.search-bar { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.search-input {
  flex: 1; min-width: 250px; background: rgba(255,255,255,0.05);
  border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px;
  color: var(--text-primary); font-size: 15px; font-family: var(--font-main);
}

.btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; font-family: var(--font-main); }
.btn-primary { background: var(--accent-blue); color: white; }
.btn-success { background: var(--accent-green); color: white; }
.btn-warning { background: var(--accent-yellow); color: var(--bg-dark); }
.btn-danger { background: var(--accent-red); color: white; }
.btn-sm { padding: 6px 12px; font-size: 13px; }

.stat-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px; text-align: center;
}
.stat-value { font-size: 48px; font-weight: 700; color: var(--accent-yellow); margin: 8px 0; }
.stat-label { font-size: 13px; color: var(--text-secondary); margin-top: 8px; }
.stat-sub { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.stat-icon { font-size: 40px; margin-bottom: 12px; }

.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 600; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 14px; color: var(--text-primary); font-family: var(--font-main);
}
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }

.tabs {
  display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;
  border-bottom: 2px solid var(--border);
}
.tab-btn {
  padding: 12px 20px; background: rgba(255,255,255,0.03);
  border: none; border-bottom: 3px solid transparent;
  color: var(--text-secondary); font-weight: 600; cursor: pointer;
  border-radius: 8px 8px 0 0; font-family: var(--font-main);
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

.payroll-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; margin-bottom: 16px;
}
.payroll-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border);
}
.payroll-name { font-size: 18px; font-weight: 700; color: var(--text-primary); }
.payroll-role { font-size: 12px; color: var(--text-secondary); padding: 4px 10px; background: rgba(74,144,226,0.15); border-radius: 12px; }
.payroll-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 16px; }
.payroll-section-title { font-size: 13px; font-weight: 700; color: var(--accent-blue); margin-bottom: 12px; }
.payroll-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; }
.payroll-total { border-top: 2px solid var(--border); padding-top: 12px; margin-top: 12px; }
.payroll-total .payroll-row { font-size: 16px; font-weight: 700; }
.payroll-actions { display: flex; gap: 8px; flex-wrap: wrap; }

.opening-stock-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }
.opening-stock-box {
  background: var(--bg-card2); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; text-align: center;
}
.opening-stock-value { font-size: 48px; font-weight: 700; margin: 8px 0; }
.opening-stock-label { font-size: 12px; color: var(--text-secondary); }

.vehicle-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 16px; display: flex; align-items: center; gap: 16px;
}
.vehicle-icon { font-size: 32px; }
.vehicle-info { flex: 1; }
.vehicle-name { font-size: 16px; font-weight: 700; color: var(--text-primary); }
.vehicle-status { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.vehicle-location { font-size: 12px; color: var(--accent-blue); margin-top: 4px; }
.vehicle-update { font-size: 11px; color: var(--text-muted); margin-top: 4px; }

.empty-state {
  text-align: center; padding: 60px 20px; color: var(--text-muted);
}
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
        <input type="password" name="password" required placeholder="Default: 1234">
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
let godownStock = {full14: 0, empty14: 0, full5: 0, full19: 0};
let officeStock = {full14: 0, empty14: 0, full5: 0, full19: 0};

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
  const container = parent.nextElementSibling;
  if (!container) return;
  let found = false;
  let current = container;
  while(current && !found) {
    current.querySelectorAll('.tab-content').forEach(t => {
      t.classList.remove('active');
      if (t.id === tabId) {
        t.classList.add('active');
        found = true;
      }
    });
    if (!found) current = current.nextElementSibling;
  }
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
    case 'tracking': return buildTracking();
    case 'staff': return buildStaff();
    case 'notices': return buildNotices();
    default: return '<div class="card"><p>Loading...</p></div>';
  }
}

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
        <button class="btn btn-warning btn-sm" onclick="showPage('trip')">📦 Stock Transfer</button>
      </div>
    </div>
    
    ${deliveries.length > 0 ? `
      <div class="search-bar">
        <input type="text" class="search-input" placeholder="🔍 ग्राहक शोधा / Search customer, area, mobile..." oninput="filterDeliveries()">
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
      
      <div class="section-title">⚪ 14.2 KG रिकामे (EMPTY) — 3 विभाग</div>
      <div style="background:rgba(148,163,184,0.05);padding:16px;border-radius:8px;margin-bottom:20px">
        <div style="margin-bottom:12px;font-size:11px;color:var(--text-secondary)">प्रत्येक विभाग: (दुहेरी उभी × दुहेरी आडवी + दुहेरी अधिक) × 2 + एकेरी अधिक = एकूण</div>
        
        <div style="margin-bottom:16px;padding:12px;background:rgba(255,255,255,0.02);border-radius:8px">
          <div style="font-weight:700;margin-bottom:8px">📍 फुडून उजवीकडे (Front Right)</div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:13px">
            <input type="number" id="e1_r" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>×</span>
            <input type="number" id="e1_c" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>+</span>
            <input type="number" id="e1_a" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>)×2+</span>
            <input type="number" id="e1_s" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>=</span>
            <span style="font-weight:700" id="e1Total">0</span>
          </div>
        </div>
        
        <div style="margin-bottom:16px;padding:12px;background:rgba(255,255,255,0.02);border-radius:8px">
          <div style="font-weight:700;margin-bottom:8px">📍 दरवाज्याच्या उजवीकडे (Door Right)</div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:13px">
            <input type="number" id="e2_r" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>×</span>
            <input type="number" id="e2_c" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>+</span>
            <input type="number" id="e2_a" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>)×2+</span>
            <input type="number" id="e2_s" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>=</span>
            <span style="font-weight:700" id="e2Total">0</span>
          </div>
        </div>
        
        <div style="margin-bottom:16px;padding:12px;background:rgba(255,255,255,0.02);border-radius:8px">
          <div style="font-weight:700;margin-bottom:8px">📍 दरवाज्याच्या डावीकडे (Door Left)</div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:13px">
            <input type="number" id="e3_r" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>×</span>
            <input type="number" id="e3_c" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>+</span>
            <input type="number" id="e3_a" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>)×2+</span>
            <input type="number" id="e3_s" value="0" oninput="calcGodownGrid()" style="width:60px;text-align:center">
            <span>=</span>
            <span style="font-weight:700" id="e3Total">0</span>
          </div>
        </div>
        
        <div style="padding:12px;background:rgba(34,197,94,0.1);border-radius:8px;text-align:center">
          <div style="font-size:12px;margin-bottom:4px">एकूण रिकामे / Total Empty</div>
          <div style="font-size:36px;font-weight:700;color:var(--accent-green)" id="emptyTotal">0</div>
        </div>
      </div>
      
      <div class="section-title">🟡 5 kg सिलेंडर</div>
      <div class="form-row" style="margin-bottom:20px">
        <div class="form-group">
          <label>भरलेले Full</label>
          <input type="number" id="full5" value="0">
        </div>
        <div class="form-group">
          <label>रिकामे Empty</label>
          <input type="number" id="empty5" value="0">
        </div>
      </div>
      
      <div class="form-group">
        <label>शेरा / REMARK — काही वेगळे असल्यास लिहा / ANY MISMATCH OR NOTES</label>
        <textarea rows="2" placeholder="काही वेगळे असल्यास लिहा... Any mismatch or notes"></textarea>
      </div>
      
      <button class="btn btn-success" onclick="saveMorningCount()">✅ सकाळचा साठा जतन करा / Save Morning Count</button>
    </div>
    
    <div class="card">
      <div class="card-header">
        <div class="card-title">📋 ट्रिप सारांश / Trip Summary</div>
        <button class="btn btn-primary btn-sm">+ नवीन ट्रिप / New Trip</button>
      </div>
      
      <div style="margin-bottom:20px">
        <div style="font-weight:700;margin-bottom:12px">ग्राहकांना दिलेले सिलेंडर / Refills Delivered</div>
        <div style="font-size:32px;font-weight:700;color:var(--accent-green)" id="tripDelivered">0</div>
      </div>
      
      <div style="margin-bottom:20px">
        <div style="font-weight:700;margin-bottom:12px">💳 पैसे प्रकार / Payment Breakdown</div>
        <table id="tripPayments">
          <tr><td>रोख / Cash</td><td style="text-align:right" id="trip_cash">0</td></tr>
          <tr><td>QR Code</td><td style="text-align:right" id="trip_qr">0</td></tr>
          <tr><td>GPay</td><td style="text-align:right" id="trip_gpay">0</td></tr>
          <tr><td>Paytm</td><td style="text-align:right" id="trip_paytm">0</td></tr>
          <tr><td>Advance (BPCL)</td><td style="text-align:right" id="trip_advance">0</td></tr>
          <tr><td>Partial (Cash+Online)</td><td style="text-align:right" id="trip_partial">0</td></tr>
          <tr style="font-weight:700;border-top:2px solid var(--border)"><td>एकूण / Total</td><td style="text-align:right" id="trip_total">0</td></tr>
        </table>
      </div>
      
      <div style="margin-bottom:20px">
        <div style="font-weight:700;margin-bottom:12px">📦 सिलेंडर हस्तांतरण / Stock Transfer</div>
        <table>
          <thead><tr><th>ठिकाण</th><th style="text-align:center">भरलेले दिले</th><th style="text-align:center">रिकामे घेतले</th></tr></thead>
          <tbody>
            <tr><td>ऑफिस / Office</td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td></tr>
            <tr><td>BDA - Kondigre</td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td></tr>
            <tr><td>BDA - Nimshirgav (Kumar)</td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td></tr>
            <tr><td>BDA - Nimshirgav (Lakhane)</td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td></tr>
            <tr><td>BDA - Danoli</td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td><td style="text-align:center"><input type="number" value="0" style="width:80px"></td></tr>
          </tbody>
        </table>
        <div style="margin-top:12px;text-align:right">
          <strong>एकूण रिकामे गोदाम जमा:</strong> <span style="font-size:20px;color:var(--accent-green)">0</span>
        </div>
      </div>
      
      <div style="margin-bottom:20px">
        <div style="font-weight:700;margin-bottom:12px">💵 नोट मोजणी / Cash Denomination Count</div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--accent-yellow)">₹500</span>
            <span>×</span>
            <input type="number" id="d500" value="0" oninput="calcDenom()" style="width:60px">
            <span>=</span>
            <span id="d500v">₹0</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--accent-yellow)">₹200</span>
            <span>×</span>
            <input type="number" id="d200" value="0" oninput="calcDenom()" style="width:60px">
            <span>=</span>
            <span id="d200v">₹0</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--accent-yellow)">₹100</span>
            <span>×</span>
            <input type="number" id="d100" value="0" oninput="calcDenom()" style="width:60px">
            <span>=</span>
            <span id="d100v">₹0</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--accent-yellow)">₹50</span>
            <span>×</span>
            <input type="number" id="d50" value="0" oninput="calcDenom()" style="width:60px">
            <span>=</span>
            <span id="d50v">₹0</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--accent-yellow)">₹20</span>
            <span>×</span>
            <input type="number" id="d20" value="0" oninput="calcDenom()" style="width:60px">
            <span>=</span>
            <span id="d20v">₹0</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--accent-yellow)">₹10</span>
            <span>×</span>
            <input type="number" id="d10" value="0" oninput="calcDenom()" style="width:60px">
            <span>=</span>
            <span id="d10v">₹0</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span>Coins</span>
            <input type="number" id="coins" value="0" oninput="calcDenom()" style="width:60px">
          </div>
        </div>
        <div style="margin-top:16px;padding:12px;background:rgba(255,209,0,0.1);border-radius:8px;text-align:center">
          <strong>एकूण Total</strong>
          <div style="font-size:28px;font-weight:700;color:var(--accent-yellow)" id="denomTotal">₹0</div>
        </div>
        <div class="alert alert-warning" style="margin-top:12px">
          ⚠️ एकूण नोट मोजणी = एकूण रोख जमा होणे आवश्यक
        </div>
      </div>
      
      <div style="margin-bottom:20px">
        <div style="font-weight:700;margin-bottom:12px">🏪 BDA कडून मिळालेले / Cash from BDA</div>
        <div class="form-row">
          <div class="form-group"><label>Kondigre — Sarika Waghmode</label><input type="number" value="0"></div>
          <div class="form-group"><label>Nimshirgav — Kumar Thomake</label><input type="number" value="0"></div>
          <div class="form-group"><label>Nimshirgav — Lakhane</label><input type="number" value="0"></div>
          <div class="form-group"><label>Danoli — Manoj</label><input type="number" value="0"></div>
        </div>
      </div>
      
      <button class="btn btn-success">✅ ट्रिप बंद करा / Close Trip</button>
    </div>
  `;
}

function calcGodownGrid() {
  const fr = parseInt(document.getElementById('full_r')?.value || 0);
  const fc = parseInt(document.getElementById('full_c')?.value || 0);
  const fe = parseInt(document.getElementById('full_e')?.value || 0);
  const fullTotal = (fr * fc) + fe;
  document.getElementById('fullTotal').textContent = fullTotal;
  
  const e1r = parseInt(document.getElementById('e1_r')?.value || 0);
  const e1c = parseInt(document.getElementById('e1_c')?.value || 0);
  const e1a = parseInt(document.getElementById('e1_a')?.value || 0);
  const e1s = parseInt(document.getElementById('e1_s')?.value || 0);
  const e1Total = ((e1r * e1c + e1a) * 2) + e1s;
  document.getElementById('e1Total').textContent = e1Total;
  
  const e2r = parseInt(document.getElementById('e2_r')?.value || 0);
  const e2c = parseInt(document.getElementById('e2_c')?.value || 0);
  const e2a = parseInt(document.getElementById('e2_a')?.value || 0);
  const e2s = parseInt(document.getElementById('e2_s')?.value || 0);
  const e2Total = ((e2r * e2c + e2a) * 2) + e2s;
  document.getElementById('e2Total').textContent = e2Total;
  
  const e3r = parseInt(document.getElementById('e3_r')?.value || 0);
  const e3c = parseInt(document.getElementById('e3_c')?.value || 0);
  const e3a = parseInt(document.getElementById('e3_a')?.value || 0);
  const e3s = parseInt(document.getElementById('e3_s')?.value || 0);
  const e3Total = ((e3r * e3c + e3a) * 2) + e3s;
  document.getElementById('e3Total').textContent = e3Total;
  
  const emptyTotal = e1Total + e2Total + e3Total;
  document.getElementById('emptyTotal').textContent = emptyTotal;
}

function calcDenom() {
  const d500 = parseInt(document.getElementById('d500')?.value || 0) * 500;
  const d200 = parseInt(document.getElementById('d200')?.value || 0) * 200;
  const d100 = parseInt(document.getElementById('d100')?.value || 0) * 100;
  const d50 = parseInt(document.getElementById('d50')?.value || 0) * 50;
  const d20 = parseInt(document.getElementById('d20')?.value || 0) * 20;
  const d10 = parseInt(document.getElementById('d10')?.value || 0) * 10;
  const coins = parseInt(document.getElementById('coins')?.value || 0);
  
  document.getElementById('d500v').textContent = '₹' + d500;
  document.getElementById('d200v').textContent = '₹' + d200;
  document.getElementById('d100v').textContent = '₹' + d100;
  document.getElementById('d50v').textContent = '₹' + d50;
  document.getElementById('d20v').textContent = '₹' + d20;
  document.getElementById('d10v').textContent = '₹' + d10;
  
  const total = d500 + d200 + d100 + d50 + d20 + d10 + coins;
  document.getElementById('denomTotal').textContent = '₹' + total.toLocaleString();
}

function saveMorningCount() {
  const fullTotal = document.getElementById('fullTotal').textContent;
  const emptyTotal = document.getElementById('emptyTotal').textContent;
  godownStock.full14 = parseInt(fullTotal);
  godownStock.empty14 = parseInt(emptyTotal);
  godownStock.full5 = parseInt(document.getElementById('full5')?.value || 0);
  alert('Morning stock count saved! Full: ' + fullTotal + ', Empty: ' + emptyTotal);
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
    
    <div>
      <div class="tab-content active" id="g-main">
        <div class="section-title">🔵 14.2 kg Domestic Cylinder (5350 / 5370)</div>
        <div class="grid-4" style="margin-bottom:24px">
          <div class="stat-card">
            <div class="stat-icon">🟢</div>
            <div class="stat-label">FULL / भरलेले</div>
            <div class="stat-value" style="color:var(--accent-green)">${godownStock.full14}</div>
            <div class="stat-sub">From morning count</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⚪</div>
            <div class="stat-label">EMPTY / रिकामे</div>
            <div class="stat-value" style="color:var(--text-secondary)">${godownStock.empty14}</div>
            <div class="stat-sub">From morning count</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🚐</div>
            <div class="stat-label">VEHICLE STOCK</div>
            <div class="stat-value" style="color:var(--accent-purple)">0</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏪</div>
            <div class="stat-label">BDA FILLED</div>
            <div class="stat-value" style="color:var(--accent-orange)">0</div>
          </div>
        </div>
        
        <div class="section-title">🟡 5 kg Cylinder (5240 / 5250 / 5260)</div>
        <div class="grid-3" style="margin-bottom:24px">
          <div class="stat-card">
            <div class="stat-icon">🟡</div>
            <div class="stat-label">TOTAL FULL</div>
            <div class="stat-value" style="color:var(--accent-yellow)">${godownStock.full5}</div>
          </div>
        </div>
        
        <div class="section-title">🔴 19 kg Commercial Cylinder (5400 / 5450)</div>
        <div class="grid-3">
          <div class="stat-card">
            <div class="stat-icon">🔴</div>
            <div class="stat-label">TOTAL FULL</div>
            <div class="stat-value" style="color:var(--accent-orange)">${godownStock.full19 || 0}</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="g-entry">
        <div class="card">
          <div class="card-title">📥 स्टॉक एंट्री / Stock Entry</div>
          <div class="alert alert-warning">⚠️ Go to Trip page to enter morning stock count</div>
        </div>
      </div>
      
      <div class="tab-content" id="g-defective">
        <div class="card">
          <div class="card-title">⚠️ खराब सिलेंडर / Defective Cylinders</div>
          <div class="empty-state">
            <div class="empty-state-icon">⚠️</div>
            <div class="empty-state-text">No defective cylinders recorded</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="g-accessories">
        <div class="card">
          <div class="card-title">📦 Accessories Inventory</div>
          <div class="empty-state">
            <div class="empty-state-icon">📦</div>
            <div class="empty-state-text">Blue Book, Suraksha Pipe, DPR tracking coming soon</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="g-transfer">
        <div class="card">
          <div class="card-title">🔄 Stock Transfer Records</div>
          <div class="empty-state">
            <div class="empty-state-icon">🔄</div>
            <div class="empty-state-text">No transfers recorded yet</div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function buildOffice() {
  const deliveredToday = deliveries.filter(d => d.status === 'delivered' || d.status === 'emergency');
  const cashCount = deliveredToday.filter(d => d.payment_mode === 'cash').length;
  const qrCount = deliveredToday.filter(d => d.payment_mode === 'qr').length;
  const gpayCount = deliveredToday.filter(d => d.payment_mode === 'gpay').length;
  const paytmCount = deliveredToday.filter(d => d.payment_mode === 'paytm').length;
  const advanceCount = deliveredToday.filter(d => d.payment_mode === 'advance').length;
  const partialCount = deliveredToday.filter(d => d.payment_mode === 'partial').length;
  
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🏢 Office Summary / ऑफिस सारांश</div>
        <div class="page-header-sub">${new Date().toLocaleDateString('en-GB')}</div>
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
    
    <div>
      <div class="tab-content active" id="office-sales">
        <div class="card">
          <div class="card-title">📊 Opening Stock / उघडणारा साठा</div>
          <div class="opening-stock-grid">
            <div class="opening-stock-box">
              <div class="opening-stock-value" style="color:var(--accent-green)">${officeStock.full14}</div>
              <div class="opening-stock-label">14.2 kg Full Opening</div>
            </div>
            <div class="opening-stock-box">
              <div class="opening-stock-value" style="color:var(--text-secondary)">${officeStock.empty14}</div>
              <div class="opening-stock-label">14.2 kg Empty Opening</div>
            </div>
            <div class="opening-stock-box">
              <div class="opening-stock-value" style="color:var(--accent-yellow)">${officeStock.full5}</div>
              <div class="opening-stock-label">5 kg Full Opening</div>
            </div>
            <div class="opening-stock-box">
              <div class="opening-stock-value" style="color:var(--accent-orange)">${officeStock.full19}</div>
              <div class="opening-stock-label">19 kg Full Opening</div>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="card-title">🛒 ग्राहकांना दिलेले / Refills to Customers</div>
          <table>
            <tr><td>Cash / रोख</td><td style="text-align:right"><strong>${cashCount} × ₹856 = ₹${(cashCount * 856).toLocaleString()}</strong></td></tr>
            <tr><td>QR Code</td><td style="text-align:right"><strong>${qrCount} × ₹856 = ₹${(qrCount * 856).toLocaleString()}</strong></td></tr>
            <tr><td>GPay</td><td style="text-align:right"><strong>${gpayCount}</strong></td></tr>
            <tr><td>Paytm</td><td style="text-align:right"><strong>${paytmCount}</strong></td></tr>
            <tr><td>Advance (BPCL)</td><td style="text-align:right"><strong>${advanceCount}</strong></td></tr>
            <tr><td>Partial Cash+Online</td><td style="text-align:right"><strong>${partialCount}</strong></td></tr>
            <tr style="border-top:2px solid var(--border)"><td><strong>एकूण / Total Refills</strong></td><td style="text-align:right"><strong style="color:var(--accent-yellow)">${deliveredToday.length}</strong></td></tr>
          </table>
        </div>
        
        <div class="card">
          <div class="card-title">🔄 Stock Transfer Summary</div>
          <div class="empty-state">
            <div class="empty-state-icon">🔄</div>
            <div class="empty-state-text">No stock transfers recorded today</div>
            <div class="empty-state-sub">Transfer data will appear after delivery men close trips</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="office-stock">
        <div class="card">
          <div class="card-title">📦 Office Stock</div>
          <div class="grid-4">
            <div class="stat-card">
              <div class="stat-value" style="color:var(--accent-green)">${officeStock.full14}</div>
              <div class="stat-label">14.2 kg Full</div>
            </div>
            <div class="stat-card">
              <div class="stat-value" style="color:var(--text-secondary)">${officeStock.empty14}</div>
              <div class="stat-label">14.2 kg Empty</div>
            </div>
            <div class="stat-card">
              <div class="stat-value" style="color:var(--accent-yellow)">${officeStock.full5}</div>
              <div class="stat-label">5 kg Full</div>
            </div>
            <div class="stat-card">
              <div class="stat-value" style="color:var(--accent-orange)">${officeStock.full19}</div>
              <div class="stat-label">19 kg Full</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="office-expenses">
        <div class="card">
          <div class="card-title">💸 Daily Expenses</div>
          <div class="empty-state">
            <div class="empty-state-icon">💸</div>
            <div class="empty-state-text">No expenses recorded today</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="office-dayend">
        <div class="card">
          <div class="card-title">📋 Day End Reconciliation</div>
          <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <div class="empty-state-text">Day end not closed yet</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="office-additional">
        <div class="card">
          <div class="card-title">➕ Additional Sales</div>
          <div class="empty-state">
            <div class="empty-state-icon">➕</div>
            <div class="empty-state-text">SV, Suraksha Pipe, Blue Book sales tracking</div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function buildBpcl() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📋 BPCL Verification / BPCL पडताळणी</div>
        <div class="page-header-sub">SAP: 187618</div>
      </div>
      <div style="display:flex;gap:8px">
        <label class="btn btn-primary btn-sm" style="cursor:pointer">
          📤 Day End PDF Upload
          <input type="file" accept=".pdf" style="display:none">
        </label>
        <label class="btn btn-success btn-sm" style="cursor:pointer">
          📊 SOA Excel Upload
          <input type="file" accept=".xls,.xlsx" style="display:none">
        </label>
      </div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'bpcl-dayend')">📋 Day End Report</button>
      <button class="tab-btn" onclick="switchTab(this,'bpcl-compare')">🔍 ERP vs BPCL</button>
      <button class="tab-btn" onclick="switchTab(this,'bpcl-soa')">📑 SOA</button>
      <button class="tab-btn" onclick="switchTab(this,'bpcl-codes')">🏷 Product Codes</button>
    </div>
    
    <div>
      <div class="tab-content active" id="bpcl-dayend">
        <div class="card">
          <div class="empty-state">
            <div class="empty-state-icon">📄</div>
            <div class="empty-state-text">No BPCL day end report uploaded</div>
            <div class="empty-state-sub">Upload PDF above to verify stock</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="bpcl-compare">
        <div class="card">
          <div class="card-title">🔍 ERP vs BPCL Comparison</div>
          <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <div class="empty-state-text">Upload BPCL report to compare</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="bpcl-soa">
        <div class="card">
          <div class="card-title">📑 Statement of Account</div>
          <div class="empty-state">
            <div class="empty-state-icon">📑</div>
            <div class="empty-state-text">No SOA uploaded</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="bpcl-codes">
        <div class="card">
          <div class="card-title">🏷 BPCL Product Codes (for reference)</div>
          <table>
            <tr><th>Product Code</th><th>Description</th></tr>
            <tr><td>5240</td><td>5 kg commercial Cylinder</td></tr>
            <tr><td>5250</td><td>5 kg Domestic Cylinder</td></tr>
            <tr><td>5260</td><td>5 kg commercial Cylinder</td></tr>
            <tr><td><strong>5350 + 5370</strong></td><td><strong>14.2 kg Domestic Cylinder (Full & Empty same product)</strong></td></tr>
            <tr><td>5400</td><td>19 kg commercial Cylinder</td></tr>
            <tr><td>5450</td><td>19 kg cutting Cylinder</td></tr>
            <tr><td>BPCDPR</td><td>14.2 kg DPR (De-pressure Regulator)</td></tr>
            <tr><td>BPCDPRF</td><td>5 kg DPR (De-pressure Regulator)</td></tr>
          </table>
        </div>
      </div>
    </div>
  `;
}

function buildPayroll() {
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
    
    <div>
      <div class="tab-content active" id="pay-delivery">
        <div class="alert alert-info" style="margin-bottom:16px">
          <strong>वेतन नियम / Wage Rules:</strong> Urban (Jaysingpur): ₹8/cylinder | Rural (Villages): ₹7/cylinder | Pair Bonus: ₹200/day | Cash Difference: deducted at once | Advance: ₹5000/month deduction
        </div>
        
        <div class="empty-state">
          <div class="empty-state-icon">💰</div>
          <div class="empty-state-text">No wage data available</div>
          <div class="empty-state-sub">Wages will be calculated after trip closures</div>
        </div>
      </div>
      
      <div class="tab-content" id="pay-office">
        <div class="card">
          <div class="empty-state">
            <div class="empty-state-icon">🏢</div>
            <div class="empty-state-text">Office staff payroll</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="pay-godown">
        <div class="card">
          <div class="empty-state">
            <div class="empty-state-icon">🏭</div>
            <div class="empty-state-text">Godown crew payroll</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="pay-advances">
        <div class="card">
          <div class="empty-state">
            <div class="empty-state-icon">💳</div>
            <div class="empty-state-text">Advances tracking</div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function buildTracking() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📍 Live Tracking / थेट ट्रॅकिंग</div>
        <div class="page-header-sub">All delivery vehicles — real-time location</div>
      </div>
      <span class="chip chip-green">LIVE</span>
    </div>
    
    <div class="grid-2" style="margin-bottom:24px">
      <div class="vehicle-card">
        <div class="vehicle-icon">🚐</div>
        <div class="vehicle-info">
          <div class="vehicle-name">Vishwas Bhore</div>
          <div class="vehicle-status" style="color:var(--text-muted)">Waiting at Godown</div>
          <div class="vehicle-location">📍 Godown</div>
          <div class="vehicle-update">Last update: Just now</div>
        </div>
      </div>
      <div class="vehicle-card">
        <div class="vehicle-icon">🏍</div>
        <div class="vehicle-info">
          <div class="vehicle-name">Mahesh Patil</div>
          <div class="vehicle-status" style="color:var(--text-muted)">Waiting at Godown</div>
          <div class="vehicle-location">📍 Godown</div>
          <div class="vehicle-update">Last update: Just now</div>
        </div>
      </div>
      <div class="vehicle-card">
        <div class="vehicle-icon">🚐</div>
        <div class="vehicle-info">
          <div class="vehicle-name">Harun Fakir</div>
          <div class="vehicle-status" style="color:var(--text-muted)">Waiting at Godown</div>
          <div class="vehicle-location">📍 Godown</div>
          <div class="vehicle-update">Last update: Just now</div>
        </div>
      </div>
      <div class="vehicle-card">
        <div class="vehicle-icon">🏍</div>
        <div class="vehicle-info">
          <div class="vehicle-name">Vishal Magdum</div>
          <div class="vehicle-status" style="color:var(--text-muted)">Waiting at Godown</div>
          <div class="vehicle-location">📍 Godown</div>
          <div class="vehicle-update">Last update: Just now</div>
        </div>
      </div>
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
          GPS tracking requires server setup. ngrok is already running at your URL.
        </div>
      </div>
    </div>
  `;
}

function buildStaff() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">👥 Staff Management</div>
      </div>
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
      <div>
        <div class="page-header-title">📢 Notices</div>
      </div>
      <button class="btn btn-primary btn-sm">+ New Notice</button>
    </div>
    <div class="empty-state">
      <div class="empty-state-icon">📢</div>
      <div class="empty-state-text">No notices posted yet</div>
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
      updateDashboardStats();
    }
  } catch (e) {
    console.error('Load deliveries error:', e);
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
            <div class="dcarea">🗂 ${d.area} | 📄 CM: ${d.cash_memo_no} | 👤 ${d.delivery_man}</div>
          </div>
          <div class="dcactions">
            <span class="chip chip-${d.status === 'scheduled' ? 'blue' : d.status === 'intrip' ? 'yellow' : d.status === 'delivered' ? 'green' : d.status === 'emergency' ? 'orange' : 'red'}">${d.status}</span>
            <div class="dcphone">📞 ${d.mobile}</div>
            ${d.otp ? `<div style="font-size:11px;color:var(--accent-green);margin-top:4px">OTP: ${d.otp}</div>` : ''}
            ${d.payment_mode ? `<div style="font-size:11px;color:var(--accent-blue);margin-top:4px">💳 ${d.payment_mode}</div>` : ''}
          </div>
        </div>
      `;
    });
    html += `</div>`;
  });
  
  container.innerHTML = html;
}

function filterDeliveries() {
  const searchTerm = document.querySelector('.search-input')?.value.toLowerCase() || '';
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

function updateDashboardStats() {
  // Stats are calculated in buildDashboard, this is just for real-time updates
}

async function handleCSVUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: async function(results) {
      const rows = results.data.filter(r => r.ConsumerName && r.CashMemoNo);
      console.log('Parsed CSV rows:', rows.length);
      
      // Send ALL rows to API
      const formData = new FormData();
      formData.append('csv_data', JSON.stringify(rows));
      
      try {
        const res = await fetch('api.php?action=upload_csv', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        
        if (data.success) {
          alert(`✅ Success! Loaded ${data.count} deliveries`);
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

updateDashboardStats();
</script>
</body>
</html>
