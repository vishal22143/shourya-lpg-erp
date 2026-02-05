"""
S5.3 — Auxiliary Stock UI Contract (Office Dashboard)

Pure binding contract.
No computation.
"""

AUX_STOCK_UI_SECTIONS = {
    "opening_stock": {
        "title_en": "Auxiliary Opening Stock",
        "title_mr": "पूरक प्रारंभिक साठा",
        "service": "save_month_opening_stock",
        "editable": True,
        "editable_once": True
    },
    "monthly_movements": {
        "title_en": "Monthly Movements",
        "title_mr": "मासिक हालचाल",
        "service": "record_aux_movement",
        "editable": True
    },
    "month_end_physical": {
        "title_en": "Month-End Physical Stock",
        "title_mr": "महिना अखेर प्रत्यक्ष साठा",
        "service": "capture_month_end_physical",
        "editable": True,
        "editable_once": True
    },
    "variance_report": {
        "title_en": "Variance Report",
        "title_mr": "तफावत अहवाल",
        "service": "generate_aux_variance_report",
        "editable": False,
        "highlight_discrepancy": True
    }
}

def get_aux_stock_ui_sections() -> dict:
    return AUX_STOCK_UI_SECTIONS.copy()
