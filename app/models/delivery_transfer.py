from sqlalchemy import Column, Integer, ForeignKey, Date
from app.core.base import Base

class DeliveryTransfer(Base):
    __tablename__ = "delivery_transfers"

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("delivery_trips.id"), nullable=False)
    to_location_id = Column(Integer, ForeignKey("stock_locations.id"), nullable=False)

    filled_qty = Column(Integer, default=0)
    empty_qty = Column(Integer, default=0)

    date = Column(Date, nullable=False)
