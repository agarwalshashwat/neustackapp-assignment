# � Ecommerce Store API

A clean, high-performance ecommerce store backend built with FastAPI. This system handles cart management, checkouts, and a reward-based discount system.

## ✨ Features
- **Product Inventory**: Browse available products and add them to your cart.
- **Cart Management**: Server-side cart persistence using unique session IDs.
- **Dynamic Discount System**: Admins can generate 10% discount codes for every $n$th order ($n=5$ by default).
- **Admin Dashboard**: Real-time tracking of items sold, total revenue, and discount statistics.
- **Interactive UI**: Clean, responsive frontend dashboard to test all API functionalities.

## 🛠️ Setup & Installation

1. **Environment Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

2. **Launch the Application**:
   ```bash
   python main.py
   ```
   Visit the platform at [http://localhost:8008](http://localhost:8008).

### 🐳 Running with Docker

If you prefer to run the application in a containerized environment:

1. **Build the Image**:
   ```bash
   docker build -t ecommerce-store .
   ```

2. **Run the Container**:
   ```bash
   docker run -p 8008:8008 ecommerce-store
   ```

### 🛠️ Running with Docker Compose

For a more streamlined experience with environment configuration:

1. **Start the Service**:
   ```bash
   docker-compose up --build
   ```

The API will be available at [http://localhost:8008](http://localhost:8008).

3. **Running Unit Tests**:
   ```bash
   pytest
   ```

## 📡 API Reference

### Shopping APIs
- `GET /items`: List all available products in inventory.
- `POST /cart`: Initialize a new shopping cart.
- `POST /cart/{cart_id}/add`: Add items to a specific cart.
- `POST /checkout`: Process orders with optional discount codes.

### Admin APIs
- `POST /admin/generate-discount`: Generate a discount code (available for every $n$th order).
- `GET /admin/stats`: Get store performance statistics (revenue, items sold, etc.).

## 🛡️ Architecture & Design
- **Thread Safety**: Uses threading locks to ensure consistency of in-memory stores during concurrent requests.
- **Validation**: Strict Pydantic models for all request/response schemas.
- **Design Decisions**: Detailed architectural choices can be found in [DECISIONS.md](DECISIONS.md).

## 📝 Configuration
The following can be configured via environment variables:
- `DISCOUNT_ORDER_INTERVAL`: The order frequency ($n$) for discount eligibility (default: 5).
- `DISCOUNT_PERCENTAGE`: The discount value (default: 0.10 for 10%).
