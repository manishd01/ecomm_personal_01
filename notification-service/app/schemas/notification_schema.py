from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    customer_id: int = Field(..., gt=0)
    subject: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    notification_type: str = Field(..., min_length=1, max_length=100)
    order_id: Optional[int] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1, max_length=1000)
    is_read: Optional[int] = None


class NotificationResponse(NotificationBase):
    id: int
    is_read: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
