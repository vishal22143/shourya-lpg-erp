from sqlalchemy import Column, Integer, String, Date
from app.core.base import Base

class DeliveryPayroll(Base):
    __tablename__ = 'delivery_payroll'

    id = Column(Integer, primary_key=True)
    delivery_man_id = Column(Integer, nullable=False)
    month = Column(String, nullable=False)          # YYYY-MM

    base_wage = Column(Integer, nullable=False)
    helper_days = Column(Integer, nullable=False)
    helper_amount = Column(Integer, nullable=False)
    gross = Column(Integer, nullable=False)

    advance_recovered = Column(Integer, nullable=False)
    net_paid = Column(Integer, nullable=False)

    payment_mode = Column(String, nullable=False)   # CASH / ONLINE
    payment_date = Column(Date, nullable=False)
