from app.core.database import SessionLocal
from app.models.app_user import AppUser

db = SessionLocal()

users = [
    ("9999999999", "Owner", "OWNER"),
    ("8888888888", "MM Madam", "PARTNER"),
    ("7777777777", "Office", "OFFICE"),
    ("6666666666", "Accounts", "ACCOUNTS"),
    ("5555555555", "Delivery", "DELIVERY"),
    ("4444444444", "BDA", "BDA"),
]

for login_id, name, role in users:
    if not db.query(AppUser).filter(AppUser.login_id == login_id).first():
        db.add(AppUser(
            login_id=login_id,
            name=name,
            role=role,
            password="1234",
            active=True
        ))

db.commit()
db.close()
print("ALL TRIAL USERS CREATED (INCLUDING MM Madam)")
