from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from app.core.base import Base

class OfficeCashDay(Base):
    __tablename__ = 'office_cash_day'
    date = Column(Date, primary_key=True)
    opening_cash = Column(Integer, default=0)
    cash_in = Column(Integer, default=0)
    cash_out = Column(Integer, default=0)
    closing_expected = Column(Integer, default=0)
    closing_counted = Column(Integer, default=0)
    difference = Column(Integer, default=0)
    status = Column(String, default='OPEN')  # OPEN / OK / SHORT / EXCESS
