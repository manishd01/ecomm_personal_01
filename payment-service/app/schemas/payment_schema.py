from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):
    order_id: int = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., min_length=1, max_length=100)
    status: str   # ✅ must exist

class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    payment_method: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = None
    transaction_id: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int
    status: str
    transaction_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
