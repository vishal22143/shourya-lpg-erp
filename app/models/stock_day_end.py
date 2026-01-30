from sqlalchemy import Column, Integer, Date, ForeignKey
from app.core.base import Base

class StockDayEnd(Base):
    __tablename__ = 'stock_day_end'
    date = Column(Date, primary_key=True)
    location_id = Column(Integer, ForeignKey('stock_locations.id'), primary_key=True)
    filled_qty = Column(Integer)
    empty_qty = Column(Integer)
