from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.base import Base

class DeliveryMan(Base):
    __tablename__ = 'delivery_men'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mobile = Column(String)
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    deactivated_at = Column(DateTime, nullable=True)
