from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from app.core.base import Base

class OfficeAuxMonthOpening(Base):
    __tablename__ = "office_aux_month_opening"

    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)  # YYYY-MM
    item_id = Column(Integer, ForeignKey("office_aux_item.id"), nullable=False)
    opening_qty = Column(Integer, nullable=False)
    created_on = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("month", "item_id", name="uq_aux_opening_month_item"),
    )
