"""
S5.2-E-5 — Auxiliary Variance Visibility Rules

- Office: view-only, acknowledge discrepancy
- Owner: full visibility
- Accountant: read-only, audit reference
"""

AUX_VARIANCE_VISIBILITY = {
    "office": {
        "can_view": True,
        "can_edit": False,
        "can_acknowledge": True
    },
    "owner": {
        "can_view": True,
        "can_edit": False
    },
    "accountant": {
        "can_view": True,
        "can_edit": False
    }
}

def get_aux_variance_visibility() -> dict:
    return AUX_VARIANCE_VISIBILITY.copy()
