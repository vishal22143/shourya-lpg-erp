from sqlalchemy import Column, Integer, String, Date
from app.core.base import Base

class OfficeExpense(Base):
    __tablename__ = 'office_expenses'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    head = Column(String)        # Rent / Courier / Salary / Misc
    amount = Column(Integer)
    remark = Column(String)
