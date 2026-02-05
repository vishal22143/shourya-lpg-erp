"""
S5.1-C — Owner Top Panel Binding (READ-ONLY)
RESTORED AS PER FREEZE

Source:
- /owner/day-end payload

Rules:
- No computation
- No DB access
- No mutation
"""

def bind_owner_top_panel(day_end_payload: dict) -> dict:
    if not day_end_payload:
        return {
            "date": None,
            "day_status": "UNKNOWN",
            "bpcl_status": "UNKNOWN",
            "totals": {
                "stock": "N/A",
                "cash": "N/A",
                "delivery": "N/A"
            }
        }

    date = day_end_payload.get("date")
    sections = day_end_payload.get("sections", [])

    day_status = "OK"
    bpcl_status = "PENDING"

    has_stock = False
    has_cash = False
    has_delivery = False

    for s in sections:
        symbol = s.get("symbol")
        if symbol == "🔢":
            has_stock = True
        elif symbol == "💰":
            has_cash = True
        elif symbol == "🚚":
            has_delivery = True
        elif symbol == "🧾":
            bpcl_status = s.get("status", "PENDING")
        elif symbol == "⚠️" and s.get("alerts"):
            day_status = "ATTENTION"

    return {
        "date": date,
        "day_status": day_status,
        "bpcl_status": bpcl_status,
        "totals": {
            "stock": "AVAILABLE" if has_stock else "N/A",
            "cash": "AVAILABLE" if has_cash else "N/A",
            "delivery": "AVAILABLE" if has_delivery else "N/A"
        }
    }
