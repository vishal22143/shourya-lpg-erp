from sqlalchemy.orm import Session
from app.models.auth import User
from app.services.auth.password_service import hash_password

def bootstrap_admin(db: Session, username: str, password: str):
    """
    Creates ADMIN user only if no users exist.
    One-time operation.
    """

    if db.query(User).count() > 0:
        raise Exception("Admin already initialized")

    admin = User(
        username=username,
        password_hash=hash_password(password),
        role="ADMIN"
    )

    db.add(admin)
    db.commit()
    return admin
