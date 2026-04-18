from fastapi import HTTPException
from app.exceptions import OrderNotFoundError, ShipmentAlreadyExistsError
from app.models.shipping_model import Shipment, ShipmentTracking
from app.schemas.shipping_schema import TrackingCreate
from datetime import datetime, timedelta
import requests
from decouple import config

# ORDER_SERVICE_URL = config(
#     "ORDER_SERVICE_URL",
#     default="http://order-service:8000/api"
# )
ORDER_SERVICE_URL = "http://order-service:8000/api"
CUSTOMER_SERVICE_URL = "http://customer-service:8000/api"

# Valid status transitions

VALID_TRANSITIONS = {
    "CREATED": ["SHIPPED"],
    "SHIPPED": ["OUT_FOR_DELIVERY"],
    "OUT_FOR_DELIVERY": ["DELIVERED"],
    "DELIVERED": ["RETURNED", "REPLACED"]
}

# 👇 ADD THIS
VALID_TRACKING_STATUSES = [
    "IN_TRANSIT",
    "ARRIVED_AT_HUB",
    "DEPARTED_HUB",
    "OUT_FOR_DELIVERY",
    "DELIVERED"
]
# def add_tracking_update(shipment_id: int, data: TrackingCreate, db):
#     print(f"Adding tracking update for shipment {shipment_id}")
#     shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

#     if not shipment:
#         raise HTTPException(404, "Shipment not found")

#     tracking = ShipmentTracking(
#         shipment_id=shipment_id,
#         location=data.location,
#         status=data.status
#     )

#     db.add(tracking)
#     db.commit()
#     db.refresh(tracking)

#     return tracking





def generate_tracking_number():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def can_transition(current: str, new: str) -> bool:
    if current not in VALID_TRANSITIONS:
        return False
    return new in VALID_TRANSITIONS[current]


# =========================
# CREATE SHIPMENT
# =========================
def create_shipment_service(order_id: int, db):

    try:
        order_res = requests.get(
            f"{ORDER_SERVICE_URL}/orders/{order_id}",
            timeout=3
        )

        if order_res.status_code != 200:
            raise OrderNotFoundError()

    except requests.exceptions.RequestException:
        raise OrderNotFoundError()

    existing = db.query(Shipment).filter(
        Shipment.order_id == order_id
    ).first()

    if existing:
        raise ShipmentAlreadyExistsError()

    shipment = Shipment(
        order_id=order_id,
        status="CREATED"
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    return shipment


# =========================
# CITY + CARRIER LOGIC
# =========================
def assign_carrier_by_city(city: str) -> str:
    city = city.lower()

    carrier_map = {
        "delhi": "Delhivery",
        "mumbai": "BlueDart",
        "bangalore": "Ecom Express",
        "hyderabad": "DTDC",
        "chennai": "XpressBees",
        "kolkata": "Gati",
        "pune": "Shadowfax",
        "ahmedabad": "India Post",
        "jaipur": "FedEx",
        "lucknow": "DHL"
    }

    return carrier_map.get(city, "EKART")


def get_customer_city(order_id: int) -> str:
    order_res = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
    order = order_res.json()

    customer_id = order["customer_id"]

    customer_res = requests.get(
        f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}"
    )
    customer = customer_res.json()

    return customer.get("city", "").lower()

def get_shipment_service(shipment_id: int, db):
    return db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()

def add_tracking_update_service(shipment_id: int, data, db):

    shipment = db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()

    if not shipment:
        return None

    status = data.status.upper().strip()

    # 🔥 Validate tracking status
    if status not in VALID_TRACKING_STATUSES:
        raise HTTPException(400, "Invalid tracking status")

    # 🔥 Prevent duplicate spam (optional but good)
    last = db.query(ShipmentTracking)\
        .filter(ShipmentTracking.shipment_id == shipment_id)\
        .order_by(ShipmentTracking.timestamp.desc())\
        .first()

    if last and last.location == data.location and last.status == status:
        raise HTTPException(400, "Duplicate tracking update")

    # 🔥 Create tracking event
    tracking = ShipmentTracking(
        shipment_id=shipment_id,
        location=data.location,
        status=status,
        description=data.description,
    )

    db.add(tracking)

    # 🔥 Update shipment main status (only when needed)
    if status == "OUT_FOR_DELIVERY":
        shipment.status = "OUT_FOR_DELIVERY"

    elif status == "DELIVERED":
        shipment.status = "DELIVERED"
        shipment.delivered_at = datetime.utcnow()

    db.commit()
    db.refresh(tracking)

    return tracking

# =========================
# UPDATE STATUS
# =========================
def update_shipment_status_service(shipment_id: int, new_status: str, db):
    print(f"Updating shipment status for ID: {shipment_id}, New Status: {new_status}")
    try:
        shipment = db.query(Shipment).filter(
            Shipment.id == shipment_id
        ).first()

        if not shipment:
            return None

        new_status = new_status.upper()

        if not can_transition(shipment.status, new_status):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition from {shipment.status} to {new_status}"
            )

        # =========================
        # SPECIAL LOGIC
        # =========================

        if new_status == "SHIPPED":
            shipment.tracking_number = generate_tracking_number()

            city = get_customer_city(shipment.order_id)
            shipment.carrier = assign_carrier_by_city(city)

            shipment.estimated_delivery = datetime.utcnow() + timedelta(days=7)

        elif new_status == "DELIVERED":
            shipment.delivered_at = datetime.utcnow()

        # =========================
        # 🔥 ALWAYS UPDATE STATUS
        # =========================
        shipment.status = new_status

        db.commit()
        db.refresh(shipment)

        return shipment

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# READ OPERATIONS
# =========================
from sqlalchemy.orm import joinedload

def get_shipment_service(shipment_id: int, db):
    shipment = (
        db.query(Shipment)
        .options(joinedload(Shipment.tracking_updates))
        .filter(Shipment.id == shipment_id)
        .first()
    )

    if not shipment:
        return None

    # 🔥 Sort tracking timeline
    shipment.tracking_updates.sort(key=lambda x: x.timestamp)

    return shipment


def get_shipments_by_order_service(order_id: int, db):
    return db.query(Shipment).filter(
        Shipment.order_id == order_id
    ).all()

def list_shipments_service(db, status=None, search=None):
    query = db.query(Shipment)

    if status:
        query = query.filter(Shipment.status == status)

    if search:
        query = query.filter(Shipment.tracking_number.contains(search))

    return query.all()

# =========================
# NOTIFY ORDER SERVICE
# =========================
def notify_order_shipped(order_id: int):
    try:
        response = requests.post(
            f"{ORDER_SERVICE_URL}/orders/{order_id}/status",
            json={"status": "SHIPPED"},
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not notify Order Service: {str(e)}")
        return None




