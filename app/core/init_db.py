from app.core.database import engine
from app.core.base import Base

from app.models.user import User
from app.models.delivery import DeliveryMan
from app.models.delivery_transfer import DeliveryTransfer
from app.models.bda import BDA
from app.models.trip import DeliveryTrip, DeliverySale
from app.models.cash import CashHandover
from app.models.stock import StockLocation, StockOpening, StockMovement
from app.models.stock_day_end import StockDayEnd

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
