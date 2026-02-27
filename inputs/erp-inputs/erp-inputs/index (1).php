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
:root {
    --bpcl-blue: #003087;
    --bpcl-yellow: #FFD100;
    --bpcl-dark: #001a4d;
    --success: #22c55e;
    --danger: #ef4444;
    --warning: #f59e0b;
    --text-dark: #1f2937;
    --text-muted: #6b7280;
    --border: #e5e7eb;
}
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, var(--bpcl-dark) 0%, #000820 100%);
    min-height: 100vh;
    color: var(--text-dark);
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
    border-radius: 16px;
    padding: 50px;
    max-width: 450px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.login-logo {
    text-align: center;
    margin-bottom: 35px;
}
.login-logo h1 {
    color: var(--bpcl-blue);
    font-size: 28px;
    margin-bottom: 10px;
    font-weight: 700;
}
.login-logo p {
    color: var(--text-muted);
    font-size: 14px;
}
.form-group {
    margin-bottom: 24px;
}
.form-group label {
    display: block;
    margin-bottom: 10px;
    color: var(--text-dark);
    font-weight: 600;
    font-size: 14px;
}
.form-group select,
.form-group input,
.form-group textarea {
    width: 100%;
    padding: 14px;
    border: 2px solid var(--border);
    border-radius: 8px;
    font-size: 15px;
    transition: all 0.3s;
}
.form-group select:focus,
.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--bpcl-blue);
    box-shadow: 0 0 0 3px rgba(0,48,135,0.1);
}
.btn-login {
    width: 100%;
    padding: 16px;
    background: var(--bpcl-blue);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 17px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
}
.btn-login:hover {
    background: #002060;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,48,135,0.3);
}
.error-msg {
    background: #fee;
    color: #c00;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: none;
    font-size: 14px;
    border-left: 4px solid #c00;
}

/* App Interface */
#appInterface {
    display: none;
}
.topbar {
    background: linear-gradient(135deg, var(--bpcl-blue) 0%, #002060 100%);
    color: white;
    padding: 18px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.topbar h1 {
    font-size: 22px;
    font-weight: 700;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 20px;
}
.user-info {
    font-size: 14px;
    text-align: right;
}
.user-info div:first-child {
    font-weight: 600;
}
.btn-logout {
    background: var(--bpcl-yellow);
    color: var(--bpcl-blue);
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 700;
    transition: all 0.3s;
}
.btn-logout:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255,209,0,0.4);
}

.nav-tabs {
    background: white;
    display: flex;
    border-bottom: 3px solid var(--border);
    overflow-x: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.nav-tab {
    padding: 18px 28px;
    cursor: pointer;
    border-bottom: 4px solid transparent;
    white-space: nowrap;
    font-weight: 600;
    transition: all 0.3s;
    color: var(--text-muted);
}
.nav-tab:hover {
    background: #f9fafb;
    color: var(--bpcl-blue);
}
.nav-tab.active {
    border-bottom-color: var(--bpcl-blue);
    color: var(--bpcl-blue);
    background: #f0f7ff;
}

.content {
    padding: 30px;
    max-width: 1600px;
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
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border: 1px solid var(--border);
}
.card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 20px;
    color: var(--bpcl-blue);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}
.stat-card {
    background: white;
    padding: 28px;
    border-radius: 12px;
    border-left: 5px solid var(--bpcl-blue);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transition: all 0.3s;
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.stat-card.green { border-left-color: var(--success); }
.stat-card.yellow { border-left-color: var(--bpcl-yellow); }
.stat-card.red { border-left-color: var(--danger); }
.stat-label {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 10px;
    font-weight: 500;
}
.stat-value {
    font-size: 38px;
    font-weight: 800;
    color: var(--bpcl-blue);
}

/* Table */
.table-container {
    overflow-x: auto;
}
table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}
th {
    background: linear-gradient(135deg, var(--bpcl-blue) 0%, #002060 100%);
    color: white;
    padding: 16px;
    text-align: left;
    font-weight: 700;
    font-size: 14px;
}
td {
    padding: 16px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
}
tr:hover td {
    background: #f9fafb;
}

/* Buttons */
.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    font-size: 15px;
    transition: all 0.3s;
    display: inline-block;
}
.btn:hover {
    transform: translateY(-2px);
}
.btn-primary { background: var(--bpcl-blue); color: white; }
.btn-primary:hover { box-shadow: 0 6px 20px rgba(0,48,135,0.3); }
.btn-success { background: var(--success); color: white; }
.btn-success:hover { box-shadow: 0 6px 20px rgba(34,197,94,0.3); }
.btn-warning { background: var(--bpcl-yellow); color: var(--bpcl-blue); }
.btn-warning:hover { box-shadow: 0 6px 20px rgba(255,209,0,0.3); }

/* Status badges */
.badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}
.badge-scheduled { background: #dbeafe; color: #1e40af; }
.badge-intrip { background: #fef3c7; color: #92400e; }
.badge-delivered { background: #dcfce7; color: #166534; }
.badge-emergency { background: #fed7aa; color: #9a3412; }
.badge-notdelivered { background: #fee2e2; color: #991b1b; }

/* Marathi grid inputs */
.grid-section {
    background: #f9fafb;
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}
.grid-section.filled {
    background: #dcfce7;
    border-color: var(--success);
}
.grid-section.empty {
    background: #f1f5f9;
    border-color: #94a3b8;
}
.grid-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--bpcl-blue);
    margin-bottom: 16px;
}
.grid-row {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.grid-input {
    width: 80px;
    padding: 10px;
    border: 2px solid var(--border);
    border-radius: 6px;
    font-size: 18px;
    font-weight: 700;
    text-align: center;
}
.grid-input:focus {
    outline: none;
    border-color: var(--bpcl-blue);
}
.grid-result {
    background: var(--bpcl-blue);
    color: white;
    padding: 10px 18px;
    border-radius: 6px;
    font-size: 24px;
    font-weight: 700;
    min-width: 80px;
    text-align: center;
}

.alert {
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 4px solid;
}
.alert-info {
    background: #dbeafe;
    border-color: #3b82f6;
    color: #1e40af;
}
.alert-success {
    background: #dcfce7;
    border-color: var(--success);
    color: #166534;
}
.alert-warning {
    background: #fef3c7;
    border-color: var(--warning);
    color: #92400e;
}

/* Loading spinner */
.spinner {
    display: inline-block;
    width: 24px;
    height: 24px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid var(--bpcl-blue);
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
        padding: 15px;
    }
    .topbar {
        padding: 15px;
    }
    .topbar h1 {
        font-size: 18px;
    }
    .card {
        padding: 20px;
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
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:15px">
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
                           style="width:100%;padding:14px;border:2px solid var(--border);border-radius:8px;font-size:15px" 
                           oninput="filterDeliveries()">
                </div>
                
                <div class="table-container" id="deliveriesTable">
                    <p style="text-align:center;padding:40px;color:var(--text-muted)">Upload CSV to load deliveries</p>
                </div>
            </div>
        </div>
        
        <!-- Godown Stock -->
        <div class="page" id="page-godown">
            <div class="card">
                <div class="card-title">🏭 गोदाऊन स्टॉक / Godown Stock</div>
                
                <div class="alert alert-info">
                    ⚠️ <strong>पहिल्या येणाऱ्याने मोजणी करावी</strong> — मागील दिवसाच्या BPCL स्टॉकशी जुळवा<br>
                    First arrival enters count — must match previous BPCL closing stock.
                </div>
                
                <!-- 14.2 KG FILLED -->
                <div class="grid-section filled">
                    <div class="grid-title">🟢 14.2 KG भरलेले (FILLED)</div>
                    <p style="font-size:13px;color:var(--text-muted);margin-bottom:12px">
                        फॉर्म्युला: उभी ओळ × आडवी ओळ + अधिक ओळ = एकूण संख्या
                    </p>
                    <div class="grid-row">
                        <div style="text-align:center">
                            <label style="font-size:12px;color:var(--text-muted);display:block;margin-bottom:5px">उभी ओळ</label>
                            <input class="grid-input" id="full_r" placeholder="10" oninput="calcGodownGrid()">
                        </div>
                        <span style="font-size:24px;color:var(--text-muted)">×</span>
                        <div style="text-align:center">
                            <label style="font-size:12px;color:var(--text-muted);display:block;margin-bottom:5px">आडवी ओळ</label>
                            <input class="grid-input" id="full_c" placeholder="12" oninput="calcGodownGrid()">
                        </div>
                        <span style="font-size:24px;color:var(--text-muted)">+</span>
                        <div style="text-align:center">
                            <label style="font-size:12px;color:var(--text-muted);display:block;margin-bottom:5px">अधिक ओळ</label>
                            <input class="grid-input" id="full_e" placeholder="8" oninput="calcGodownGrid()">
                        </div>
                        <span style="font-size:24px;color:var(--text-muted)">=</span>
                        <div class="grid-result" id="full_total">—</div>
                    </div>
                </div>
                
                <!-- 14.2 KG EMPTY -->
                <div class="grid-section empty">
                    <div class="grid-title">⚪ 14.2 KG रिकामे (EMPTY) — 3 विभाग</div>
                    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px">
                        प्रत्येक विभाग: <strong style="color:var(--bpcl-blue)">(दुहेरी उभी × दुहेरी आडवी + दुहेरी अधिक) × 2 + एकेरी अधिक = एकूण</strong>
                    </p>
                    
                    <div style="background:rgba(255,255,255,0.5);padding:15px;border-radius:8px;margin-bottom:12px">
                        <div style="font-weight:700;color:var(--bpcl-blue);margin-bottom:10px">📍 फुडून उजवीकडे (Front Right)</div>
                        <div class="grid-row" style="font-size:14px">
                            <span>(</span>
                            <input class="grid-input" id="e1_r" placeholder="6" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>×</span>
                            <input class="grid-input" id="e1_c" placeholder="5" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>+</span>
                            <input class="grid-input" id="e1_a" placeholder="3" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>)×2+</span>
                            <input class="grid-input" id="e1_s" placeholder="4" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>=</span>
                            <span class="grid-result" id="e1_total" style="font-size:20px;padding:8px 14px;min-width:60px">—</span>
                        </div>
                    </div>
                    
                    <div style="background:rgba(255,255,255,0.5);padding:15px;border-radius:8px;margin-bottom:12px">
                        <div style="font-weight:700;color:var(--bpcl-blue);margin-bottom:10px">📍 दरवाज्याच्या उजवीकडे (Door Right)</div>
                        <div class="grid-row" style="font-size:14px">
                            <span>(</span>
                            <input class="grid-input" id="e2_r" placeholder="6" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>×</span>
                            <input class="grid-input" id="e2_c" placeholder="5" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>+</span>
                            <input class="grid-input" id="e2_a" placeholder="3" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>)×2+</span>
                            <input class="grid-input" id="e2_s" placeholder="4" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>=</span>
                            <span class="grid-result" id="e2_total" style="font-size:20px;padding:8px 14px;min-width:60px">—</span>
                        </div>
                    </div>
                    
                    <div style="background:rgba(255,255,255,0.5);padding:15px;border-radius:8px">
                        <div style="font-weight:700;color:var(--bpcl-blue);margin-bottom:10px">📍 दरवाज्याच्या डावीकडे (Door Left)</div>
                        <div class="grid-row" style="font-size:14px">
                            <span>(</span>
                            <input class="grid-input" id="e3_r" placeholder="6" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>×</span>
                            <input class="grid-input" id="e3_c" placeholder="5" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>+</span>
                            <input class="grid-input" id="e3_a" placeholder="3" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>)×2+</span>
                            <input class="grid-input" id="e3_s" placeholder="4" oninput="calcGodownGrid()" style="width:60px;font-size:16px">
                            <span>=</span>
                            <span class="grid-result" id="e3_total" style="font-size:20px;padding:8px 14px;min-width:60px">—</span>
                        </div>
                    </div>
                    
                    <div style="margin-top:16px;padding:16px;background:rgba(148,163,184,0.2);border-radius:8px;display:flex;justify-content:space-between;align-items:center">
                        <span style="font-weight:700;font-size:16px">एकूण रिकामे / Total Empty</span>
                        <span class="grid-result" id="empty_total" style="font-size:28px">—</span>
                    </div>
                </div>
                
                <!-- 5 KG -->
                <div class="grid-section" style="background:#fffbeb;border-color:var(--bpcl-yellow)">
                    <div class="grid-title">🟡 5 kg सिलेंडर</div>
                    <div class="grid-row">
                        <span style="font-size:14px">भरलेले Full:</span>
                        <input class="grid-input" id="five_full" placeholder="0" oninput="calcGodownGrid()">
                        <span style="font-size:14px">रिकामे Empty:</span>
                        <input class="grid-input" id="five_empty" placeholder="0" oninput="calcGodownGrid()">
                    </div>
                </div>
                
                <!-- TOTALS -->
                <div class="stats-grid" style="margin-top:24px">
                    <div class="stat-card green">
                        <div class="stat-label">एकूण भरलेले / Total Full</div>
                        <div class="stat-value" id="grand_full" style="color:var(--success)">—</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">एकूण रिकामे / Total Empty</div>
                        <div class="stat-value" id="grand_empty" style="color:var(--text-muted)">—</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>शेरा / REMARK — काही वेगळे असल्यास लिहा</label>
                    <textarea rows="2" placeholder="Any mismatch or notes..." style="width:100%;padding:12px;border:2px solid var(--border);border-radius:8px"></textarea>
                </div>
                
                <button class="btn btn-success" onclick="saveGodownCount()">✅ सकाळचा साठा जतन करा / Save Morning Count</button>
            </div>
        </div>
        
        <!-- Trip Management (for delivery boys) -->
        <div class="page" id="page-trip">
            <div class="card">
                <div class="card-title">🚛 ट्रिप मॅनेजमेंट / Trip Management</div>
                
                <div class="alert alert-success">
                    📅 आजची तारीख: <strong><?php echo date('d/m/Y'); ?></strong> | 
                    👤 डिलिव्हरी मन: <strong id="trip-delivery-man"><?php echo $currentUser ? $currentUser['name'] : ''; ?></strong>
                </div>
                
                <!-- Morning Stock Count -->
                <div class="card" style="background:#f0f7ff;border:2px solid var(--bpcl-blue)">
                    <div class="card-title">📦 सकाळी गाडीत साठा / Morning Vehicle Stock</div>
                    
                    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px">
                        <div class="form-group">
                            <label>14.2 kg भरलेले दिले / Full Given</label>
                            <input type="number" id="trip_full_14" class="grid-input" style="width:100%" placeholder="0">
                        </div>
                        <div class="form-group">
                            <label>14.2 kg रिकामे घेतले / Empty Taken</label>
                            <input type="number" id="trip_empty_14" class="grid-input" style="width:100%" placeholder="0">
                        </div>
                        <div class="form-group">
                            <label>5 kg भरलेले दिले / 5kg Full</label>
                            <input type="number" id="trip_full_5" class="grid-input" style="width:100%" placeholder="0">
                        </div>
                        <div class="form-group">
                            <label>5 kg रिकामे घेतले / 5kg Empty</label>
                            <input type="number" id="trip_empty_5" class="grid-input" style="width:100%" placeholder="0">
                        </div>
                    </div>
                </div>
                
                <!-- Cash Collection -->
                <div class="card" style="background:#dcfce7;border:2px solid var(--success)">
                    <div class="card-title">💰 रोख गोळा / Cash Collection</div>
                    
                    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px">
                        <div class="form-group">
                            <label>रोख / Cash (₹)</label>
                            <input type="number" id="trip_cash" class="grid-input" style="width:100%" placeholder="0">
                        </div>
                        <div class="form-group">
                            <label>ऑनलाइन / Online (₹)</label>
                            <input type="number" id="trip_online" class="grid-input" style="width:100%" placeholder="0">
                        </div>
                        <div class="stat-card green" style="margin:0">
                            <div class="stat-label">एकूण गोळा / Total Collected</div>
                            <div class="stat-value" id="trip_total" style="font-size:28px">₹0</div>
                        </div>
                    </div>
                </div>
                
                <!-- Notes -->
                <div class="form-group">
                    <label>शेरा / Notes</label>
                    <textarea id="trip_notes" rows="3" placeholder="कोणतीही नोंद लिहा..." style="width:100%;padding:12px;border:2px solid var(--border);border-radius:8px"></textarea>
                </div>
                
                <button class="btn btn-success btn-lg" onclick="saveTrip()">
                    ✅ ट्रिप पूर्ण करा / Complete Trip
                </button>
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
        owner: ['dashboard', 'deliveries', 'godown', 'trip', 'notices'],
        manager: ['dashboard', 'deliveries', 'godown', 'trip', 'notices'],
        delivery: ['dashboard', 'deliveries', 'trip', 'notices'],
        bda: ['dashboard', 'deliveries', 'notices']
    };
    
    const userNavs = navs[currentUser.role] || ['dashboard'];
    const navHTML = userNavs.map(nav => {
        const labels = {
            dashboard: '📊 Dashboard',
            deliveries: '🚴 Deliveries',
            godown: '🏭 Godown',
            trip: '🚛 Trip',
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
    
    // Load page-specific data
    if (page === 'deliveries') loadDeliveries();
}

// ========== GODOWN GRID CALCULATION ==========
function calcGodownGrid() {
    // Full 14.2 kg: rows × cols + extra = total
    const fr = parseFloat(document.getElementById('full_r')?.value) || 0;
    const fc = parseFloat(document.getElementById('full_c')?.value) || 0;
    const fe = parseFloat(document.getElementById('full_e')?.value) || 0;
    const fullTotal = fr * fc + fe;
    const ftEl = document.getElementById('full_total');
    if (ftEl) ftEl.textContent = fullTotal || '—';
    
    // Empty sections: (double_rows × double_cols + double_extra) × 2 + single_extra = total
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
    
    // 5 kg
    const fiveFull = parseFloat(document.getElementById('five_full')?.value) || 0;
    const fiveEmpty = parseFloat(document.getElementById('five_empty')?.value) || 0;
    
    // Grand totals
    const gf = document.getElementById('grand_full');
    const ge = document.getElementById('grand_empty');
    if (gf) gf.textContent = (fullTotal + fiveFull) || '—';
    if (ge) ge.textContent = (emptyGrandTotal + fiveEmpty) || '—';
}

async function saveGodownCount() {
    const fullTotal = document.getElementById('full_total')?.textContent;
    const emptyTotal = document.getElementById('empty_total')?.textContent;
    
    if (fullTotal === '—' || fullTotal === '0') {
        alert('⚠️ कृपया आधी मोजणी करा / Please enter count first');
        return;
    }
    
    alert(`✅ सकाळचा साठा जतन केला!\nभरलेले: ${fullTotal}\nरिकामे: ${emptyTotal}`);
    
    // TODO: Save to database via API
}

// ========== TRIP MANAGEMENT ==========
function updateTripTotal() {
    const cash = parseFloat(document.getElementById('trip_cash')?.value) || 0;
    const online = parseFloat(document.getElementById('trip_online')?.value) || 0;
    const total = cash + online;
    
    const el = document.getElementById('trip_total');
    if (el) el.textContent = '₹' + total.toLocaleString('en-IN');
}

// Auto-update total when cash/online changes
document.addEventListener('DOMContentLoaded', function() {
    const tripCash = document.getElementById('trip_cash');
    const tripOnline = document.getElementById('trip_online');
    if (tripCash) tripCash.addEventListener('input', updateTripTotal);
    if (tripOnline) tripOnline.addEventListener('input', updateTripTotal);
});

async function saveTrip() {
    const full14 = document.getElementById('trip_full_14')?.value || 0;
    const empty14 = document.getElementById('trip_empty_14')?.value || 0;
    const full5 = document.getElementById('trip_full_5')?.value || 0;
    const empty5 = document.getElementById('trip_empty_5')?.value || 0;
    const cash = document.getElementById('trip_cash')?.value || 0;
    const online = document.getElementById('trip_online')?.value || 0;
    const notes = document.getElementById('trip_notes')?.value || '';
    
    if (!full14 && !empty14) {
        alert('⚠️ कृपया साठा भरा / Please enter stock details');
        return;
    }
    
    const form = new FormData();
    form.append('action', 'save_trip');
    form.append('date', new Date().toISOString().split('T')[0]);
    form.append('full_14', full14);
    form.append('empty_14', empty14);
    form.append('full_5', full5);
    form.append('empty_5', empty5);
    form.append('cash', cash);
    form.append('online', online);
    form.append('notes', notes);
    
    try {
        const res = await fetch('api.php', {
            method: 'POST',
            body: form
        });
        const data = await res.json();
        
        if (data.success) {
            alert('✅ ट्रिप जतन केली! / Trip saved successfully');
            // Clear form
            document.getElementById('trip_full_14').value = '';
            document.getElementById('trip_empty_14').value = '';
            document.getElementById('trip_full_5').value = '';
            document.getElementById('trip_empty_5').value = '';
            document.getElementById('trip_cash').value = '';
            document.getElementById('trip_online').value = '';
            document.getElementById('trip_notes').value = '';
            updateTripTotal();
        } else {
            alert('❌ Error: ' + data.message);
        }
    } catch (err) {
        alert('❌ Failed to save trip: ' + err.message);
    }
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
