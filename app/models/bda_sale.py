from sqlalchemy import Column, Integer, Date, ForeignKey, Numeric
from app.core.base import Base

class BDASale(Base):
    __tablename__ = 'bda_sales'

    id = Column(Integer, primary_key=True, index=True)
    bda_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    filled_out = Column(Integer, default=0)
    empty_in = Column(Integer, default=0)
    cash_collected = Column(Numeric(10,2), default=0)
