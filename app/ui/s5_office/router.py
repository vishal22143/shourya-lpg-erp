from fastapi import APIRouter
from app.ui.s5_office.read_only.office_read_only_sections import get_office_read_only

router = APIRouter(prefix="/ui/office", tags=["Office UI"])

@router.get("")
def office_dashboard():
    return get_office_read_only()
