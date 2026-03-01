# Shourya Bharatgas Services — LPG ERP v5

**BPCL Distributor: 187618 | Jaysinghpur, Kolhapur**

## Quick Start

### 1. Install Python (if not installed)
Download Python 3.10+ from https://python.org

### 2. Install dependencies
```
pip install flask openpyxl
```

### 3. Copy data files to this folder
- `ni.csv` — Consumer master (9242 records)
- `ListOfBlockedConsumers.csv` — 7078 blocked consumers

### 4. Run
```
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

### 6. Login
- Use any staff mobile number
- Default PIN: **1234** (system forces change on first login)

### 7. Load data (one-time, Owner login)
- Go to Settings → Load Consumer Master (ni.csv)
- Go to Settings → Load Blocked List

---

## Staff Logins (default PIN: 1234)

| Name | Mobile | Role |
|------|--------|------|
| Vishal Patil | 7887456789 | Owner |
| Mrinmayi Patil | 8080802880 | Owner |
| Baba | 9665036191 | Owner |
| Rajesh Awale | 8007183197 | Manager |
| Mrs. Awale | 9807183197 | BDA (Chipri Beghar) |
| Vishwas Bhore | 7643982982 | Delivery |
| Swapnil Patil | 8830669611 | Delivery |
| Haroon Fakir | 9970660901 | Delivery |
| Vishal Magdum | 9096853954 | Delivery |
| Ajinath | 8669164977 | Driver |
| Sandeep | 8788076864 | Loader |
| Sager | 8605444617 | Loader |
| + 8 BDA owners | see db.py | BDA |

---

## Features

### Daily Operations
- 📁 BPCL CSV upload with deduplication (never overwrites delivered)
- 🚚 Uber-style delivery with GPS map (Leaflet.js)
- 📍 GPS saved ONLY at first doorstep delivery
- 🔒 OTP capture + central storage + export
- 🏭 Godown 3-zone empty count formula
- 🏘️ BDA portal with customer OTP list
- 💬 Team chat with photo sharing

### Financial
- 💵 Full denomination capture (₹500,200,100,50,20,10,coins)
- 📱 Online modes: QR, GPay, Paytm, BPCL Advance, Partial
- 💰 Auto wage calculation: Urban ₹8/Rural ₹7/Pair ₹200
- 🏦 Advance tracking with 20% monthly recovery cap
- 📊 BPCL SOA upload + reconciliation

### Reporting
- 💰 Monthly wage sheet with Mgr→Owner approval workflow
- 📊 BPCL Day End comparison (ERP vs SAP)
- 📋 GST export (GSTR-1 + GSTR-2 format)
- 📁 Cash ledger CSV export
- 🖨️ OTP export (area-wise, delivery-man-wise)

---

## Mobile Access (Local Network)

Find your computer's IP:
- Windows: `ipconfig` → IPv4 Address
- e.g. `192.168.1.5`

Open on mobile: `http://192.168.1.5:5000`

All staff can access on their phones over WiFi.

---

## Files
```
app.py          — Main Flask app
db.py           — Database + helpers
templates.py    — HTML base template
routes1.py      — Auth + Dashboard + Office
routes2.py      — Delivery (GPS map + OTP)
routes3.py      — Godown + BDA
routes4.py      — Wages + Accounting + BPCL Day End
routes5.py      — Users + Settings + Chat
erp.db          — SQLite database (auto-created)
static/         — CSS, images, chat photos
ni.csv          — Consumer master (copy here)
ListOfBlockedConsumers.csv — (copy here)
```
