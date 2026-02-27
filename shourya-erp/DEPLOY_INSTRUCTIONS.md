# SHOURYA BHARATGAS ERP — DEPLOYMENT GUIDE
## Complete steps to go live on Render

---

## STEP 1: Set up Supabase (Free PostgreSQL Database)

1. Go to: https://supabase.com
2. Sign up / Login
3. Click **New Project**
   - Name: `shourya-erp`
   - Password: create a strong password (SAVE IT)
   - Region: **South Asia (ap-south-1)** or nearest
4. Wait ~2 minutes for project to create
5. Go to: **Settings → Database**
6. Under "Connection string" select **URI**
7. Copy the string — it looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   ```
8. **Save this URL** — you need it in Step 3

---

## STEP 2: Wipe your GitHub repo (clean slate)

Open Command Prompt on your laptop:

```cmd
cd C:\
mkdir shourya-erp-fresh
cd shourya-erp-fresh

:: Initialize new git
git init
git remote add origin https://github.com/vishal22143/shourya-lpg-erp.git

:: Copy all files from downloaded folder into shourya-erp-fresh
:: (copy all files from the downloaded ZIP here)

git add .
git commit -m "Clean slate ERP v1.0 — complete rewrite"
git branch -M main
git push origin main --force
```

> ⚠️ `--force` will replace all old broken code. This is intentional.

---

## STEP 3: Set Environment Variables on Render

1. Go to: https://dashboard.render.com
2. Click your service: **shourya-lpg-erp**
3. Click **Environment** in left menu
4. Click **Add Environment Variable** and add these:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (paste your Supabase URI from Step 1) |
| `SECRET_KEY` | `shourya-erp-2025-vishal-mrinmayi-secure-key-xyz123` |

5. Click **Save Changes**

---

## STEP 4: Update Render Build/Start Command

In Render service settings:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## STEP 5: Trigger Deploy

In Render dashboard, click **Manual Deploy → Deploy latest commit**

Wait 2-3 minutes. You should see "Live" in green.

---

## STEP 6: Seed Initial Data

Once deployed, open your browser and go to:
```
https://shourya-lpg-erp.onrender.com/health
```
You should see: `{"status":"ok","service":"Shourya Bharatgas ERP"}`

Now seed the initial users and vehicles. On your laptop:
```cmd
cd shourya-erp-fresh
pip install fastapi sqlalchemy passlib itsdangerous python-dotenv psycopg2-binary

:: Create .env file with your Supabase URL
echo DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres > .env
echo SECRET_KEY=shourya-erp-2025-vishal-mrinmayi-secure-key-xyz123 >> .env

python scripts/seed_data.py
```

This seeds: Vishal, Mrinmayi, Bhore, Swapnil, Haroon, Sandip, Sagar, Ajinath, Office Staff + 5 vehicles + 3 BDAs.

---

## STEP 7: Login and Test

Go to: **https://shourya-lpg-erp.onrender.com**

| User | Mobile | PIN | Role |
|------|--------|-----|------|
| Vishal Patil | 9876500001 | 1234 | OWNER |
| Mrinmayi Patil | 9876500002 | 1234 | PARTNER |
| Bhore | 9876500003 | 1111 | DELIVERY |
| Swapnil Patil | 9876500004 | 2222 | DELIVERY |
| Haroon | 9876500006 | 4444 | DELIVERY |
| Sandip | 9876500007 | 5555 | LOADER |
| Office Staff | 9876500010 | 8888 | OFFICE |

> ⚠️ **CHANGE ALL PINS AFTER FIRST LOGIN** (via Owner → Users → change PIN)

---

## DAILY OPERATION FLOW

```
Morning:
1. Delivery Man → Login → Godown → Enter Physical Stock
2. Office → Upload BPCL CSV (delivery list)
3. Delivery Man → Open Trip → Select Vehicle → Enter Cylinders
4. Deliver each customer → Mark status → Enter payment

During day:
5. BDA → Record BDA transactions
6. Office → Add expenses, advances

Evening:
7. Delivery Man → Close Trip (enter empty cylinders returned, final cash)
8. Owner → Dashboard → Generate Day End
9. Compare with BPCL SAP day end
10. Owner → Lock Day (when all correct)
```

---

## MOBILE ACCESS

Any user can open Chrome/Safari on mobile and go to:
**https://shourya-lpg-erp.onrender.com**

No app install needed. Works on Android and iPhone.

⚠️ Render free tier sleeps after 15 min inactivity. First load may take 30-50 seconds.
   To avoid this: upgrade Render to Starter plan (~$7/month) = always on.

---

## IMPORTANT MOBILE NUMBERS TO UPDATE

After seeding, go to **Owner → Users** and update:
- Each staff member's actual mobile number
- Each staff member's actual PIN
- Vehicles: add actual registration numbers
- BDA: add actual BDA owner names and mobile numbers

---

## BACKUP

Data is in Supabase (PostgreSQL cloud). Supabase has automatic backups.
You can also export from Supabase → Table Editor → Export as CSV anytime.
