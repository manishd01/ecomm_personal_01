from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    model_number = Column(String(100), unique=True, nullable=False, index=True)  # 🔥 NEW
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
