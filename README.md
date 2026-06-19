# 🛒 E-Commerce REST API

A production-ready e-commerce REST API built with **FastAPI** and **SQLite**.

## Quick Start

```bash
cd ecommerce-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger UI.

## API Endpoints

### Auth
| Method | Endpoint         | Description           | Auth  |
|--------|------------------|-----------------------|-------|
| POST   | /auth/register   | Register a new user   | None  |
| POST   | /auth/login      | Login & get JWT token | None  |

### Products
| Method | Endpoint            | Description    | Auth       |
|--------|---------------------|----------------|------------|
| GET    | /products/          | List all       | None       |
| GET    | /products/search    | Search by name | None       |
| GET    | /products/{id}      | Get by ID      | None       |
| POST   | /products/          | Create         | Admin only |
| PUT    | /products/{id}      | Update         | Admin only |
| DELETE | /products/{id}      | Delete         | Admin only |

### Orders
| Method | Endpoint          | Description       | Auth     |
|--------|-------------------|-------------------|----------|
| POST   | /orders/place     | Place an order    | Required |
| GET    | /orders/my-orders | Get user's orders | Required |

## Make a User Admin

```python
# Run in Python shell inside venv
from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == "admin@example.com").first()
user.is_admin = True
db.commit()
```
