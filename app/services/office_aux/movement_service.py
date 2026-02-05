from datetime import date
from sqlalchemy.orm import Session

from app.models.office_aux import OfficeAuxMovement


def record_aux_movement(
    db: Session,
    month: str,
    item_id: int,
    qty: int,
    movement_type: str,
):
    """
    Append-only movement record.
    No update, no delete.
    """

    movement = OfficeAuxMovement(
        month=month,
        item_id=item_id,
        qty=qty,
        movement_type=movement_type,
        movement_date=date.today(),
    )

    db.add(movement)
    db.commit()
    return movement
