from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.base import Base

class DeliveryTrip(Base):
    __tablename__ = 'delivery_trips'
    id = Column(Integer, primary_key=True)
    delivery_man_id = Column(Integer, ForeignKey('delivery_men.id'))
    date = Column(Date, nullable=False)
    trip_no = Column(Integer, nullable=False)
    status = Column(String, default='OPEN')

class DeliverySale(Base):
    __tablename__ = 'delivery_sales'
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('delivery_trips.id'))
    payment_mode = Column(String)
    amount = Column(Integer)
