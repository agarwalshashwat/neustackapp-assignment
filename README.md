# Ecommerce Store Assignment

This is a simple ecommerce store implementation with FastAPI and an in-memory store.

## Features
- List items and add to cart.
- Checkout with optional discount code.
- Admin API to generate discount codes for every $n$th order (default is $n=5$).
- Admin API to view store statistics.
- Simple HTML/JS frontend.

## Setup

1. **Install dependencies and run**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   uv run python main.py
   ```
   The application will be available at [http://localhost:8008](http://localhost:8008).

2. **Running Tests**:
   ```bash
   pytest
   ```

## APIs

### Store APIs
- `GET /items`: List all available items.
- `POST /checkout`: Place an order. Accepts a list of item IDs, quantities, and an optional discount code.

### Admin APIs
- `POST /admin/generate-discount`: Generates a 10% discount code if the next order is an $n$th order.
- `GET /admin/stats`: Get summary of total items, total amount, discount codes, and discount amounts.

## Assumptions
- In-memory storage is used; data resets on server restart.
- $N$ is set to 5 by default in `main.py`.
- Discount code applies 10% to the entire order.
- Each generated discount code can only be used once.
