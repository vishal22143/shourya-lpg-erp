"""
Auxiliary Stock UI Components (Metadata Only)
"""

AUX_STOCK_COMPONENTS = {
    "opening_form": {
        "fields": ["item", "opening_qty"],
        "lock_after_save": True,
        "show_warning": "Once saved, opening stock cannot be changed"
    },
    "movement_table": {
        "columns": ["date", "item", "qty", "movement_type"],
        "append_only": True
    },
    "physical_form": {
        "fields": ["item", "physical_qty"],
        "lock_after_save": True
    },
    "variance_card": {
        "fields": [
            "opening_qty",
            "movement_total",
            "expected_qty",
            "physical_qty",
            "variance",
            "status",
            "accountable_to"
        ],
        "color_rules": {
            "SHORTAGE": "red",
            "EXCESS": "amber",
            "MATCHED": "green"
        }
    }
}

def get_aux_stock_components() -> dict:
    return AUX_STOCK_COMPONENTS.copy()
