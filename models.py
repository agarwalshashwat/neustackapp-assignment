from pydantic import BaseModel, Field
from typing import List, Optional

class Item(BaseModel):
    id: str
    name: str
    price: float

class CartItem(BaseModel):
    item_id: str
    quantity: int

class Cart(BaseModel):
    items: List[CartItem] = []
    discount_code: Optional[str] = None

class Order(BaseModel):
    id: str
    items: List[CartItem]
    total_amount: float
    discount_applied: float
    final_amount: float

class Stats(BaseModel):
    total_items_purchased: int
    total_purchase_amount: float
    discount_codes: List[str]
    total_discount_amount: float

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    discount_code: Optional[str] = None
