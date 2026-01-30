from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from app.core.base import Base

class DeliveryDaySummary(Base):
    __tablename__ = 'delivery_day_summary'

    delivery_man_id = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)

    total_cylinders = Column(Integer, nullable=False)
    day_type = Column(String, nullable=False)  # SHAHARI / GAVAATIL
    helper_used = Column(Boolean, default=False)

    confirmed_by = Column(String)  # OWNER / PARTNER / OFFICE
    confirmed_at = Column(DateTime)
