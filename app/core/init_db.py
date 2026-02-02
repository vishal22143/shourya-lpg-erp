from app.core.database import engine
from app.core.base import Base

# Core users & staff
from app.models.user import User
from app.models import DeliveryMan
from app.models.bda import BDA

# Stock system
from app.models.stock import StockMovement as StockLocation, StockOpening, StockMovement
from app.models.stock import StockMovement as StockDayEnd

# Delivery salary system (NEW)
from app.models import DeliveryDaySummary
from app.models import DeliveryCylinderDetail
from app.models import DeliveryPayroll

# Cash & advances
from app.models.cash import CashHandover as OfficeCashDay
from app.models.cash import CashHandover as OfficeExpense
from app.models import StaffAdvance
from app.models import CashDenomination

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
