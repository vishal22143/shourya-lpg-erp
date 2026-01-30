from sqlalchemy import Column, Integer, Date
from app.core.base import Base

class CashDenomination(Base):
    __tablename__ = 'cash_denominations'
    date = Column(Date, primary_key=True)
    n2000 = Column(Integer, default=0)
    n500  = Column(Integer, default=0)
    n200  = Column(Integer, default=0)
    n100  = Column(Integer, default=0)
    n50   = Column(Integer, default=0)
    n20   = Column(Integer, default=0)
    n10   = Column(Integer, default=0)
    coins = Column(Integer, default=0)
