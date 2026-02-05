"""
S5.4 — Accountant Dashboard Data Contract
Read-only bindings to existing endpoints
"""

ACCOUNTANT_SECTIONS = {
    "cash_ledger": {
        "label_en": "Cash Ledger",
        "label_mr": "रोख वहन",
        "endpoint": "GET /cash/ledger",
        "expandable": True
    },
    "delivery_summary": {
        "label_en": "Delivery Summary",
        "label_mr": "वितरण सारांश",
        "endpoint": "GET /delivery/summary",
        "expandable": True
    },
    "wages_advances": {
        "label_en": "Wages & Advances",
        "label_mr": "वेतन व आगाऊ",
        "endpoint": "GET /wages/summary",
        "expandable": True
    },
    "bpcl_comparison": {
        "label_en": "BPCL Reconciliation",
        "label_mr": "BPCL ताळमेळ",
        "endpoint": "GET /bpcl/comparison",
        "expandable": True
    },
    "aux_variance": {
        "label_en": "Auxiliary Stock Variance",
        "label_mr": "पूरक साठा तफावत",
        "endpoint": "SERVICE generate_aux_variance_report",
        "expandable": True
    },
    "owner_day_end": {
        "label_en": "Owner Day-End (Read Only)",
        "label_mr": "मालक दिवस समाप्ती",
        "endpoint": "GET /owner/day-end",
        "expandable": False
    }
}

def get_accountant_sections() -> dict:
    return ACCOUNTANT_SECTIONS.copy()
