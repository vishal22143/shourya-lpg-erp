from fastapi import APIRouter, Depends
from app.core.database import SessionLocal
from app.services.day_end import run_day_end

router = APIRouter(prefix="/day-end", tags=["Day End"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/run")
def run_day_end_api(db=Depends(get_db)):
    result = run_day_end(db)
    db.commit()
    return result
