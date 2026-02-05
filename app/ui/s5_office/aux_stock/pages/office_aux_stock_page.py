"""
Office Dashboard — Auxiliary Stock Page Wiring
"""

from app.ui.s5_office.aux_stock.contracts.aux_stock_ui_contract import (
    get_aux_stock_ui_sections
)
from app.ui.s5_office.aux_stock.components.aux_stock_components import (
    get_aux_stock_components
)

def get_office_aux_stock_page() -> dict:
    return {
        "page_id": "office_aux_stock",
        "title_en": "Auxiliary Stock Control",
        "title_mr": "पूरक साठा नियंत्रण",
        "sections": get_aux_stock_ui_sections(),
        "components": get_aux_stock_components(),
        "access": "OFFICE_ONLY"
    }
