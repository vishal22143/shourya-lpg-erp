from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/owner")
def owner_home():
    return RedirectResponse("/owner/s5")

@router.get("/office")
def office_home():
    return RedirectResponse("/office/s2")

@router.get("/godown")
def godown_home():
    return RedirectResponse("/godown/s3")

@router.get("/delivery")
def delivery_home():
    return RedirectResponse("/delivery/s4")
