from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from app.core.base import Base

class OfficeAuxMonthPhysical(Base):
    __tablename__ = "office_aux_month_physical"

    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)  # YYYY-MM
    item_id = Column(Integer, ForeignKey("office_aux_item.id"), nullable=False)
    physical_qty = Column(Integer, nullable=False)
    captured_on = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("month", "item_id", name="uq_aux_physical_month_item"),
    )
