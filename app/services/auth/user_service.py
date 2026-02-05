from sqlalchemy.orm import Session
from app.models.auth import User
from app.services.auth.password_service import hash_password

def create_user(
    db: Session,
    username: str,
    password: str,
    role: str
):
    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    return user
