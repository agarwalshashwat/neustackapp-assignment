# 🛡️ Insurance Store & Enrollment Predictor

This is a modern insurance ecommerce platform built with FastAPI, combining a checkout system with machine learning to predict customer enrollment behavior.

## ✨ Features
- **Digital Policy Store**: Browse insurance plans and add them to your cart.
- **Dynamic Discounts**: Automatic 10% discount codes generated for every $n$th order ($n=5$).
- **Admin Dashboard**: Real-time tracking of sales, items sold, and active discount codes.
- **ML Enrollment Predictor**: Predicts the likelihood of an employee enrolling in a policy based on demographic data.
- **Interactive UI**: Clean, responsive frontend with policy management and prediction tools.

## 🛠️ Setup & Installation

1. **Environment Setup**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **ML Pipeline (Data & Training)**:
   Generate the synthetic employee dataset (~10k rows) and train the Random Forest model:
   ```bash
   python generate_data.py
   python train_model.py
   ```

3. **Launch the Application**:
   ```bash
   python main.py
   ```
   Visit the platform at [http://localhost:8008](http://localhost:8008).

4. **Running Unit Tests**:
   ```bash
   pytest
   ```

## 🧠 Machine Learning Component
The project includes a predictive model to help the business understand enrollment drivers.
- **Model**: Random Forest Classifier.
- **Dataset**: `employee_data.csv` (features: age, salary, tenure, dependents, etc.).
- **Report**: See [report.md](report.md) for data insights and evaluation results.

## 📡 API Reference

### Store & ML APIs
- `GET /items`: List all available insurance policies.
- `POST /cart`: Initialize a new server-side cart.
- `POST /cart/{cart_id}/add`: Add items to a specific cart.
- `POST /checkout`: Process orders with optional discount codes.
- `POST /predict-enrollment`: Get ML-based enrollment probability.

### Admin APIs
- `POST /admin/generate-discount`: Generate a 10% discount code (available every $n$th order).
- `GET /admin/stats`: Get store performance statistics.

## 🛡️ Production Readiness
- **Thread Safety**: Uses threading locks to ensure consistency of in-memory stores during concurrent requests.
- **Logging**: Structured logging implemented for tracking transactions and errors.
- **Validation**: Strict Pydantic models for all request/response schemas.
- **Configuration**: interval ($n$) and discount percentage can be tuned via environment variables.
- **Testing**: Suite of unit tests covering the order lifecycle and discount logic.

### Admin APIs
- `POST /admin/generate-discount`: Manual triggers for code generation (per nth rules).
- `GET /admin/stats`: Business metrics and discount history.

## 📝 Assumptions
- For testing purposes, $n$ is set to 5.
- Store data is kept in-memory; restart clears history.
- The ML model is pre-trained and loaded on server startup.
