import pytest
from fastapi.testclient import TestClient
from main import app, orders, valid_discount_codes, used_discount_codes, carts

client = TestClient(app)

def setup_function():
    """Clear order history, carts and codes before each test."""
    orders.clear()
    valid_discount_codes.clear()
    used_discount_codes.clear()
    carts.clear()

def test_cart_apis():
    # Create cart
    res = client.post("/cart")
    assert res.status_code == 200
    cart_id = res.json()["cart_id"]
    
    # Add item (Wireless Headphones - price 150)
    res = client.post(f"/cart/{cart_id}/add", json={"item_id": "1", "quantity": 2})
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["subtotal"] == 300.0

def test_checkout_no_discount():
    payload = {
        "items": [{"item_id": "1", "quantity": 1}]
    }
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 150.0
    assert data["discount_applied"] == 0.0
    assert data["final_amount"] == 150.0

def test_discount_generation_logic():
    # Place 4 orders
    for _ in range(4):
        client.post("/checkout", json={"items": [{"item_id": "2", "quantity": 1}]})
    
    # Try to generate discount - should succeed for 5th (since current_orders is 4, 4+1=5 is mult of 5)
    response = client.post("/admin/generate-discount")
    assert response.status_code == 200
    assert "discount_code" in response.json()
    
    # Try again with different count - should fail if not multiple of 5
    client.post("/checkout", json={"items": [{"item_id": "2", "quantity": 1}]}) # order 5 placed
    response = client.post("/admin/generate-discount") # checking for order 6
    assert response.status_code == 400

def test_checkout_with_valid_discount():
    # Place 4 orders
    for _ in range(4):
        client.post("/checkout", json={"items": [{"item_id": "2", "quantity": 1}]})
    
    # Generate code
    gen_response = client.post("/admin/generate-discount")
    code = gen_response.json()["discount_code"]
    
    # Checkout with code
    payload = {
        "items": [{"item_id": "1", "quantity": 1}],
        "discount_code": code
    }
    response = client.post("/checkout", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["discount_applied"] == 15.0  # 10% of 150
    assert data["final_amount"] == 135.0

def test_admin_stats():
    # Place an order (Smart Watch - 250)
    client.post("/checkout", json={"items": [{"item_id": "2", "quantity": 2}]}) # 250 * 2 = 500
    
    response = client.get("/admin/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items_purchased"] == 2
    assert data["total_revenue"] == 500.0
