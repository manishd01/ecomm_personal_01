from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, index=True)
    customer_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(100), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    transaction_id = Column(String(255), nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),onupdate=func.now())
