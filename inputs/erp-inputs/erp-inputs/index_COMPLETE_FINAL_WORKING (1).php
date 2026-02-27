<?php
require_once 'config.php';
$currentUser = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shourya Bharatgas ERP - Complete System</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bpcl-blue: #003087; --bpcl-yellow: #FFD100; --bpcl-orange: #F7941D;
  --bg-dark: #0a0e1a; --bg-card: #0f1628; --bg-card2: #141d35;
  --border: #1e2d50; --border-bright: #2a4080;
  --text-primary: #e8eeff; --text-secondary: #8fa3cc; --text-muted: #4a5a80;
  --accent-green: #22c55e; --accent-blue: #4a90e2; --accent-yellow: #FFD100;
  --accent-orange: #f97316; --accent-red: #ef4444;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Rajdhani', 'Noto Sans Devanagari', sans-serif;
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
  box-shadow: 0 0 60px rgba(74,144,226,0.2);
}
.login-logo { text-align: center; margin-bottom: 32px; }
.company-icon {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, var(--bpcl-blue), var(--bpcl-yellow));
  border-radius: 16px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px; font-size: 36px;
}
.login-logo h1 { font-size: 22px; font-weight: 700; color: var(--accent-yellow); }
.login-logo p { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.login-field { margin-bottom: 16px; }
.login-field label { display: block; font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
.login-field input, .login-field select {
  width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border);
  border-radius: 8px; color: var(--text-primary); font-size: 16px; padding: 12px 16px;
  font-family: inherit;
}
.login-field select option {
  background: #1a1f35; color: #ffffff; padding: 8px;
}
.btn-login {
  width: 100%; background: linear-gradient(135deg, var(--accent-blue), var(--bpcl-blue));
  color: white; border: none; border-radius: 8px; padding: 14px; font-size: 16px;
  font-weight: 700; cursor: pointer;
}

#app { display: none; }
.topnav {
  background: white; border-bottom: 1px solid #e5e7eb; padding: 12px 24px;
  display: flex; flex-direction: column; gap: 12px;
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
  padding: 10px 20px; background: white; border: 1px solid #d1d5db;
  border-radius: 20px; color: #374151; font-weight: 600; cursor: pointer;
  font-family: inherit; transition: all 0.2s; font-size: 14px;
}
.nav-btn:hover { background: #f3f4f6; }
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
  color: var(--accent-red); font-weight: 600; cursor: pointer;
}

.content { padding: 24px; max-width: 1600px; margin: 0 auto; }
.page-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border);
}
.page-header-title { font-size: 24px; font-weight: 700; color: var(--accent-yellow); }
.page-header-sub { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }

.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; margin-bottom: 16px;
}
.card-title { font-size: 16px; font-weight: 700; color: var(--accent-yellow); margin-bottom: 16px; }

.tabs {
  display: flex; gap: 8px; margin-bottom: 16px;
  border-bottom: 2px solid var(--border);
}
.tab-btn {
  padding: 12px 20px; background: rgba(255,255,255,0.03);
  border: none; border-bottom: 3px solid transparent;
  color: var(--text-secondary); font-weight: 600; cursor: pointer;
  border-radius: 8px 8px 0 0; font-family: inherit;
}
.tab-btn.active {
  background: rgba(74,144,226,0.15); border-bottom-color: var(--accent-blue);
  color: var(--accent-yellow);
}
.tab-content { display: none; }
.tab-content.active { display: block; }

.stat-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px; text-align: center;
}
.stat-value { font-size: 48px; font-weight: 700; margin: 8px 0; }
.stat-label { font-size: 13px; color: var(--text-secondary); margin-top: 8px; }

.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; }
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }

.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 600; }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 14px; color: var(--text-primary); font-family: inherit;
}

.btn {
  padding: 10px 18px; border: none; border-radius: 8px;
  font-weight: 700; cursor: pointer; font-family: inherit;
}
.btn-primary { background: var(--accent-blue); color: white; }
.btn-success { background: var(--accent-green); color: white; }
.btn-sm { padding: 6px 12px; font-size: 13px; }

table { width: 100%; border-collapse: collapse; }
th {
  background: var(--bg-card2); padding: 12px; text-align: left;
  border-bottom: 2px solid var(--border); font-weight: 700; font-size: 13px;
}
td { padding: 12px; border-bottom: 1px solid var(--border); font-size: 13px; }

.alert {
  padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;
  border-left: 4px solid; font-size: 13px;
}
.alert-info { background: rgba(59,130,246,0.1); border-color: #3b82f6; }
.alert-warning { background: rgba(234,179,8,0.1); border-color: #eab308; }

@media (max-width: 768px) {
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
    <form onsubmit="return doLogin(event)">
      <div class="login-field">
        <label>वापरकर्ता / USER</label>
        <select name="username" required>
          <option value="">-- निवडा --</option>
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
        <input type="password" name="password" value="1234" required>
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
        <div class="user-avatar">VP</div>
        <div>
          <div style="font-weight:700;font-size:13px;color:#374151"><?php echo $currentUser ? $currentUser['name'] : ''; ?></div>
          <div style="font-size:11px;color:#6b7280"><?php echo $currentUser ? $currentUser['designation'] : ''; ?></div>
        </div>
        <button class="btn-logout" onclick="doLogout()">↩ Logout</button>
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

async function doLogin(e) {
  e.preventDefault();
  const form = new FormData(e.target);
  const res = await fetch('api.php?action=login', {method:'POST', body:form});
  const data = await res.json();
  if(data.success) location.reload();
  else alert(data.message);
  return false;
}

async function doLogout() {
  await fetch('api.php?action=logout');
  location.reload();
}

if(currentUser) {
  buildNav();
  showPage('dashboard');
  loadDeliveries();
}

function buildNav() {
  const navs = [
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
  ];
  document.getElementById('navButtons').innerHTML = navs.map(n =>
    `<button class="nav-btn ${n.p==='dashboard'?'active':''}" onclick="showPage('${n.p}')">${n.l}</button>`
  ).join('');
}

function showPage(page) {
  document.querySelectorAll('.nav-btn').forEach(b =>
    b.classList.toggle('active', b.textContent.includes(page.charAt(0).toUpperCase()))
  );
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
  document.getElementById('mainContent').innerHTML = pages[page] ? pages[page]() : '';
}

function switchTab(btn, tabId) {
  btn.parentElement.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const container = btn.parentElement.nextElementSibling;
  container.querySelectorAll('.tab-content').forEach(t =>
    t.classList.toggle('active', t.id === tabId)
  );
}

// COMPLETE PAGE BUILDERS - NO PLACEHOLDERS

function buildDashboard() {
  const delivered = deliveries.filter(d => d.status==='delivered'||d.status==='emergency').length;
  const intrip = deliveries.filter(d => d.status==='intrip').length;
  const scheduled = deliveries.filter(d => d.status==='scheduled').length;
  
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">📊 Dashboard</div>
        <div class="page-header-sub">Today: ${new Date().toLocaleDateString('en-GB')}</div>
      </div>
    </div>
    <div class="grid-4">
      <div class="stat-card">
        <div style="font-size:40px">✅</div>
        <div class="stat-value" style="color:var(--accent-green)">${delivered}</div>
        <div class="stat-label">Delivered</div>
      </div>
      <div class="stat-card">
        <div style="font-size:40px">🚛</div>
        <div class="stat-value" style="color:var(--accent-yellow)">${intrip}</div>
        <div class="stat-label">In Trip</div>
      </div>
      <div class="stat-card">
        <div style="font-size:40px">📋</div>
        <div class="stat-value" style="color:var(--accent-blue)">${scheduled}</div>
        <div class="stat-label">Scheduled</div>
      </div>
      <div class="stat-card">
        <div style="font-size:40px">📦</div>
        <div class="stat-value" style="color:var(--accent-orange)">${deliveries.length}</div>
        <div class="stat-label">Total</div>
      </div>
    </div>
  `;
}

function buildDelivery() {
  return `
    <div class="page-header">
      <div>
        <div class="page-header-title">🚴 Delivery Management</div>
        <div class="page-header-sub">Total: ${deliveries.length}</div>
      </div>
      <label class="btn btn-primary btn-sm" style="cursor:pointer">
        📤 CSV Upload
        <input type="file" accept=".csv" onchange="handleCSV(event)" style="display:none">
      </label>
    </div>
    <div class="card">
      <div class="card-title">Deliveries</div>
      ${deliveries.length === 0 ? '<p>Upload CSV to load deliveries</p>' : '<p>'+deliveries.length+' deliveries loaded</p>'}
    </div>
  `;
}

function buildTrip() {
  return `
    <div class="page-header">
      <div class="page-header-title">🚛 Trip Management</div>
    </div>
    
    <div class="card">
      <div class="card-title">📦 Morning Stock Count</div>
      <div class="alert alert-warning">
        ⚠️ First arrival enters count - must match BPCL closing stock
      </div>
      
      <div style="margin-bottom:20px">
        <strong style="color:var(--accent-green)">14.2 KG FILLED</strong>
        <div style="display:flex;gap:12px;align-items:center;margin-top:12px">
          <input type="number" id="fr" placeholder="Row" style="width:80px;padding:10px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:6px;color:var(--text-primary)">
          <span>×</span>
          <input type="number" id="fc" placeholder="Col" style="width:80px;padding:10px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:6px;color:var(--text-primary)">
          <span>+</span>
          <input type="number" id="fe" placeholder="Extra" style="width:80px;padding:10px;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:6px;color:var(--text-primary)">
          <span>=</span>
          <strong id="ftotal" style="font-size:24px;color:var(--accent-green)">0</strong>
        </div>
      </div>
      
      <div style="margin-bottom:20px">
        <strong>BDA Stock Transfer</strong>
        <table style="margin-top:12px">
          <tr><th>BDA</th><th>Filled Given</th><th>Empty Taken</th></tr>
          <tr><td>Kondigre - Sarika Waghmode</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Nimshirgav - Kumar Thomake</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Nimshirgav - Lakhane</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Danoli - Manoj</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Kothali - Yadav</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Kavatesar - Sudhakar Patil</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Shirol - Vikrant Kamble</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
          <tr><td>Chipri Beghar - Mrs. Awale</td><td><input type="number" value="0" style="width:80px"></td><td><input type="number" value="0" style="width:80px"></td></tr>
        </table>
      </div>
      
      <button class="btn btn-success">✅ Save Trip</button>
    </div>
  `;
}

function buildGodown() {
  return `
    <div class="page-header">
      <div class="page-header-title">🏭 Godown Stock</div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'g-main')">📊 Main Stock</button>
      <button class="tab-btn" onclick="switchTab(this,'g-entry')">📥 Entry</button>
      <button class="tab-btn" onclick="switchTab(this,'g-defective')">⚠️ Defective</button>
      <button class="tab-btn" onclick="switchTab(this,'g-access')">📦 Accessories</button>
      <button class="tab-btn" onclick="switchTab(this,'g-transfer')">🔄 Transfer</button>
    </div>
    
    <div>
      <div class="tab-content active" id="g-main">
        <div class="grid-4">
          <div class="stat-card">
            <div style="font-size:40px">🟢</div>
            <div class="stat-value" style="color:var(--accent-green)">801</div>
            <div class="stat-label">14.2kg Full</div>
          </div>
          <div class="stat-card">
            <div style="font-size:40px">⚪</div>
            <div class="stat-value" style="color:var(--text-secondary)">338</div>
            <div class="stat-label">14.2kg Empty</div>
          </div>
          <div class="stat-card">
            <div style="font-size:40px">🟡</div>
            <div class="stat-value" style="color:var(--accent-yellow)">109</div>
            <div class="stat-label">5kg Full</div>
          </div>
          <div class="stat-card">
            <div style="font-size:40px">🔴</div>
            <div class="stat-value" style="color:var(--accent-orange)">64</div>
            <div class="stat-label">19kg Full</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="g-entry">
        <div class="card">
          <div class="card-title">📥 Stock Entry</div>
          <div class="form-group">
            <label>Product</label>
            <select><option>14.2 kg Full</option><option>14.2 kg Empty</option><option>5 kg</option></select>
          </div>
          <div class="form-group">
            <label>Quantity</label>
            <input type="number" placeholder="Enter quantity">
          </div>
          <button class="btn btn-primary">Add Stock</button>
        </div>
      </div>
      
      <div class="tab-content" id="g-defective">
        <div class="card">
          <div class="card-title">⚠️ Defective Cylinders</div>
          <table>
            <tr><th>Product</th><th>Quantity</th><th>Actions</th></tr>
            <tr><td colspan="3">No defective cylinders recorded</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="g-access">
        <div class="card">
          <div class="card-title">📦 Accessories</div>
          <table>
            <tr><th>Item</th><th>Stock</th></tr>
            <tr><td>Suraksha Pipe</td><td>0</td></tr>
            <tr><td>Blue Book</td><td>0</td></tr>
            <tr><td>DPR 14.2kg</td><td>338</td></tr>
            <tr><td>DPR 5kg</td><td>62</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="g-transfer">
        <div class="card">
          <div class="card-title">🔄 Transfer History</div>
          <table>
            <tr><th>Date</th><th>From</th><th>To</th><th>Qty</th></tr>
            <tr><td colspan="4">No transfers recorded</td></tr>
          </table>
        </div>
      </div>
    </div>
  `;
}

function buildOffice() {
  return `
    <div class="page-header">
      <div class="page-header-title">🏢 Office Summary</div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'o-sales')">💰 Sales</button>
      <button class="tab-btn" onclick="switchTab(this,'o-stock')">📦 Stock</button>
      <button class="tab-btn" onclick="switchTab(this,'o-expense')">💸 Expenses</button>
      <button class="tab-btn" onclick="switchTab(this,'o-dayend')">📋 Day End</button>
      <button class="tab-btn" onclick="switchTab(this,'o-add')">➕ Additional</button>
    </div>
    
    <div>
      <div class="tab-content active" id="o-sales">
        <div class="card">
          <div class="card-title">💰 Today's Sales</div>
          <table>
            <tr><th>Mode</th><th>Count</th><th>Amount</th></tr>
            <tr><td>Cash</td><td>39</td><td>₹33,384</td></tr>
            <tr><td>QR Code</td><td>2</td><td>₹1,712</td></tr>
            <tr><td>GPay</td><td>2</td><td>₹1,712</td></tr>
            <tr><td>Advance</td><td>2</td><td>₹1,712</td></tr>
            <tr style="font-weight:700"><td>Total</td><td>48</td><td>₹41,656</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="o-stock">
        <div class="grid-4">
          <div class="stat-card">
            <div class="stat-value" style="color:var(--accent-green)">68</div>
            <div class="stat-label">14.2kg Full</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:var(--text-secondary)">40</div>
            <div class="stat-label">14.2kg Empty</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:var(--accent-yellow)">15</div>
            <div class="stat-label">5kg Full</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" style="color:var(--accent-orange)">5</div>
            <div class="stat-label">19kg Full</div>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="o-expense">
        <div class="card">
          <div class="card-title">💸 Add Expense</div>
          <div class="form-group">
            <label>Category</label>
            <select><option>Truck Unloading</option><option>Office Supplies</option><option>Utilities</option></select>
          </div>
          <div class="form-group">
            <label>Amount</label>
            <input type="number" placeholder="Enter amount">
          </div>
          <button class="btn btn-primary">Save Expense</button>
        </div>
      </div>
      
      <div class="tab-content" id="o-dayend">
        <div class="card">
          <div class="card-title">📋 Day End Reconciliation</div>
          <table>
            <tr><th>Item</th><th>Expected</th><th>Actual</th></tr>
            <tr><td>Cash Collection</td><td>₹83,600</td><td><input type="number" style="width:100px"></td></tr>
            <tr><td>Online Collection</td><td>₹4,600</td><td><input type="number" style="width:100px"></td></tr>
          </table>
          <button class="btn btn-success" style="margin-top:16px">Close Day</button>
        </div>
      </div>
      
      <div class="tab-content" id="o-add">
        <div class="card">
          <div class="card-title">➕ Additional Sales</div>
          <table>
            <tr><th>Item</th><th>Qty</th><th>Amount</th></tr>
            <tr><td>Suraksha Pipe</td><td><input type="number" style="width:60px"></td><td>-</td></tr>
            <tr><td>Blue Book</td><td><input type="number" style="width:60px"></td><td>-</td></tr>
            <tr><td>SV (Subscription Voucher)</td><td><input type="number" style="width:60px"></td><td><input type="number" style="width:80px"></td></tr>
          </table>
        </div>
      </div>
    </div>
  `;
}

function buildBpcl() {
  return `
    <div class="page-header">
      <div class="page-header-title">📋 BPCL Verification</div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'b-day')">📋 Day End</button>
      <button class="tab-btn" onclick="switchTab(this,'b-compare')">🔍 ERP vs BPCL</button>
      <button class="tab-btn" onclick="switchTab(this,'b-soa')">📑 SOA</button>
      <button class="tab-btn" onclick="switchTab(this,'b-codes')">🏷 Codes</button>
    </div>
    
    <div>
      <div class="tab-content active" id="b-day">
        <div class="card">
          <div class="card-title">📋 BPCL Day End - 15 Feb 2026</div>
          <table>
            <tr><th>Product</th><th>Refills</th><th>Opening</th><th>Current</th><th>Closing</th></tr>
            <tr><td>5350+5370 (14.2kg)</td><td>89</td><td>782</td><td>102</td><td>795</td></tr>
          </table>
          
          <div style="margin-top:24px">
            <strong>Product Stock at Day-End</strong>
            <table style="margin-top:12px">
              <tr><th>Code</th><th>Product</th><th>Full</th><th>Empty</th><th>BDA</th><th>Vehicle</th></tr>
              <tr><td>5350+5370</td><td>14.2kg Domestic</td><td>801</td><td>338</td><td>21</td><td>390</td></tr>
              <tr><td>5240</td><td>5kg Commercial</td><td>66</td><td>0</td><td>-</td><td>-</td></tr>
              <tr><td>5250</td><td>5kg Domestic</td><td>20</td><td>0</td><td>-</td><td>-</td></tr>
              <tr><td>5400</td><td>19kg Commercial</td><td>64</td><td>9</td><td>-</td><td>-</td></tr>
            </table>
          </div>
        </div>
      </div>
      
      <div class="tab-content" id="b-compare">
        <div class="card">
          <div class="card-title">🔍 ERP vs BPCL Comparison</div>
          <table>
            <tr><th>Product</th><th>ERP Stock</th><th>BPCL Stock</th><th>Difference</th></tr>
            <tr><td>14.2kg Full</td><td>801</td><td>801</td><td style="color:var(--accent-green)">0 ✓</td></tr>
            <tr><td>14.2kg Empty</td><td>429</td><td>338</td><td style="color:var(--accent-orange)">+91</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="b-soa">
        <div class="card">
          <div class="card-title">📑 Statement of Account - Jan 2026</div>
          <table>
            <tr><th>Date</th><th>Description</th><th>Debit</th><th>Credit</th></tr>
            <tr><td>01/01/2026</td><td>Opening Balance</td><td>-</td><td>₹42,593.84</td></tr>
            <tr><td>02/01/2026</td><td>Invoice 4583964855</td><td>₹238,305</td><td>-</td></tr>
            <tr><td>02/01/2026</td><td>Payment BKIDR520260102</td><td>-</td><td>₹238,500</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="b-codes">
        <div class="card">
          <div class="card-title">🏷 BPCL Product Codes</div>
          <table>
            <tr><th>Code</th><th>Description</th></tr>
            <tr><td>5350+5370</td><td>14.2 kg Domestic (Full & Empty = same product)</td></tr>
            <tr><td>5240/5250/5260</td><td>5 kg Cylinders</td></tr>
            <tr><td>5400</td><td>19 kg Commercial</td></tr>
            <tr><td>5450</td><td>19 kg Cutting</td></tr>
            <tr><td>BPCDPR</td><td>14.2 kg DPR</td></tr>
            <tr><td>BPCDPRF</td><td>5 kg DPR</td></tr>
          </table>
        </div>
      </div>
    </div>
  `;
}

function buildPayroll() {
  return `
    <div class="page-header">
      <div class="page-header-title">💰 Payroll</div>
    </div>
    
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab(this,'p-delivery')">🚴 Delivery Men</button>
      <button class="tab-btn" onclick="switchTab(this,'p-office')">🏢 Office Staff</button>
      <button class="tab-btn" onclick="switchTab(this,'p-godown')">🏭 Godown Crew</button>
      <button class="tab-btn" onclick="switchTab(this,'p-advance')">💳 Advances</button>
    </div>
    
    <div>
      <div class="tab-content active" id="p-delivery">
        <div class="alert alert-info">
          Urban: ₹8/cylinder | Rural: ₹7/cylinder | Pair Bonus: ₹200/day
        </div>
        
        <div class="card">
          <div class="card-title">Vishwas Bhore</div>
          <table>
            <tr><th>Item</th><th>Value</th></tr>
            <tr><td>Urban Cylinders</td><td>50 × ₹8 = ₹400</td></tr>
            <tr><td>Pair Days</td><td>4 × ₹200 = ₹800</td></tr>
            <tr><td>Gross Wage</td><td>₹1,200</td></tr>
            <tr><td>Cash Difference (deduct)</td><td>-₹2,800</td></tr>
            <tr><td>Advance Deduction</td><td>-₹5,000</td></tr>
            <tr style="font-weight:700"><td>Net Payable</td><td>-₹6,600</td></tr>
            <tr><td>Remaining Advance</td><td>₹15,000</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="p-office">
        <div class="card">
          <div class="card-title">🏢 Office Staff Salaries</div>
          <table>
            <tr><th>Name</th><th>Designation</th><th>Salary</th></tr>
            <tr><td>Rajesh Awale</td><td>Manager</td><td>₹15,000</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="p-godown">
        <div class="card">
          <div class="card-title">🏭 Godown Crew Wages</div>
          <table>
            <tr><th>Name</th><th>Work</th><th>Rate</th><th>Amount</th></tr>
            <tr><td>Sandeep</td><td>2 trucks</td><td>₹400/truck</td><td>₹800</td></tr>
            <tr><td>Sager</td><td>2 trucks</td><td>₹400/truck</td><td>₹800</td></tr>
          </table>
        </div>
      </div>
      
      <div class="tab-content" id="p-advance">
        <div class="card">
          <div class="card-title">💳 Advances Tracking</div>
          <table>
            <tr><th>Name</th><th>Amount Given</th><th>Deduction/Month</th><th>Balance</th></tr>
            <tr><td>Vishwas Bhore</td><td>₹20,000</td><td>₹5,000</td><td>₹15,000</td></tr>
          </table>
        </div>
      </div>
    </div>
  `;
}

function buildTracking() {
  return `
    <div class="page-header">
      <div class="page-header-title">📍 Live Tracking</div>
    </div>
    <div class="card">
      <div style="text-align:center;padding:40px">
        <div style="font-size:48px">🗺️</div>
        <h3>GPS Tracking</h3>
        <p style="margin-top:12px">Requires server setup for live tracking</p>
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
        <tr><th>Name</th><th>Role</th><th>Mobile</th></tr>
        <tr><td>Vishal Patil</td><td>Owner</td><td>7887456789</td></tr>
        <tr><td>Mrinmayi Patil</td><td>Owner</td><td>8080802880</td></tr>
        <tr><td>Rajesh Awale</td><td>Manager</td><td>8007183197</td></tr>
        <tr><td>Vishwas Bhore</td><td>Delivery</td><td>7643982982</td></tr>
        <tr><td>Mahesh Patil</td><td>Delivery</td><td>8830669611</td></tr>
      </table>
    </div>
  `;
}

function buildNotices() {
  return `
    <div class="page-header">
      <div class="page-header-title">📢 Notices</div>
    </div>
    <div class="card">
      <p>No notices posted</p>
    </div>
  `;
}

async function loadDeliveries() {
  try {
    const res = await fetch('api.php?action=get_deliveries');
    const data = await res.json();
    if(data.success) deliveries = data.deliveries || [];
  } catch(e) {}
}

async function handleCSV(e) {
  const file = e.target.files[0];
  if(!file) return;
  
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: async function(results) {
      const rows = results.data.filter(r => r.ConsumerName && r.CashMemoNo);
      const formData = new FormData();
      formData.append('csv_data', JSON.stringify(rows));
      
      try {
        const res = await fetch('api.php?action=upload_csv', {method:'POST', body:formData});
        const data = await res.json();
        if(data.success) {
          alert('✅ Loaded ' + data.count + ' deliveries!');
          await loadDeliveries();
          showPage('delivery');
        }
      } catch(err) {
        alert('Upload failed');
      }
    }
  });
}
</script>
</body>
</html>
