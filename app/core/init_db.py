from app.core.database import engine
from app.core.base import Base

# Core users & staff
from app.models.user import User
from app.models.delivery import DeliveryMan
from app.models.bda import BDA

# Stock system
from app.models.stock import StockMovement as StockLocation, StockOpening, StockMovement
from app.models.stock import StockMovement as StockDayEnd

# Delivery salary system (NEW)
from app.models.delivery_day_summary import DeliveryDaySummary
from app.models.delivery_cylinder_detail import DeliveryCylinderDetail
from app.models.delivery_payroll import DeliveryPayroll

# Cash & advances
from app.models.cash import CashHandover as OfficeCashDay
from app.models.cash import CashHandover as OfficeExpense
from app.models.staff_advance import StaffAdvance
from app.models.cash_denomination import CashDenomination

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
