from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.auth import require_admin
from app.services import product as product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Retrieve all products."""
    return product_service.list_products(db)


@router.get("/search", response_model=list[ProductResponse])
def search_products(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """Search products by name (case-insensitive partial match)."""
    return product_service.search_products(name, db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by ID."""
    return product_service.get_product(product_id, db)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Create a new product (admin only)."""
    return product_service.create_product(payload, db)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Update an existing product (admin only)."""
    return product_service.update_product(product_id, payload, db)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Delete a product (admin only)."""
    product_service.delete_product(product_id, db)
