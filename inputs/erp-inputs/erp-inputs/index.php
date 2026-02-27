<?php
require_once 'config.php';

// If already logged in, redirect to app
$currentUser = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="mr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shourya Bharatgas ERP</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #001a4d 0%, #000820 100%);
    min-height: 100vh;
}

/* Login Page */
#loginPage {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
}
.login-card {
    background: white;
    border-radius: 12px;
    padding: 40px;
    max-width: 400px;
    width: 100%;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.login-logo {
    text-align: center;
    margin-bottom: 30px;
}
.login-logo h1 {
    color: #003087;
    font-size: 24px;
    margin-bottom: 8px;
}
.login-logo p {
    color: #666;
    font-size: 13px;
}
.form-group {
    margin-bottom: 20px;
}
.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #333;
    font-weight: 600;
    font-size: 14px;
}
.form-group select,
.form-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 15px;
}
.form-group select:focus,
.form-group input:focus {
    outline: none;
    border-color: #003087;
}
.btn-login {
    width: 100%;
    padding: 14px;
    background: #003087;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
}
.btn-login:hover {
    background: #002060;
}
.error-msg {
    background: #fee;
    color: #c00;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 20px;
    display: none;
    font-size: 14px;
}

/* App Interface */
#appInterface {
    display: none;
}
.topbar {
    background: #003087;
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.topbar h1 {
    font-size: 20px;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 15px;
}
.user-info {
    font-size: 14px;
}
.btn-logout {
    background: #FFD100;
    color: #003087;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
}

.nav-tabs {
    background: white;
    display: flex;
    border-bottom: 2px solid #ddd;
    overflow-x: auto;
}
.nav-tab {
    padding: 15px 20px;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    white-space: nowrap;
    font-weight: 500;
}
.nav-tab:hover {
    background: #f5f5f5;
}
.nav-tab.active {
    border-bottom-color: #003087;
    color: #003087;
}

.content {
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.page {
    display: none;
}
.page.active {
    display: block;
}

/* Cards */
.card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #003087;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}
.stat-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #003087;
}
.stat-card.green { border-left-color: #22c55e; }
.stat-card.yellow { border-left-color: #FFD100; }
.stat-card.red { border-left-color: #ef4444; }
.stat-label {
    font-size: 13px;
    color: #666;
    margin-bottom: 8px;
}
.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #003087;
}

/* Table */
table {
    width: 100%;
    border-collapse: collapse;
}
th {
    background: #f5f5f5;
    padding: 12px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid #ddd;
}
td {
    padding: 12px;
    border-bottom: 1px solid #eee;
}
tr:hover td {
    background: #f9f9f9;
}

/* Buttons */
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}
.btn-primary { background: #003087; color: white; }
.btn-success { background: #22c55e; color: white; }
.btn-warning { background: #FFD100; color: #003087; }

/* Status badges */
.badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
.badge-scheduled { background: #dbeafe; color: #1e40af; }
.badge-intrip { background: #fef3c7; color: #92400e; }
.badge-delivered { background: #dcfce7; color: #166534; }
.badge-emergency { background: #fed7aa; color: #9a3412; }
.badge-notdelivered { background: #fee2e2; color: #991b1b; }

/* File upload */
.upload-area {
    border: 2px dashed #ddd;
    border-radius: 8px;
    padding: 30px;
    text-align: center;
    cursor: pointer;
}
.upload-area:hover {
    border-color: #003087;
    background: #f9f9f9;
}

/* Loading spinner */
.spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #003087;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
    .content {
        padding: 10px;
    }
}
</style>
</head>
<body>

<!-- Login Page -->
<div id="loginPage" <?php if($currentUser) echo 'style="display:none"'; ?>>
    <div class="login-card">
        <div class="login-logo">
            <h1>🔥 SHOURYA BHARATGAS</h1>
            <p>SAP: 187618 | Jaysingpur</p>
            <p style="font-size:11px;color:#999;margin-top:8px">BPCL Authorized Distributor</p>
        </div>
        
        <div class="error-msg" id="loginError"></div>
        
        <form id="loginForm" onsubmit="return doLogin(event)">
            <div class="form-group">
                <label>वापरकर्ता / User</label>
                <select name="username" required>
                    <option value="">-- Select User --</option>
                    <optgroup label="👤 Owners">
                        <option value="owner">Vishal Patil (Owner)</option>
                        <option value="owner2">Mrinmayi Patil (Owner)</option>
                    </optgroup>
                    <optgroup label="💼 Management">
                        <option value="manager">Rajesh Awale (Manager)</option>
                    </optgroup>
                    <optgroup label="🚴 Delivery Boys">
                        <option value="delivery_bhore">Vishwas Bhore</option>
                        <option value="delivery_mahesh">Mahesh Patil</option>
                        <option value="delivery_harun">Harun Fakir</option>
                        <option value="delivery_magdum">Vishal Magdum</option>
                    </optgroup>
                    <optgroup label="🏪 BDA Owners">
                        <option value="bda_kondigre">Kondigre - Sarika Waghmode</option>
                        <option value="bda_nimshirgav1">Nimshirgav - Kumar Thomake</option>
                        <option value="bda_nimshirgav2">Nimshirgav - Lakhane</option>
                        <option value="bda_danoli">Danoli - Manoj</option>
                        <option value="bda_kothali">Kothali - Yadav</option>
                        <option value="bda_kavatesar">Kavatesar - Sudhakar Patil</option>
                        <option value="bda_shirol">Shirol - Vikrant Kamble</option>
                        <option value="bda_awale">Chipri Beghar - Mrs. Awale</option>
                    </optgroup>
                </select>
            </div>
            
            <div class="form-group">
                <label>पासवर्ड / Password</label>
                <input type="password" name="password" required placeholder="Enter password">
            </div>
            
            <button type="submit" class="btn-login">🔐 लॉगिन करा / Login</button>
        </form>
        
        <p style="text-align:center;margin-top:20px;font-size:11px;color:#999">
            Default password: 1234
        </p>
    </div>
</div>

<!-- App Interface -->
<div id="appInterface" <?php if($currentUser) echo 'style="display:block"'; ?>>
    <div class="topbar">
        <h1>🔥 SHOURYA BHARATGAS ERP</h1>
        <div class="topbar-right">
            <div class="user-info">
                <div id="userName"><?php echo $currentUser ? $currentUser['name'] : ''; ?></div>
                <div style="font-size:12px;opacity:0.8" id="userRole"><?php echo $currentUser ? $currentUser['designation'] : ''; ?></div>
            </div>
            <button class="btn-logout" onclick="doLogout()">↩ Logout</button>
        </div>
    </div>
    
    <div class="nav-tabs" id="navTabs"></div>
    
    <div class="content">
        <!-- Dashboard -->
        <div class="page active" id="page-dashboard">
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card green">
                    <div class="stat-label">✅ Delivered Today</div>
                    <div class="stat-value" id="stat-delivered">0</div>
                </div>
                <div class="stat-card yellow">
                    <div class="stat-label">🚴 In Trip</div>
                    <div class="stat-value" id="stat-intrip">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">📋 Scheduled</div>
                    <div class="stat-value" id="stat-scheduled">0</div>
                </div>
                <div class="stat-card red">
                    <div class="stat-label">❌ Not Delivered</div>
                    <div class="stat-value" id="stat-notdelivered">0</div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">📊 Today's Summary</div>
                <p>Total Deliveries: <strong id="total-today">0</strong></p>
                <p>Cash Collected: <strong style="color:#22c55e">₹<span id="cash-today">0</span></strong></p>
            </div>
        </div>
        
        <!-- Deliveries -->
        <div class="page" id="page-deliveries">
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
                    <div class="card-title" style="margin:0">🚴 Deliveries / डिलिव्हरी</div>
                    <div>
                        <label class="btn btn-primary" style="cursor:pointer;margin:0">
                            📤 Upload CSV
                            <input type="file" id="csvUpload" accept=".csv" style="display:none" onchange="handleCSVUpload(event)">
                        </label>
                    </div>
                </div>
                
                <div style="margin-bottom:15px">
                    <input type="text" id="searchDelivery" placeholder="🔍 Search customer, area, mobile..." 
                           style="width:100%;padding:10px;border:1px solid #ddd;border-radius:6px" 
                           oninput="filterDeliveries()">
                </div>
                
                <div id="deliveriesTable">
                    <p style="text-align:center;padding:40px;color:#999">Upload CSV to load deliveries</p>
                </div>
            </div>
        </div>
        
        <!-- Other pages will be added here -->
    </div>
</div>

<script>
let currentUser = <?php echo json_encode($currentUser); ?>;
let deliveries = [];

// Login
async function doLogin(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    
    try {
        const res = await fetch('api.php?action=login', {
            method: 'POST',
            body: form
        });
        const data = await res.json();
        
        if (data.success) {
            location.reload();
        } else {
            document.getElementById('loginError').textContent = data.message;
            document.getElementById('loginError').style.display = 'block';
        }
    } catch (err) {
        alert('Login failed: ' + err.message);
    }
}

// Logout
async function doLogout() {
    await fetch('api.php?action=logout');
    location.reload();
}

// Initialize app
if (currentUser) {
    buildNav();
    loadDashboard();
}

function buildNav() {
    const navs = {
        owner: ['dashboard', 'deliveries', 'godown', 'office', 'payroll', 'notices'],
        manager: ['dashboard', 'deliveries', 'godown', 'office', 'payroll', 'notices'],
        delivery: ['dashboard', 'deliveries', 'notices']
    };
    
    const userNavs = navs[currentUser.role] || ['dashboard'];
    const navHTML = userNavs.map(nav => {
        const labels = {
            dashboard: '📊 Dashboard',
            deliveries: '🚴 Deliveries',
            godown: '🏭 Godown',
            office: '🏢 Office',
            payroll: '💰 Payroll',
            notices: '📢 Notices'
        };
        return `<div class="nav-tab ${nav === 'dashboard' ? 'active' : ''}" onclick="showPage('${nav}')">${labels[nav]}</div>`;
    }).join('');
    
    document.getElementById('navTabs').innerHTML = navHTML;
}

function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    
    const pageEl = document.getElementById('page-' + page);
    if (pageEl) pageEl.classList.add('active');
    
    event.target.classList.add('active');
}

// Load dashboard stats
async function loadDashboard() {
    try {
        const res = await fetch('api.php?action=get_dashboard_stats');
        const data = await res.json();
        
        if (data.success) {
            const stats = data.data;
            document.getElementById('stat-delivered').textContent = stats.delivered || 0;
            document.getElementById('stat-intrip').textContent = stats.intrip || 0;
            document.getElementById('stat-scheduled').textContent = stats.scheduled || 0;
            document.getElementById('stat-notdelivered').textContent = stats.notdelivered || 0;
            document.getElementById('total-today').textContent = stats.total_today || 0;
            document.getElementById('cash-today').textContent = (stats.cash_collected || 0).toLocaleString('en-IN');
        }
    } catch (err) {
        console.error('Failed to load dashboard:', err);
    }
}

// CSV Upload
async function handleCSVUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const form = new FormData();
    form.append('csv_file', file);
    form.append('action', 'upload_csv');
    
    try {
        const res = await fetch('api.php', {
            method: 'POST',
            body: form
        });
        const data = await res.json();
        
        if (data.success) {
            alert(data.message);
            loadDeliveries();
        } else {
            alert('Upload failed: ' + data.message);
        }
    } catch (err) {
        alert('Upload error: ' + err.message);
    }
}

// Load deliveries
async function loadDeliveries() {
    try {
        const res = await fetch('api.php?action=get_deliveries');
        const data = await res.json();
        
        if (data.success) {
            deliveries = data.data.deliveries;
            renderDeliveries(deliveries);
        }
    } catch (err) {
        console.error('Failed to load deliveries:', err);
    }
}

function renderDeliveries(list) {
    if (list.length === 0) {
        document.getElementById('deliveriesTable').innerHTML = '<p style="text-align:center;padding:40px;color:#999">No deliveries found</p>';
        return;
    }
    
    const statusBadges = {
        scheduled: 'badge-scheduled',
        intrip: 'badge-intrip',
        delivered: 'badge-delivered',
        emergency: 'badge-emergency',
        notdelivered: 'badge-notdelivered'
    };
    
    const html = `
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Customer</th>
                    <th>Area</th>
                    <th>Mobile</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Operator</th>
                </tr>
            </thead>
            <tbody>
                ${list.map(d => `
                    <tr>
                        <td>${d.sl_no}</td>
                        <td><strong>${d.consumer_name}</strong><br><small style="color:#666">${d.consumer_number}</small></td>
                        <td>${d.area}</td>
                        <td>${d.mobile}</td>
                        <td style="max-width:200px"><small>${d.address}</small></td>
                        <td><span class="badge ${statusBadges[d.status]}">${d.status}</span></td>
                        <td><small>${d.operator_name}</small></td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    document.getElementById('deliveriesTable').innerHTML = html;
}

function filterDeliveries() {
    const search = document.getElementById('searchDelivery').value.toLowerCase();
    const filtered = deliveries.filter(d => 
        d.consumer_name.toLowerCase().includes(search) ||
        d.area.toLowerCase().includes(search) ||
        d.mobile.includes(search)
    );
    renderDeliveries(filtered);
}

// Load deliveries on page load if CSV was previously uploaded
if (currentUser) {
    loadDeliveries();
}
</script>

</body>
</html>
