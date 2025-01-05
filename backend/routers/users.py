from fastapi import APIRouter

router = APIRouter(prefix="/items")

@router.get("")
def get_items():
    return {"message": "Get all items"}

@router.post("")
def add_item(name: str, quantity: int = 0, price: float = 0.0):
    return {"message": f"Item '{name}' added with quantity {quantity} and price {price}"}   