from sqlalchemy import Column, Integer, String, Date
from app.core.base import Base

class CashHandover(Base):
    __tablename__ = 'cash_handovers'
    id = Column(Integer, primary_key=True)
    source_type = Column(String)
    source_id = Column(Integer)
    amount = Column(Integer)
    payment_mode = Column(String)
    receiver_type = Column(String)
    receiver_name = Column(String)
    date = Column(Date)
