from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.base import Base

class StaffAdvance(Base):
    __tablename__ = 'staff_advances'
    id = Column(Integer, primary_key=True)
    staff_type = Column(String)      # DELIVERY
    staff_id = Column(Integer)
    date = Column(Date)
    amount = Column(Integer)
    recovered = Column(Integer, default=0)
