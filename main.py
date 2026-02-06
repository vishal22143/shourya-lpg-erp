from fastapi import FastAPI

app = FastAPI(title="Shourya LPG ERP")

def try_include(path, name):
    try:
        module = __import__(path, fromlist=["router"])
        app.include_router(module.router)
        print(f"✓ Loaded {name}")
    except Exception as e:
        print(f"⚠ Skipped {name}: {e}")

# Core routers (only if present)
try_include("app.auth.router", "Auth")
try_include("app.ui.owner.router", "Owner UI")
try_include("app.ui.accounts.router", "Accounts UI")
try_include("app.ui.office.router", "Office UI")

@app.get("/")
def root():
    return {"status": "ERP BOOT OK", "mode": "admin"}
