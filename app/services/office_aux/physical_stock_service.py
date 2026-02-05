from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.office_aux import OfficeAuxMonthPhysical


class PhysicalStockAlreadyCaptured(Exception):
    pass


def capture_month_end_physical(
    db: Session,
    month: str,
    item_id: int,
    physical_qty: int,
):
    """
    Capture physical stock ONCE at month end.
    """

    record = OfficeAuxMonthPhysical(
        month=month,
        item_id=item_id,
        physical_qty=physical_qty,
        captured_on=date.today(),
    )

    try:
        db.add(record)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise PhysicalStockAlreadyCaptured(
            f"Physical stock already captured for item {item_id} in {month}"
        )

    return record
