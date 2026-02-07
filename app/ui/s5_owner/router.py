from fastapi import APIRouter
from app.ui.s5_owner.bindings.owner_top_panel import get_owner_top_panel

router = APIRouter(prefix="/ui/owner", tags=["Owner UI"])

@router.get("")
def owner_dashboard():
    return get_owner_top_panel()
