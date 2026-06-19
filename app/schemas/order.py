from pydantic import BaseModel, Field
from datetime import datetime


# ── Request Schemas ──────────────────────────────────────────────

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


# ── Response Schemas ─────────────────────────────────────────────

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
