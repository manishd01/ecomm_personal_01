from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict



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
    location: Optional[str] = None


# 🔹 Response schema
class ShipmentResponse(ShipmentBase):
    id: int
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    # ✅ ADD ALL 4 FIELDS
    return_requested_at: Optional[datetime]
    returned_at: Optional[datetime]
    replacement_requested_at: Optional[datetime]
    replaced_at: Optional[datetime]


    

    class Config:
        from_attributes = True





# // tracking schemaa
class TrackingCreate(BaseModel):
    location: str
    status: str
    description: Optional[str] = None
    lat: Optional[str] = None
    lng: Optional[str] = None

class TrackingResponse(BaseModel):
    id: int
    location: Optional[str] = ""
    status: str
    timestamp: datetime
    description: Optional[str] = None
    lat: Optional[str] = None
    lng: Optional[str] = None

    class Config:
        from_attributes = True
        
class ShipmentDetailResponse(ShipmentResponse):
    tracking_updates: list[TrackingResponse] = []
      # ✅ ADD THIS
    allowed_actions: list = []

    