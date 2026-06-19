from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


def place_order(payload: OrderCreate, user: User, db: Session) -> Order:
    product = (
        db.query(Product).filter(Product.id == payload.product_id).first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {payload.product_id} not found",
        )
    if product.stock < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product.stock}",
        )

    total_price = product.price * payload.quantity
    product.stock -= payload.quantity

    order = Order(
        user_id=user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        total_price=total_price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_user_orders(user: User, db: Session) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user.id).all()
