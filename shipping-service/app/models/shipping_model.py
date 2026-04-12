
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func
# from app.database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

    # 🔗 Relation
    order_id = Column(Integer, nullable=False)

    # 📦 Status lifecycle
    status = Column(String(20), default="CREATED", nullable=False)
    # CREATED → SHIPPED → DELIVERED

    # 🚚 Shipping details
    tracking_number = Column(String(100), unique=True, nullable=True)
    carrier = Column(String(50), nullable=True)  # e.g., Delhivery, BlueDart

    # 📅 Delivery info
    estimated_delivery = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    # ⏱️ Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )