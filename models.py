from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    id: str
    name: str
    price: float

class CartItem(BaseModel):
    item_id: str
    quantity: int

class CartResponse(BaseModel):
    cart_id: str
    items: List[CartItem]
    subtotal: float

class Order(BaseModel):
    id: str
    items: List[CartItem]
    total_amount: float
    discount_applied: float
    final_amount: float

class Stats(BaseModel):
    total_items_purchased: int
    total_revenue: float
    discount_codes: List[str]
    total_discount_amount: float

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    discount_code: Optional[str] = None
