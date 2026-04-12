from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# 🔹 Base schema (common fields)
class ShipmentBase(BaseModel):
    order_id: int = Field(..., gt=0)
    status: str = Field(default="CREATED")


# 🔹 Create request
class CreateShipment(BaseModel):
    order_id: int = Field(..., gt=0)


# 🔹 Update request
class UpdateShipmentStatus(BaseModel):
    status: str = Field(..., min_length=1, max_length=50)


# 🔹 Response schema
class ShipmentResponse(ShipmentBase):
    id: int
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShipmentDetailResponse(ShipmentResponse):
    pass
