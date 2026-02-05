# ==========================================================
# SHOURYA LPG ERP — MASTER FREEZE DOCUMENT
# ==========================================================
# This file is the ONLY source of truth for ERP state.
# ChatGPT conversations are NOT persistent memory.
# Any new chat must follow this document strictly.
# ==========================================================

## 0. PROJECT IDENTITY
- Project Name: SHOURYA LPG ERP
- Domain: LPG Distribution (BPCL-aligned)
- Users:
  - Owner
  - Partner
  - Office
  - Delivery Man
  - BDA
  - Accountant (future)

---

## 1. SOURCE CONTROL (LOCKED)
- GitHub Repo: https://github.com/vishal22143/shourya-lpg-erp
- Branch: main
- Git is the ONLY source of truth
- No local-only logic allowed
- Every milestone = Git commit + tag

---

## 2. DEPLOYMENT (LOCKED)
- Hosting Platform: Render
- Backend Framework: FastAPI
- Database: SQLite (current), Postgres-ready
- Runtime Command: uvicorn main:app
- Delivery Mobile Access: Browser (Chrome / PWA)
- Owner & Partner Access: Laptop/Desktop only

---

## 3. DATABASE GOVERNANCE (NON-NEGOTIABLE)
- Alembic is MANDATORY
- No Base.metadata.create_all()
- No dashboard may query a table without migration
- Schema changes ONLY via Alembic revision
- All tables must physically exist in DB

STATUS:
- Alembic initialized
- env.py wired to Base.metadata
- Initial migration generated and applied
- Database schema is now REAL

---

## 4. LANGUAGE & UI RULES (GLOBAL)
- English + Marathi mandatory everywhere
- Symbols mandatory everywhere
- No new symbols without updating this file

STANDARD SYMBOL SET:
🔢 Stock Summary / साठा सारांश
💰 Cash Summary / रोख रक्कम सारांश
🚚 Delivery / डिलिव्हरी
🧾 BPCL Comparison / BPCL तुलना
⚠️ Discrepancy / तफावत
📦 Godown / गोडाऊन
🏢 Office / कार्यालय
🛵 Vehicle / वाहन
👤 Delivery Man / डिलिव्हरी कर्मचारी
👥 BDA / बी.डी.ए
🧮 Wages / वेतन
💳 Online Payment / ऑनलाईन पेमेंट
📍 Location / स्थान

---

## 5. COMPLETED FUNCTIONAL PHASES

S0 — Project bootstrap  
S1 — Auth & Role segregation  
S2 — System checks  
S3.1 — Delivery core logic  
S3.2 — Cash, advance, recovery  
S3.3 — Wages engine  
S4.1 — BPCL CSV import logic  
S4.2 — Map, area, routing, color codes  
S4.3 — Delivery UI contract (mobile-first)  

S5.1-A — Owner Day-End aggregation  
S5.1-B — Owner Day-End data wiring  
DATABASE ERROR LOOP FIXED VIA ALEMBIC

---

## 6. OWNER DAY-END (LOCKED DESIGN)

DESIGN TYPE:
- Desktop / Laptop FIRST
- SAP-style expandable dashboard
- NOT a summary report
- NOT mobile-first

ORDER (NON-CHANGEABLE):
1. 🔢 Stock Summary (Opening → Sale → Closing)
2. 💰 Cash Summary (Source-wise)
3. 🚚 Delivery-wise Breakup
4. 🧾 BPCL Comparison
5. ⚠️ Discrepancy Alerts

RULES:
- Every number must drill down
- No hard-coded column names
- No runtime schema guessing
- Missing data → empty section, never crash

---

## 7. CURRENT STATE (FREEZE POINT)

- Alembic migration applied
- All defined models now have physical tables
- Owner Day-End can be safely re-enabled
- Trial-and-error loop STOPPED

FREEZE TAG RECOMMENDED:
- v0.5-schema-stable

---

## 8. NEXT PHASES (FROM THIS POINT)

S5.1-C — Deep drill-down
  - Delivery → Trip → Stock movement
  - Cash → Source → Entry
  - Stock → Location → Movement

S5.2 — Office Dashboard
  - Live delivery control
  - Cash register
  - CSV re-upload
  - Manual corrections (logged)

S5.3 — Reports
  - Excel export
  - PDF export
  - BPCL punch-ready formats

S6 — Mobile UI hardening
  - Delivery UX polish
  - Offline tolerance
  - Call / map optimizations

S7 — BPCL Day-End Assist
  - Punch guidance
  - Variance explanation
  - Carry-forward logic

---

## 9. CHAT RECOVERY PROTOCOL (MANDATORY)

If chat crashes or new chat is opened:
1. Share THIS file (ERP_FREEZE.md)
2. Share project tree
3. Resume from CURRENT PHASE ONLY
4. No re-design
5. No re-explanation
6. No schema changes without Alembic

---

## 10. ABSOLUTE RULE
If a feature is not listed here,
IT DOES NOT EXIST.

[S5.2-E FREEZE]
- Office Auxiliary Stock scope frozen
- Opening stock immutable after save
- Month-based reconciliation enforced
- Isolated from core LPG logic

[S5.2-E-4 LOCK]
- Auxiliary reconciliation logic frozen
- No edits permitted without freeze update

[S5.2-E-5 LOCK]
- Variance reporting logic frozen
- Accountability mapping fixed

[S5.3 LOCK]
- Auxiliary stock UI wiring frozen

[S5.4 LOCK]
- Accountant dashboard frozen (read-only)

[S6 ROLE ROUTING LOCK]
- Role → route mapping frozen

[S6 COMPLETED]
- Integration checks passed
- Role routing frozen
- Git tagged v1.0-go-live
- Render deployment ready

[S7 COMPLETED]
- Admin bootstrap implemented
- Secure password hashing enabled
- User & role creation ready

[CLEANUP]
- Temporary debug/test files removed
- Cache cleared
- Repo stabilized for final steps
