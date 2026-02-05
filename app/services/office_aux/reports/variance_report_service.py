from app.services.office_aux.reconciliation_service import calculate_aux_month_variance


def generate_aux_variance_report(db, month: str, item_id: int) -> dict:
    """
    Generate variance report and classify accountability.
    Read-only. No persistence.
    """

    data = calculate_aux_month_variance(db, month, item_id)

    variance = data["variance"]

    if variance < 0:
        status = "SHORTAGE"
        accountable = "OFFICE / MANAGER ADVANCE"
    elif variance > 0:
        status = "EXCESS"
        accountable = "INFORMATIONAL"
    else:
        status = "MATCHED"
        accountable = "NONE"

    report = {
        "month": data["month"],
        "item_id": data["item_id"],
        "opening_qty": data["opening_qty"],
        "movement_total": data["movement_total"],
        "expected_qty": data["expected_qty"],
        "physical_qty": data["physical_qty"],
        "variance": variance,
        "status": status,
        "accountable_to": accountable,
    }

    return report
