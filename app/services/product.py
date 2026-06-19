from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def get_product(product_id: int, db: Session) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return product


def search_products(name: str, db: Session) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.name.ilike(f"%{name}%"))
        .all()
    )


def create_product(payload: ProductCreate, db: Session) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    product_id: int, payload: ProductUpdate, db: Session
) -> Product:
    product = get_product(product_id, db)
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(product_id: int, db: Session) -> None:
    product = get_product(product_id, db)
    db.delete(product)
    db.commit()
