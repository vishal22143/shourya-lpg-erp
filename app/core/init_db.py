from app.core.database import engine
from app.core.base import Base

from app.models.delivery_day_summary import DeliveryDaySummary
from app.models.delivery_cylinder_detail import DeliveryCylinderDetail
from app.models.delivery_payroll import DeliveryPayroll

from app.models.office_cash import OfficeCashDay
from app.models.office_expense import OfficeExpense
from app.models.staff_advance import StaffAdvance
from app.models.cash_denomination import CashDenomination

from app.models.salary_master import SalaryMaster
from app.models.salary_payment import SalaryPayment

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
