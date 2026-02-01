from app.core.database import engine
from app.core.base import Base

from app.models import AppUser

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
