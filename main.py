"""
Insurance Store & Enrollment Predictor API.

This module provides a FastAPI application for an insurance ecommerce platform,
including cart management, checkout with discount logic, and an ML-based 
enrollment prediction service.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional, Dict
import uuid
import os
import joblib
import pandas as pd
import logging
import threading
from models import Item, CartItem, Order, Stats, CheckoutRequest, EnrollmentPredictionRequest, EnrollmentPredictionResponse, CartResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Insurance Store API")

# Load ML Model
MODEL_PATH = "enrollment_model.joblib"
enrollment_model = None
if os.path.exists(MODEL_PATH):
    try:
        enrollment_model = joblib.load(MODEL_PATH)
        logger.info("ML Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load ML model: {e}")

# ... (rest of the file)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    """
    Serves the main frontend dashboard.
    
    Returns:
        FileResponse: The index.html content.
    """
    return FileResponse(os.path.join(static_dir, "index.html"))

# Configuration
N = int(os.getenv("DISCOUNT_ORDER_INTERVAL", 5))
DISCOUNT_PERCENTAGE = float(os.getenv("DISCOUNT_PERCENTAGE", 0.10))

# In-memory store
store_lock = threading.Lock()
inventory: Dict[str, Item] = {
    "1": Item(id="1", name="Life Insurance Plan", price=500.0),
    "2": Item(id="2", name="Health Insurance Premium", price=300.0),
    "3": Item(id="3", name="Car Insurance Policy", price=150.0),
    "4": Item(id="4", name="Travel Insurance Pack", price=50.0),
}

carts: Dict[str, List[CartItem]] = {}
orders: List[Order] = []
valid_discount_codes: List[str] = []
used_discount_codes: List[str] = []

# --- Store Helpers ---

def get_product_price(item_id: str) -> float:
    """
    Retrieves the price of a product from the inventory.

    Args:
        item_id (str): The unique identifier of the product.

    Returns:
        float: The price of the product.

    Raises:
        HTTPException: If the item is not found in inventory.
    """
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return inventory[item_id].price

# --- API Endpoints ---

@app.get("/items", response_model=List[Item])
async def list_items():
    """
    Lists all available insurance policies in the inventory.

    Returns:
        List[Item]: A list of available policy items.
    """
    return list(inventory.values())

# --- Cart APIs ---

@app.post("/cart", response_model=CartResponse)
async def create_cart():
    """
    Initializes a new server-side shopping cart.

    Returns:
        CartResponse: Details of the newly created empty cart.
    """
    cart_id = str(uuid.uuid4())
    with store_lock:
        carts[cart_id] = []
    logger.info(f"Created new cart with ID: {cart_id}")
    return CartResponse(cart_id=cart_id, items=[], subtotal=0.0)

@app.post("/cart/{cart_id}/add", response_model=CartResponse)
async def add_to_cart(cart_id: str, cart_item: CartItem):
    """
    Adds an insurance policy to a specific cart.

    Args:
        cart_id (str): The ID of the cart to modify.
        cart_item (CartItem): The item and quantity to add.

    Returns:
        CartResponse: The updated cart state.

    Raises:
        HTTPException: If the cart_id is invalid.
    """
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    price = get_product_price(cart_item.item_id)
    
    with store_lock:
        # Check if item already in cart
        found = False
        for item in carts[cart_id]:
            if item.item_id == cart_item.item_id:
                item.quantity += cart_item.quantity
                found = True
                break
        if not found:
            carts[cart_id].append(cart_item)
            
        subtotal = sum(get_product_price(i.item_id) * i.quantity for i in carts[cart_id])
        
    logger.info(f"Added item {cart_item.item_id} to cart {cart_id}")
    return CartResponse(cart_id=cart_id, items=carts[cart_id], subtotal=subtotal)

# --- Checkout API ---

@app.post("/checkout", response_model=Order)
async def checkout(request: CheckoutRequest):
    """
    Processes the checkout for a list of items and applies discounts if valid.

    Args:
        request (CheckoutRequest): Contains items and an optional discount code.

    Returns:
        Order: The finalized order details including totals and discounts.

    Raises:
        HTTPException: If the cart is empty or the discount code is invalid/used.
    """
    if not request.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    subtotal = 0.0
    for cart_item in request.items:
        price = get_product_price(cart_item.item_id)
        subtotal += price * cart_item.quantity

    discount_amount = 0.0
    with store_lock:
        if request.discount_code:
            if request.discount_code in valid_discount_codes:
                discount_amount = subtotal * DISCOUNT_PERCENTAGE
                valid_discount_codes.remove(request.discount_code)
                used_discount_codes.append(request.discount_code)
                logger.info(f"Applied discount code: {request.discount_code}")
            else:
                logger.warning(f"Invalid discount code attempt: {request.discount_code}")
                raise HTTPException(status_code=400, detail="Invalid or already used discount code")

        final_amount = subtotal - discount_amount
        
        order = Order(
            id=str(uuid.uuid4()),
            items=request.items,
            total_amount=subtotal,
            discount_applied=discount_amount,
            final_amount=final_amount
        )
        
        orders.append(order)
    
    logger.info(f"Order {order.id} placed successfully. Total: {final_amount}")
    return order

# --- Admin APIs ---

@app.post("/admin/generate-discount")
async def generate_discount():
    """
    Generates a new 10% discount code if the nth order condition is met.
    
    Condition: Current order count + 1 must be a multiple of N.
    A code can only be generated once for each interval and must be used
    before the next one is generated.

    Returns:
        Dict: A dictionary containing the new 'discount_code'.

    Raises:
        HTTPException: If the condition is not met or a code already exists.
    """
    with store_lock:
        current_orders_count = len(orders)
        already_generated_for_next = any(c.startswith(f"ORD-{current_orders_count + 1}") for c in valid_discount_codes)
        
        if (current_orders_count + 1) % N == 0 and not already_generated_for_next:
            if valid_discount_codes:
                raise HTTPException(
                    status_code=400,
                    detail="A discount code has already been generated and is waiting to be used."
                )

            new_code = f"DISCOUNT-{uuid.uuid4().hex[:6].upper()}"
            valid_discount_codes.append(new_code)
            logger.info(f"Generated new discount code: {new_code}")
            return {"discount_code": new_code}
        else:
            if (current_orders_count + 1) % N != 0:
                detail = f"Discount code can only be generated for every {N}th order. Current order count is {current_orders_count}."
            else:
                detail = "Discount code already generated for the upcoming eligible order."
            
            logger.info("Discount generation rejected: condition not met.")
            raise HTTPException(status_code=400, detail=detail)

@app.get("/admin/stats", response_model=Stats)
async def get_stats():
    """
    Retrieves store-wide statistics for administration.

    Returns:
        Stats: Aggregated metrics including total items sold and total discounts.
    """
    with store_lock:
        total_items = 0
        total_amount = 0.0
        total_discount = 0.0
        
        for order in orders:
            for item in order.items:
                total_items += item.quantity
            total_amount += order.total_amount
            total_discount += order.discount_applied
            
        stats = Stats(
            total_items_purchased=total_items,
            total_purchase_amount=total_amount,
            discount_codes=used_discount_codes + valid_discount_codes,
            total_discount_amount=total_discount
        )
    return stats

# --- ML APIs ---

@app.post("/predict-enrollment", response_model=EnrollmentPredictionResponse)
async def predict_enrollment(request: EnrollmentPredictionRequest):
    """
    Predicts the likelihood of an employee enrolling in an insurance policy.

    Uses a trained Random Forest model to predict enrollment probability 
    based on demographic and employment features.

    Args:
        request (EnrollmentPredictionRequest): Employee demographic data.

    Returns:
        EnrollmentPredictionResponse: Probability and binary prediction result.

    Raises:
        HTTPException: If the ML model is unavailable or prediction fails.
    """
    if enrollment_model is None:
        raise HTTPException(status_code=503, detail="ML Model not available. Please train the model first.")
    
    # Convert request to DataFrame for the pipeline
    data = pd.DataFrame([request.model_dump()])
    
    try:
        prob = enrollment_model.predict_proba(data)[0][1]
        prediction = bool(enrollment_model.predict(data)[0])
        return EnrollmentPredictionResponse(
            enrolled_probability=round(prob, 4),
            will_enroll=prediction
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
