
from datetime import datetime
# from dataclasses import Field

from pydantic import BaseModel, Field
from typing import Optional
class DecreaseStockRequest(BaseModel):
    quantity: int = Field(..., gt=0)

# Request schema (POST/PUT)
class InventoryCreate(BaseModel):
    model_number: str
    product_name: str
    quantity: int
    
    price: float
    description: Optional[str] = None


class InventoryUpdate(BaseModel):
    model_number: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None


# Response schema
class InventoryResponse(BaseModel):
    id: int
    model_number: str
    product_name: str
    quantity: int
    price: float
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] 
    

    class Config:
        from_attributes = True   # ✅ important for SQLAlchemy