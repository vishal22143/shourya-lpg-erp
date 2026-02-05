from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.office_aux import (
    OfficeAuxMonthOpening,
    OfficeAuxMovement,
    OfficeAuxMonthPhysical
)


def calculate_aux_month_variance(db: Session, month: str, item_id: int) -> dict:
    """
    Calculate expected stock, physical stock, and variance
    for a given auxiliary item and month.
    """

    opening = (
        db.query(OfficeAuxMonthOpening)
        .filter_by(month=month, item_id=item_id)
        .first()
    )
    if not opening:
        raise ValueError("Opening stock not found")

    movement_total = (
        db.query(func.coalesce(func.sum(OfficeAuxMovement.qty), 0))
        .filter_by(month=month, item_id=item_id)
        .scalar()
    )

    physical = (
        db.query(OfficeAuxMonthPhysical)
        .filter_by(month=month, item_id=item_id)
        .first()
    )
    if not physical:
        raise ValueError("Physical stock not captured")

    expected_qty = opening.opening_qty + movement_total
    variance = physical.physical_qty - expected_qty

    return {
        "month": month,
        "item_id": item_id,
        "opening_qty": opening.opening_qty,
        "movement_total": movement_total,
        "expected_qty": expected_qty,
        "physical_qty": physical.physical_qty,
        "variance": variance,
    }
