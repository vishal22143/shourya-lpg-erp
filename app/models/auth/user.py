from sqlalchemy import Column, Integer, String, Boolean
from app.core.base import Base

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN / OWNER / OFFICE / ACCOUNTANT / DELIVERY
    active = Column(Boolean, default=True)
