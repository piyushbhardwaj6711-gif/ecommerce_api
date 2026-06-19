from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.auth import get_current_user
from app.services import order as order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/place", response_model=OrderResponse, status_code=201)
def place_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Place a new order (authenticated users)."""
    return order_service.place_order(payload, current_user, db)


@router.get("/my-orders", response_model=list[OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all orders for the current user."""
    return order_service.get_user_orders(current_user, db)
