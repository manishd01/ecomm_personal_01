from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
import random
import string


def generate_tracking_number():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, nullable=False)

    status = Column(String(20), default="CREATED", nullable=False)

    # ✅ FIX
    tracking_number = Column(
        String(100), unique=True, nullable=True, default=generate_tracking_number
    )

    carrier = Column(String(50), nullable=True)

    estimated_delivery = Column(DateTime, nullable=True)

    delivered_at = Column(DateTime, nullable=True)

    # ✅ FUNCTION REFERENCE
    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    return_requested_at = Column(DateTime, nullable=True)

    returned_at = Column(DateTime, nullable=True)

    replacement_requested_at = Column(DateTime, nullable=True)

    replaced_at = Column(DateTime, nullable=True)

    tracking_updates = relationship(
        "ShipmentTracking", back_populates="shipment", cascade="all, delete-orphan"
    )


class ShipmentTracking(Base):
    __tablename__ = "shipment_tracking"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(Integer, ForeignKey("shipments.id"), index=True)

    event_type = Column(String(20), nullable=False, default="TRACKING")

    location = Column(String(255), nullable=True)

    status = Column(String(50), nullable=False)

    description = Column(String(255), nullable=True)

    # ✅ FUNCTION REFERENCE
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    lat = Column(String(50), nullable=True)

    lng = Column(String(50), nullable=True)

    shipment = relationship("Shipment", back_populates="tracking_updates")


# from app.database import Base
# from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
# # from app.database import Base
# from datetime import datetime
# from sqlalchemy.orm import relationship

# class Shipment(Base):
#     __tablename__ = "shipments"

#     id = Column(Integer, primary_key=True, index=True)

#     # 🔗 Relation
#     order_id = Column(Integer, nullable=False)

#     # 📦 Status lifecycle
#     status = Column(String(20), default="CREATED", nullable=False)
#     # CREATED → SHIPPED → DELIVERED

#     # 🚚 Shipping details
#     tracking_number = Column(String(100), unique=True, nullable=True)
#     carrier = Column(String(50), nullable=True)  # e.g., Delhivery, BlueDart

#     # 📅 Delivery info
#     estimated_delivery = Column(DateTime, nullable=True)
#     delivered_at = Column(DateTime, nullable=True)

#     # ⏱️ Timestamps
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(
#         DateTime,
#         server_default=func.now(),
#         onupdate=func.now()
#     )
#     return_requested_at = Column(DateTime, nullable=True)
#     returned_at = Column(DateTime, nullable=True)
#     replacement_requested_at = Column(DateTime, nullable=True)
#     replaced_at = Column(DateTime, nullable=True)
#     tracking_updates = relationship(
#         "ShipmentTracking",
#         back_populates="shipment",
#         cascade="all, delete-orphan"
#     )


# class ShipmentTracking(Base):
#     __tablename__ = "shipment_tracking"

#     id = Column(Integer, primary_key=True, index=True)
#     shipment_id = Column(Integer, ForeignKey("shipments.id"), index=True)
#     event_type = Column(String(20), nullable=False, default="TRACKING")
#     location = Column(String(255), nullable=True)     # ✅ FIXED
#     status = Column(String(50), nullable=False)        # ✅ FIXED
#     description = Column(String(255), nullable=True)
#     timestamp = Column(DateTime, default=datetime.utcnow, index=True)
#     # "Arrived at sorting center"
#     lat = Column(String(50), nullable=True)          # optional (maps support)
#     lng = Column(String(50), nullable=True)
#     shipment = relationship("Shipment", back_populates="tracking_updates")
