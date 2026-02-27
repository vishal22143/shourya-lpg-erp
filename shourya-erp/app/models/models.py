from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date,
    Text, ForeignKey, Enum, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


# ─── ENUMS ───────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    OWNER    = "OWNER"
    PARTNER  = "PARTNER"
    OFFICE   = "OFFICE"
    DELIVERY = "DELIVERY"
    LOADER   = "LOADER"   # loading/unloading staff (Sandip, Sagar, Ajinath)
    BDA      = "BDA"      # BDA owners who can log in to capture OTP & spot deliveries

class DayStatus(str, enum.Enum):
    OPEN   = "OPEN"
    LOCKED = "LOCKED"

class TripStatus(str, enum.Enum):
    OPEN   = "OPEN"
    CLOSED = "CLOSED"

class DeliveryStatus(str, enum.Enum):
    SCHEDULED   = "SCHEDULED"
    IN_TRIP     = "IN_TRIP"
    DELIVERED   = "DELIVERED"
    DELIVERED_EMERGENCY = "DELIVERED_EMERGENCY"   # no OTP
    NOT_DELIVERED = "NOT_DELIVERED"
    CANCELLED   = "CANCELLED"

class PaymentMode(str, enum.Enum):
    CASH    = "CASH"
    QR_CODE = "QR_CODE"       # QR Code Scan
    GPAY    = "GPAY"          # Google Pay
    PAYTM   = "PAYTM"         # Paytm
    ONLINE  = "ONLINE"        # Generic online / BPCL prepaid
    MIXED   = "MIXED"         # Cash + online partial payment
    PREPAID = "PREPAID"       # Advance payment via BPCL booking

class StockReason(str, enum.Enum):
    BPCL_RECEIPT    = "BPCL_RECEIPT"
    BPCL_RETURN     = "BPCL_RETURN"
    VEHICLE_ISSUE   = "VEHICLE_ISSUE"
    VEHICLE_RETURN  = "VEHICLE_RETURN"
    SALE            = "SALE"
    BDA_ISSUE       = "BDA_ISSUE"
    BDA_RETURN      = "BDA_RETURN"
    DEFECTIVE       = "DEFECTIVE"
    PHYSICAL_ADJUST = "PHYSICAL_ADJUST"

class CashReason(str, enum.Enum):
    SALE              = "SALE"
    BDA_HANDOVER      = "BDA_HANDOVER"
    EXPENSE           = "EXPENSE"
    ADVANCE           = "ADVANCE"
    OPENING           = "OPENING"
    ADJUSTMENT        = "ADJUSTMENT"
    SV_NEW_CONNECTION = "SV_NEW_CONNECTION"   # ₹4000 new connection
    BLUEBOOK_SALE     = "BLUEBOOK_SALE"       # ₹60 per blue book
    PIPE_SALE         = "PIPE_SALE"           # ₹190 Suraksha pipe
    DPR_SALE          = "DPR_SALE"            # DPR paid
    TERMINATION_VOUCHER = "TERMINATION_VOUCHER"
    NAME_CHANGE       = "NAME_CHANGE"         # customer pays us
    CYLINDER_5KG      = "CYLINDER_5KG"        # 5kg office sale
    DIESEL            = "DIESEL"
    SALARY            = "SALARY"


# ─── CORE TABLES ─────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True)
    name       = Column(String(100), nullable=False)
    mobile     = Column(String(15), unique=True, nullable=False)
    role       = Column(Enum(UserRole), nullable=False)
    pin_hash   = Column(String(200), nullable=False)
    is_active  = Column(Boolean, default=True)
    # wage rate per cylinder (for delivery staff)
    rate_urban  = Column(Float, default=0.0)
    rate_rural  = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())


class ErpDay(Base):
    __tablename__ = "erp_days"
    date       = Column(Date, primary_key=True)
    status     = Column(Enum(DayStatus), default=DayStatus.OPEN)
    opened_by  = Column(Integer, ForeignKey("users.id"))
    opened_at  = Column(DateTime, server_default=func.now())
    closed_by  = Column(Integer, ForeignKey("users.id"), nullable=True)
    closed_at  = Column(DateTime, nullable=True)


# ─── MASTER DATA ─────────────────────────────────────────────────────────────

class Vehicle(Base):
    __tablename__ = "vehicles"
    id           = Column(Integer, primary_key=True)
    name         = Column(String(50), nullable=False)   # e.g. "Tata 407"
    reg_number   = Column(String(20))
    capacity     = Column(Integer, default=55)
    extra_cap    = Column(Integer, default=10)
    default_driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active    = Column(Boolean, default=True)


class BdaMaster(Base):
    __tablename__ = "bda_master"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(100), nullable=False)   # e.g. "Shirol BDA"
    village     = Column(String(100))
    owner_name  = Column(String(100))
    mobile      = Column(String(15))
    max_allowed = Column(Integer, default=50)
    is_active   = Column(Boolean, default=True)


# ─── DELIVERY (CSV / SAP POOL) ────────────────────────────────────────────────

class DeliveryPool(Base):
    """CSV-imported delivery schedule from BPCL SAP"""
    __tablename__ = "delivery_pool"
    id              = Column(Integer, primary_key=True)
    erp_date        = Column(Date, nullable=False)
    consumer_no     = Column(String(30), nullable=False)
    consumer_name   = Column(String(200))
    address         = Column(Text)
    mobile          = Column(String(15))
    area            = Column(String(100))
    product_code    = Column(String(10), default="5350")
    booking_type    = Column(String(20))     # REGULAR, SV, PMUY
    status          = Column(Enum(DeliveryStatus), default=DeliveryStatus.SCHEDULED)
    trip_id         = Column(Integer, ForeignKey("trips.id"), nullable=True)
    lat             = Column(Float, nullable=True)
    lng             = Column(Float, nullable=True)
    otp             = Column(String(6), nullable=True)
    payment_mode    = Column(Enum(PaymentMode), nullable=True)
    amount_collected = Column(Float, nullable=True)
    delivered_by    = Column(Integer, ForeignKey("users.id"), nullable=True)
    delivered_at    = Column(DateTime, nullable=True)
    remarks         = Column(String(200), nullable=True)
    is_duplicate    = Column(Boolean, default=False)
    uploaded_at     = Column(DateTime, server_default=func.now())


# ─── TRIPS ───────────────────────────────────────────────────────────────────

class Trip(Base):
    __tablename__ = "trips"
    id              = Column(Integer, primary_key=True)
    erp_date        = Column(Date, nullable=False)
    delivery_man_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id      = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    status          = Column(Enum(TripStatus), default=TripStatus.OPEN)
    filled_issued   = Column(Integer, default=0)   # filled cylinders taken from godown
    empty_returned  = Column(Integer, default=0)   # empty cylinders returned to godown
    total_sales     = Column(Integer, default=0)
    cash_collected  = Column(Float, default=0.0)
    online_collected = Column(Float, default=0.0)
    bda_cash        = Column(Float, default=0.0)
    bda_online      = Column(Float, default=0.0)
    notes           = Column(Text, nullable=True)
    opened_at       = Column(DateTime, server_default=func.now())
    closed_at       = Column(DateTime, nullable=True)

    delivery_man    = relationship("User", foreign_keys=[delivery_man_id])
    vehicle         = relationship("Vehicle")
    deliveries      = relationship("DeliveryPool", back_populates=None, foreign_keys=[DeliveryPool.trip_id],
                                    primaryjoin="Trip.id == DeliveryPool.trip_id")


# ─── STOCK LEDGER (APPEND-ONLY TRUTH) ─────────────────────────────────────────

class StockLedger(Base):
    __tablename__ = "stock_ledger"
    id            = Column(Integer, primary_key=True)
    erp_date      = Column(Date, nullable=False)
    product_code  = Column(String(10), nullable=False)   # 5350, 5370, 5400, etc.
    location      = Column(String(50), nullable=False)   # GODOWN, VEHICLE_1, BDA_SHIROL, etc.
    qty           = Column(Integer, nullable=False)       # positive = IN, negative = OUT
    is_filled     = Column(Boolean, default=True)         # True = filled, False = empty
    reason        = Column(Enum(StockReason), nullable=False)
    ref_type      = Column(String(20), nullable=True)     # TRIP, OFFICE, BDA, BPCL
    ref_id        = Column(Integer, nullable=True)
    created_by    = Column(Integer, ForeignKey("users.id"))
    created_at    = Column(DateTime, server_default=func.now())
    notes         = Column(String(200), nullable=True)


class GodownPhysicalEntry(Base):
    """Blind physical stock count — append-only, never edited"""
    __tablename__ = "godown_physical_entries"
    id            = Column(Integer, primary_key=True)
    erp_date      = Column(Date, nullable=False)
    filled_14_2   = Column(Integer, default=0)
    empty_14_2    = Column(Integer, default=0)
    filled_19     = Column(Integer, default=0)
    empty_19      = Column(Integer, default=0)
    filled_5      = Column(Integer, default=0)
    empty_5       = Column(Integer, default=0)
    entered_by    = Column(Integer, ForeignKey("users.id"))
    entered_at    = Column(DateTime, server_default=func.now())
    notes         = Column(String(200), nullable=True)


# ─── CASH LEDGER (APPEND-ONLY TRUTH) ─────────────────────────────────────────

class CashLedger(Base):
    __tablename__ = "cash_ledger"
    id            = Column(Integer, primary_key=True)
    erp_date      = Column(Date, nullable=False)
    location      = Column(String(50), nullable=False)  # OFFICE, VEHICLE_1, etc.
    amount        = Column(Float, nullable=False)        # positive = IN, negative = OUT
    mode          = Column(Enum(PaymentMode), nullable=False)
    reason        = Column(Enum(CashReason), nullable=False)
    denomination  = Column(JSON, nullable=True)          # {500:2, 100:5, ...}
    ref_type      = Column(String(20), nullable=True)
    ref_id        = Column(Integer, nullable=True)
    actor_id      = Column(Integer, ForeignKey("users.id"))
    created_at    = Column(DateTime, server_default=func.now())
    notes         = Column(String(200), nullable=True)


# ─── BDA TRANSACTIONS ─────────────────────────────────────────────────────────

class BdaTransaction(Base):
    __tablename__ = "bda_transactions"
    id            = Column(Integer, primary_key=True)
    erp_date      = Column(Date, nullable=False)
    bda_id        = Column(Integer, ForeignKey("bda_master.id"), nullable=False)
    trip_id       = Column(Integer, ForeignKey("trips.id"), nullable=True)
    filled_issued = Column(Integer, default=0)
    empty_received = Column(Integer, default=0)
    cash_paid     = Column(Float, default=0.0)
    online_paid   = Column(Float, default=0.0)
    cash_receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by    = Column(Integer, ForeignKey("users.id"))
    created_at    = Column(DateTime, server_default=func.now())
    notes         = Column(String(200), nullable=True)

    bda           = relationship("BdaMaster")


# ─── OFFICE OPERATIONS ────────────────────────────────────────────────────────

class OfficeExpense(Base):
    __tablename__ = "office_expenses"
    id          = Column(Integer, primary_key=True)
    erp_date    = Column(Date, nullable=False)
    head        = Column(String(100), nullable=False)  # DIESEL, STATIONARY, etc.
    amount      = Column(Float, nullable=False)
    mode        = Column(Enum(PaymentMode), default=PaymentMode.CASH)
    paid_to     = Column(String(100), nullable=True)
    created_by  = Column(Integer, ForeignKey("users.id"))
    created_at  = Column(DateTime, server_default=func.now())
    notes       = Column(String(200), nullable=True)


class StaffAdvance(Base):
    __tablename__ = "staff_advances"
    id          = Column(Integer, primary_key=True)
    erp_date    = Column(Date, nullable=False)
    staff_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount      = Column(Float, nullable=False)    # positive = advance given, negative = recovery
    source      = Column(String(50), default="MANUAL")  # MANUAL, CASH_SHORT_ADJUSTMENT
    created_by  = Column(Integer, ForeignKey("users.id"))
    created_at  = Column(DateTime, server_default=func.now())
    notes       = Column(String(200), nullable=True)

    staff       = relationship("User", foreign_keys=[staff_id])


class OfficeStock(Base):
    """Blue book, Suraksha pipe, DPR stock — monthly tracked"""
    __tablename__ = "office_stock"
    id           = Column(Integer, primary_key=True)
    item_name    = Column(String(100), nullable=False)  # BLUE_BOOK, SURAKSHA_PIPE, DPR_14_2, DPR_5
    quantity     = Column(Integer, nullable=False)      # positive = stock in, negative = sold
    unit_price   = Column(Float, nullable=False)
    erp_date     = Column(Date, nullable=False)
    reason       = Column(String(50), nullable=False)   # OPENING, SALE, ADJUSTMENT
    created_by   = Column(Integer, ForeignKey("users.id"))
    created_at   = Column(DateTime, server_default=func.now())


# ─── WAGES ────────────────────────────────────────────────────────────────────

class WageEntry(Base):
    """Auto-computed wages — one entry per trip close"""
    __tablename__ = "wage_entries"
    id              = Column(Integer, primary_key=True)
    erp_date        = Column(Date, nullable=False)
    staff_id        = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id         = Column(Integer, ForeignKey("trips.id"), nullable=True)
    cylinders_urban = Column(Integer, default=0)
    cylinders_rural = Column(Integer, default=0)
    rate_urban      = Column(Float, default=5.0)
    rate_rural      = Column(Float, default=7.0)
    gross_wage      = Column(Float, default=0.0)
    advance_recovery = Column(Float, default=0.0)
    net_wage        = Column(Float, default=0.0)
    paid            = Column(Boolean, default=False)
    created_at      = Column(DateTime, server_default=func.now())

    staff           = relationship("User", foreign_keys=[staff_id])


# ─── BPCL MOVEMENT (entered by loader staff) ──────────────────────────────────

class BpclMovement(Base):
    __tablename__ = "bpcl_movements"
    id                = Column(Integer, primary_key=True)
    erp_date          = Column(Date, nullable=False)
    product_code      = Column(String(10), nullable=False)
    filled_received   = Column(Integer, default=0)
    empty_returned    = Column(Integer, default=0)
    entered_by        = Column(Integer, ForeignKey("users.id"))
    created_at        = Column(DateTime, server_default=func.now())
    notes             = Column(String(200), nullable=True)


# ─── ERP DAY END SNAPSHOT ─────────────────────────────────────────────────────

class DayEndSnapshot(Base):
    """Read-only day-end summary — generated at day close"""
    __tablename__ = "day_end_snapshots"
    id              = Column(Integer, primary_key=True)
    erp_date        = Column(Date, unique=True, nullable=False)
    snapshot_json   = Column(JSON, nullable=False)   # full day summary
    bpcl_data_json  = Column(JSON, nullable=True)    # BPCL SAP data for comparison
    created_by      = Column(Integer, ForeignKey("users.id"))
    created_at      = Column(DateTime, server_default=func.now())
