from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union

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

class EnrollmentPredictionRequest(BaseModel):
    age: int
    gender: str
    marital_status: str
    salary: float
    employment_type: str
    region: str
    has_dependents: Union[str, int, bool]
    tenure_years: float

    @field_validator('has_dependents', mode='before')
    @classmethod
    def validate_has_dependents(cls, v):
        if isinstance(v, bool):
            return "Yes" if v else "No"
        if isinstance(v, int):
            return "Yes" if v == 1 else "No"
        if isinstance(v, str):
            if str(v).lower() in ("yes", "1", "true"):
                return "Yes"
            if str(v).lower() in ("no", "0", "false"):
                return "No"
        return v

class EnrollmentPredictionResponse(BaseModel):
    enrolled_probability: float
    will_enroll: bool
