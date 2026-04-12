from fastapi import HTTPException
from app.exceptions import OrderNotFoundError, ShipmentAlreadyExistsError
from app.models.shipping_model import Shipment
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
def get_shipment_service(shipment_id: int, db):
    return db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()


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






# from fastapi import HTTPException
# from app.exceptions import OrderNotFoundError, ShipmentAlreadyExistsError
# from app.models.shipping_model import Shipment
# from datetime import datetime, timedelta
# import requests
# from decouple import config

# # ORDER_SERVICE_URL = config(
# #     "ORDER_SERVICE_URL",
# #     default="http://order-service:8000/api"
# # )
# ORDER_SERVICE_URL = "http://order-service:8000/api"
# CUSTOMER_SERVICE_URL = "http://customer-service:8000/api"

# # Valid status transitions
# VALID_TRANSITIONS = {
#     "CREATED": ["SHIPPED"],
#     "SHIPPED": ["DELIVERED"],
#     "DELIVERED": []
# }


# def generate_tracking_number():
#     """Generate a unique tracking number"""
#     import random
#     import string
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


# def can_transition(current: str, new: str) -> bool:
#     """Check if status transition is valid"""
#     if current not in VALID_TRANSITIONS:
#         return False
#     return new in VALID_TRANSITIONS[current]

# def create_shipment_service(order_id: int, db):
#     """Business logic only"""

#     # 1. Validate order exists
#     try:
#         order_res = requests.get(
#             f"{ORDER_SERVICE_URL}/orders/{order_id}",
#             timeout=3
#         )

#         if order_res.status_code != 200:
#             raise OrderNotFoundError()

#     except requests.exceptions.RequestException:
#         raise OrderNotFoundError()

#     # 2. Check duplicate shipment
#     existing = db.query(Shipment).filter(
#         Shipment.order_id == order_id
#     ).first()

#     if existing:
#         raise ShipmentAlreadyExistsError()

#     # 3. Create shipment
#     shipment = Shipment(
#         order_id=order_id,
#         status="CREATED"
#     )

#     db.add(shipment)
#     db.commit()
#     db.refresh(shipment)

#     return shipment

# def assign_carrier_by_city(city: str) -> str:
#     city = city.lower()

#     carrier_map = {
#         "delhi": "Delhivery",
#         "mumbai": "BlueDart",
#         "bangalore": "Ecom Express",
#         "hyderabad": "DTDC",
#         "chennai": "XpressBees",
#         "kolkata": "Gati",
#         "pune": "Shadowfax",
#         "ahmedabad": "India Post",
#         "jaipur": "FedEx",
#         "lucknow": "DHL"
#     }

#     return carrier_map.get(city, "EKART")  # default fallback


# def get_customer_city(order_id: int) -> str:
#     # 1️⃣ Get order
#     order_res = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
#     order = order_res.json()
#     print("got order", order, order_id)

#     customer_id = order["customer_id"]
    

#     # 2️⃣ Get customer
#     customer_res = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")
#     customer = customer_res.json()
#     print("got customer",customer)

#     return customer.get("city", "").lower()


# def update_shipment_status_service(shipment_id: int, new_status: str, db):
#     """Update shipment status with transition validation"""
#     try:
#         shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

#         if not shipment:
#             return None
        

#         if not can_transition(shipment.status, new_status):
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Invalid transition from {shipment.status} to {new_status}"
#             )

#         new_status = new_status.upper()
#         # Update tracking info when shipped
#         if new_status == "SHIPPED" and shipment.status != "SHIPPED":
#             shipment.status = new_status
#             shipment.tracking_number = generate_tracking_number()

#             # 🔥 Get city from services
#             city = get_customer_city(shipment.order_id)

#             # 🔥 Assign carrier
#             shipment.carrier = assign_carrier_by_city(city)

#             shipment.estimated_delivery = datetime.utcnow() + timedelta(days=7)
#             print("update status toshipped")
        
#         # Update delivery time
#         if new_status == "DELIVERED":
#             shipment.status = new_status
#             shipment.delivered_at = datetime.utcnow()

#         db.commit()
#         db.refresh(shipment)

#         return shipment

#     except HTTPException:
#         raise

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))


# def get_shipment_service(shipment_id: int, db):
#     """Retrieve a shipment by ID"""
#     try:
#         shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
#         return shipment

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def get_shipments_by_order_service(order_id: int, db):
#     """Get all shipments for an order"""
#     try:
#         shipments = db.query(Shipment).filter(Shipment.order_id == order_id).all()
#         return shipments

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def list_shipments_service(db):
#     """List all shipments"""
#     try:
#         data= db.query(Shipment).all()
#         return  data

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def notify_order_shipped(order_id: int):
#     """Notify Order Service that shipment is created"""
#     try:
#         response = requests.post(
#             f"{ORDER_SERVICE_URL}/orders/{order_id}/status",
#             json={"status": "SHIPPED"},
#             timeout=5
#         )
#         response.raise_for_status()
#         return response.json()

#     except requests.exceptions.RequestException as e:
#         print(f"Warning: Could not notify Order Service: {str(e)}")
#         # Don't fail the shipment creation if notification fails
#         return None

#         shipment.status = new_status
#         shipment.updated_at = datetime.utcnow()

#         db.commit()
#         db.refresh(shipment)

#         return shipment

#     except HTTPException:
#         raise

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         db.close()


# def get_shipment(shipment_id: int):
#     """Retrieve a shipment by ID"""
#     db = SessionLocal()

#     try:
#         shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

#         if not shipment:
#             raise HTTPException(status_code=404, detail="Shipment not found")

#         return shipment

#     finally:
#         db.close()


# def get_shipments_by_order(order_id: int):
#     """Get all shipments for an order"""
#     db = SessionLocal()

#     try:
#         shipments = db.query(Shipment).filter(Shipment.order_id == order_id).all()
#         return shipments

#     finally:
#         db.close()


# def notify_order_shipped(order_id: int):
#     """Notify Order Service that shipment is created"""
#     try:
#         response = requests.post(
#             f"{ORDER_SERVICE_URL}/orders/{order_id}/status",
#             json={"status": "SHIPPED"},
#             timeout=5
#         )
#         response.raise_for_status()
#         return response.json()

#     except requests.exceptions.RequestException as e:
#         print(f"Warning: Could not notify Order Service: {str(e)}")
#         # Don't fail the shipment creation if notification fails
#         return None
