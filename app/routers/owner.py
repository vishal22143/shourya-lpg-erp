from fastapi import APIRouter

router = APIRouter(prefix="/owner", tags=["Owner"])

@router.post("/delivery-man/add")
def add_delivery_man(name: str, mobile: str):
    return {"status": "delivery man added", "name": name}

@router.post("/delivery-man/deactivate")
def deactivate_delivery_man(delivery_man_id: int):
    return {"status": "delivery man deactivated", "id": delivery_man_id}

@router.get("/delivery-man/list")
def list_delivery_men():
    return {"status": "list"}
