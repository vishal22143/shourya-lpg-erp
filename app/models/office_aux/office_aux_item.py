from sqlalchemy import Column, Integer, String, Boolean
from app.core.base import Base

class OfficeAuxItem(Base):
    __tablename__ = "office_aux_item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # CYLINDER / ACCESSORY
    active = Column(Boolean, default=True)
