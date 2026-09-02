from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# 🔹 Base schema (common fields)
class OrderBase(BaseModel):
    customer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


# 🔹 Create request
class OrderCreate(OrderBase):
    pass


# 🔹 Update request (all optional)
class OrderUpdate(BaseModel):
    customer_id: Optional[int] = Field(None, gt=0)
    product_id: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str]


# 🔹 Response schema
class OrderResponse(OrderBase):
    order_number: str
    total_price: float
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # 🔥 important for SQLAlchemy
