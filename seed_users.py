from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

users = [
    {'username': '7887456789', 'role': 'OWNER'},
    {'username': '9000000001', 'role': 'PARTNER'},
    {'username': '9000000002', 'role': 'OFFICE'},
    {'username': '9000000003', 'role': 'ACCOUNTS'},
    {'username': '9000000004', 'role': 'DELIVERY'},
    {'username': '9000000005', 'role': 'DELIVERY'},
    {'username': '9000000006', 'role': 'BDA'},
]

for u in users:
    existing = db.query(User).filter(User.username == u['username']).first()
    if not existing:
        db.add(User(
            username=u['username'],
            role=u['role'],
            active=True
        ))

db.commit()
db.close()

print('USER SEEDING DONE')
