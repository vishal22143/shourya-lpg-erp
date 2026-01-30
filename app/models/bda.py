from sqlalchemy import Column, Integer, String, Boolean
from app.core.base import Base

class BDA(Base):
    __tablename__ = 'bdas'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    village = Column(String)
    active = Column(Boolean, default=True)
