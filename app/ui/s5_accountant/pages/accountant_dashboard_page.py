"""
Accountant Dashboard Page Wiring
"""

from app.ui.s5_accountant.contracts.accountant_data_contract import (
    get_accountant_sections
)

def get_accountant_dashboard_page() -> dict:
    return {
        "page_id": "accountant_dashboard",
        "title_en": "Accountant Dashboard",
        "title_mr": "लेखापाल डॅशबोर्ड",
        "sections": get_accountant_sections(),
        "access": "ACCOUNTANT_ONLY",
        "mode": "READ_ONLY"
    }
