from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.auth_service import authenticate

router = APIRouter()

@router.post('/login')
def login(login_id: str, password: str, db: Session = Depends(get_db)):
    user = authenticate(db, login_id, password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid login')

    return {
        'login_id': user.login_id,
        'name': user.name,
        'role': user.role
    }
