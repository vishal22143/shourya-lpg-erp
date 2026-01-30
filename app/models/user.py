from sqlalchemy import Column, Integer, String, Boolean
from app.core.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    active = Column(Boolean, default=True)
