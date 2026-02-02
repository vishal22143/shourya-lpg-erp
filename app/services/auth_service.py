from sqlalchemy.orm import Session
from app.models.user import User as AppUser

def authenticate(db: Session, login_id: str, password: str):
    user = db.query(AppUser).filter(
        AppUser.login_id == login_id,
        AppUser.active == True
    ).first()

    if not user:
        return None
    if user.password != password:
        return None

    return user
