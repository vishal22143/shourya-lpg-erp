from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.base import Base

class StockLocation(Base):
    __tablename__ = 'stock_locations'
    id = Column(Integer, primary_key=True)
    location_type = Column(String)
    ref_id = Column(Integer)

class StockOpening(Base):
    __tablename__ = 'stock_opening'
    date = Column(Date, primary_key=True)
    location_id = Column(Integer, ForeignKey('stock_locations.id'), primary_key=True)
    filled_qty = Column(Integer, default=0)
    empty_qty = Column(Integer, default=0)

class StockMovement(Base):
    __tablename__ = 'stock_movements'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    from_location = Column(Integer)
    to_location = Column(Integer)
    filled_qty = Column(Integer)
    empty_qty = Column(Integer)
    reason = Column(String)
    ref_type = Column(String)
    ref_id = Column(Integer)
