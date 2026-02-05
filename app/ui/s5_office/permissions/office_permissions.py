"""
S5.2-B — Office Dashboard Data Sources & Permissions Mapping

Purpose:
- Explicitly define Office read/write access
- Map Office UI actions to existing backend services
- Prevent unauthorized operations
"""

OFFICE_PERMISSIONS = {
    "delivery_monitoring": {
        "read": [
            "GET /delivery/active",
            "GET /trip/active",
            "GET /vehicle/status"
        ],
        "write": []
    },

    "cash_operations": {
        "read": [
            "GET /cash/opening",
            "GET /cash/summary"
        ],
        "write": [
            "POST /cash/opening",
            "POST /cash/in",
            "POST /cash/out",
            "POST /cash/denomination",
            "POST /cash/closing"
        ]
    },

    "csv_operations": {
        "read": [
            "GET /csv/status"
        ],
        "write": [
            "POST /csv/upload"
        ]
    },

    "manual_corrections": {
        "read": [
            "GET /delivery/remarks"
        ],
        "write": [
            "POST /delivery/remark",
            "POST /delivery/reschedule"
        ]
    },

    "read_only_sections": {
        "read": [
            "GET /stock/ledger",
            "GET /wages/summary",
            "GET /bpcl/comparison",
            "GET /owner/day-end"
        ],
        "write": []
    }
}

def get_office_permissions() -> dict:
    """
    Returns Office dashboard permissions mapping.
    """
    return OFFICE_PERMISSIONS.copy()
