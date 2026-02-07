from erp_spine import build_erp_spine
from auth_entry import router as auth_router
from ui_mounts import mount_ui

app = build_erp_spine()
app.include_router(auth_router)
mount_ui(app)
