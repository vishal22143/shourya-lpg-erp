from sqlalchemy import Column, Integer, String, Boolean
from app.core.base import Base

class AppUser(Base):
    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)   # ALWAYS '1234'
    active = Column(Boolean, default=True)
