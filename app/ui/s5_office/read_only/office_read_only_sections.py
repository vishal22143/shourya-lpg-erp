"""
S5.2-C — Office Dashboard Read-Only Sections

Purpose:
- Define read-only sections visible to Office users
- Bind to existing backend endpoints
- Prevent write operations in this phase
"""

OFFICE_READ_ONLY_SECTIONS = {
    "stock_overview": {
        "label_en": "Stock Overview",
        "label_mr": "साठा आढावा",
        "endpoint": "GET /stock/ledger",
        "expandable": True
    },
    "wages_overview": {
        "label_en": "Wages Overview",
        "label_mr": "वेतन आढावा",
        "endpoint": "GET /wages/summary",
        "expandable": False
    },
    "bpcl_status": {
        "label_en": "BPCL Status",
        "label_mr": "BPCL स्थिती",
        "endpoint": "GET /bpcl/comparison",
        "expandable": True
    },
    "owner_day_end_view": {
        "label_en": "Owner Day-End View",
        "label_mr": "मालक दिवस समाप्ती",
        "endpoint": "GET /owner/day-end",
        "expandable": False
    }
}

def get_office_read_only_sections() -> dict:
    """
    Returns Office dashboard read-only section definitions.
    """
    return OFFICE_READ_ONLY_SECTIONS.copy()
