from app.core.database import engine
from app.core.base import Base

# Core users & staff
from app.models import User
from app.models import DeliveryMan
from app.models import BDA

# Stock system
from app.models import StockLocation, StockOpening, StockMovement
from app.models import StockDayEnd

# Delivery salary system (NEW)
from app.models import DeliveryDaySummary
from app.models import DeliveryCylinderDetail
from app.models import DeliveryPayroll

# Cash & advances
from app.models import OfficeCashDay
from app.models import OfficeExpense
from app.models import StaffAdvance
from app.models import CashDenomination

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
