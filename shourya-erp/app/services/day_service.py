from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import ErpDay, DayStatus
from datetime import date, datetime


def get_or_create_today(db: Session, opened_by: int) -> ErpDay:
    today = date.today()
    day = db.query(ErpDay).filter(ErpDay.date == today).first()
    if not day:
        day = ErpDay(date=today, status=DayStatus.OPEN, opened_by=opened_by)
        db.add(day)
        db.commit()
        db.refresh(day)
    return day


def get_today(db: Session) -> ErpDay:
    return db.query(ErpDay).filter(ErpDay.date == date.today()).first()


def is_day_open(db: Session) -> bool:
    day = get_today(db)
    return day is not None and day.status == DayStatus.OPEN


def lock_day(db: Session, locked_by: int) -> ErpDay:
    day = get_today(db)
    if day and day.status == DayStatus.OPEN:
        day.status = DayStatus.LOCKED
        day.closed_by = locked_by
        day.closed_at = datetime.now()
        db.commit()
        db.refresh(day)
    return day
