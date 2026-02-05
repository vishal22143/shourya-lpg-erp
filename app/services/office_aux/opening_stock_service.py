from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.office_aux import OfficeAuxMonthOpening


class OpeningStockAlreadyExists(Exception):
    pass


def save_month_opening_stock(
    db: Session,
    month: str,
    item_id: int,
    opening_qty: int,
):
    """
    Save opening stock ONCE per (month, item).
    This operation is IMMUTABLE.
    """

    opening = OfficeAuxMonthOpening(
        month=month,
        item_id=item_id,
        opening_qty=opening_qty,
        created_on=date.today(),
    )

    try:
        db.add(opening)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise OpeningStockAlreadyExists(
            f"Opening stock already saved for item {item_id} in {month}"
        )

    return opening
