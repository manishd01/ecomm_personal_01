
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
# from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

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
    
    tracking_updates = relationship(
        "ShipmentTracking",
        back_populates="shipment",
        cascade="all, delete-orphan"
    )
    
    
    
    
class ShipmentTracking(Base):
    __tablename__ = "shipment_tracking"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), index=True)
    location = Column(String(255), nullable=False)     # ✅ FIXED
    status = Column(String(50), nullable=False)        # ✅ FIXED
    description = Column(String(255), nullable=True)  
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    # "Arrived at sorting center"
    lat = Column(String(50), nullable=True)          # optional (maps support)
    lng = Column(String(50), nullable=True)
    shipment = relationship("Shipment", back_populates="tracking_updates")