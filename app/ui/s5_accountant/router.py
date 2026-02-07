from fastapi import APIRouter
from app.ui.s5_accountant.pages.accountant_dashboard_page import get_accountant_dashboard

router = APIRouter(prefix="/ui/accounts", tags=["Accounts UI"])

@router.get("")
def accounts_dashboard():
    return get_accountant_dashboard()
