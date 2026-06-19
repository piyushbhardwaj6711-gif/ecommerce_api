from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth, products, orders

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="A production-ready e-commerce REST API built with FastAPI and SQLite.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/", tags=["Health"])
def health_check():
    """Root endpoint – confirms the API is running."""
    return {"status": "ok", "message": "E-Commerce API is running"}
