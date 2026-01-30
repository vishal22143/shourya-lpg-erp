from sqlalchemy import Column, Integer, String, Date
from app.core.base import Base

class DeliveryCylinderDetail(Base):
    __tablename__ = 'delivery_cylinder_detail'

    delivery_man_id = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    area_type = Column(String, primary_key=True)  # URBAN / RURAL
    cylinders = Column(Integer, nullable=False)
