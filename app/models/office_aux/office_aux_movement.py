from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.base import Base

class OfficeAuxMovement(Base):
    __tablename__ = "office_aux_movement"

    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)  # YYYY-MM
    item_id = Column(Integer, ForeignKey("office_aux_item.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    movement_type = Column(String, nullable=False)  # SALE / ISSUE / RETURN
    movement_date = Column(Date, nullable=False)
