from typing import Optional

from fastapi import HTTPException
from app.exceptions import OrderNotFoundError, ShipmentAlreadyExistsError
from app.models.shipping_model import Shipment, ShipmentTracking
from app.schemas.shipping_schema import TrackingCreate
from datetime import datetime, timedelta
import requests
from decouple import config
from app.kafka_producer import send_event   #kafka  thing


# ORDER_SERVICE_URL = config(
#     "ORDER_SERVICE_URL",
#     default="http://order-service:8000/api"
# )
ORDER_SERVICE_URL = "http://order-service:8000/api"
CUSTOMER_SERVICE_URL = "http://customer-service:8000/api"

# VALID_TRANSITIONS = {
#     "CREATED": [
#         {"type": "STATUS", "value": "SHIPPED"}
#     ],

#     # 🚚 after shipped → ONLY tracking
#     "SHIPPED": [
#         {"type": "TRACKING"}
#     ],

#     "IN_TRANSIT": [
#         {"type": "TRACKING"}
#     ],

#     "OUT_FOR_DELIVERY": [
#         {"type": "TRACKING"}
#     ],

#     "DELIVERED": [
#         {"type": "STATUS", "value": "RETURN_REQUESTED"},
#         {"type": "STATUS", "value": "REPLACEMENT_REQUESTED"}
#     ],

#     "RETURN_REQUESTED": [
#         {"type": "STATUS", "value": "RETURNED"}
#     ],

#     "REPLACEMENT_REQUESTED": [
#         {"type": "STATUS", "value": "REPLACED"}
#     ],

#     "RETURNED": [],
#     "REPLACED": []
# }

# Valid status transitions
VALID_TRANSITIONS = {
    "CREATED": [
        {"type": "STATUS", "value": "SHIPPED"}
    ],

    # 🚚 After shipped → allow tracking + move to transit
    "SHIPPED": [
        {"type": "STATUS", "value": "IN_TRANSIT"},
        {"type": "TRACKING", "label": "📍 Add Tracking Update"}
    ],

    # 📦 In transit → allow tracking + next step
    "IN_TRANSIT": [
        {"type": "STATUS", "value": "OUT_FOR_DELIVERY"},
        {"type": "TRACKING", "label": "📍 Add Tracking Update"}
    ],

    # 🚪 Out for delivery → allow tracking + delivery
    "OUT_FOR_DELIVERY": [
        {"type": "STATUS", "value": "DELIVERED"},
        {"type": "TRACKING", "label": "📍 Add Tracking Update"}
    ],

    # ✅ Delivered → no tracking, only business flows
    "DELIVERED": [
        {"type": "STATUS", "value": "RETURN_REQUESTED"},
        {"type": "STATUS", "value": "REPLACEMENT_REQUESTED"}
    ],

    "RETURN_REQUESTED": [
        {"type": "STATUS", "value": "RETURNED"}
    ],

    "REPLACEMENT_REQUESTED": [
        {"type": "STATUS", "value": "REPLACED"}
    ],

    "RETURNED": [],
    "REPLACED": []
}

# 👇 ADD THIS
VALID_TRACKING_STATUSES = [
    "IN_TRANSIT",
    "ARRIVED_AT_HUB",
    "DEPARTED_HUB",
    "OUT_FOR_DELIVERY",
    "DELIVERED"
]






def generate_tracking_number():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def can_transition(current: str, new: str) -> bool:
    if current not in VALID_TRANSITIONS:
        return False

    actions = VALID_TRANSITIONS[current]

    # ✅ extract only STATUS transitions
    allowed_values = [
        action["value"]
        for action in actions
        if action.get("type") == "STATUS"
    ]

    return new in allowed_values


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



def list_shipments_service(db, status=None, search=None):
    query = db.query(Shipment)

    if status:
        query = query.filter(Shipment.status == status)

    if search:
        query = query.filter(Shipment.tracking_number.contains(search))

    shipments = query.all()

    # ✅ ADD THIS LOOP
    for s in shipments: 
        s.allowed_actions = VALID_TRANSITIONS.get(s.status, [])

    return shipments 

def get_customer_city(order_id: int) -> str:
    order_res = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
    order = order_res.json()

    customer_id = order["customer_id"]

    customer_res = requests.get(
        f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}"
    )
    customer = customer_res.json()

    return customer.get("city", "").lower()

def update_shipment_status_service(shipment_id: int, new_status: str, db, location: Optional[str] = None):
    print("🔵 STEP 0: Function called")
    print(f"➡️ Shipment ID: {shipment_id}, Incoming Status: {new_status}")

    try:
        print("🔵 STEP 1: Fetching shipment from DB") 
        shipment = db.query(Shipment).filter(
            Shipment.id == shipment_id
        ).first()

        if not shipment:
            print("❌ STEP FAIL: Shipment not found")
            return None

        print(f"✅ STEP 2: Shipment found with current status: {shipment.status}")

        new_status = new_status.upper().strip()
        print(f"🔵 STEP 3: Normalized new status: {new_status}")

        print("🔵 STEP 4: Checking transition validity")
        if not can_transition(shipment.status, new_status):
            print(f"❌ STEP FAIL: Invalid transition {shipment.status} → {new_status}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition from {shipment.status} to {new_status}"
            )

        print("✅ STEP 5: Transition valid")

        # ✅ UPDATE STATUS
        print("🔵 STEP 6: Updating shipment status")
        shipment.status = new_status

        # ✅ ADD STATUS TRACKING EVENT
        print("🔵 STEP 7: Creating status tracking entry")
        tracking = ShipmentTracking(
            shipment_id=shipment.id,
            status=new_status,
            description=f"Status changed to {new_status}",
            event_type="STATUS_UPDATE",
            timestamp=datetime.utcnow(),
            location=location
        )
        db.add(tracking)
        print("✅ STEP 8: Tracking entry created")
        # =========================
        # BUSINESS LOGIC (UNCHANGED)
        # =========================
        if new_status == "SHIPPED":
            shipment.tracking_number = generate_tracking_number()

            city = get_customer_city(shipment.order_id)
            shipment.carrier = assign_carrier_by_city(city)

            shipment.estimated_delivery = datetime.utcnow() + timedelta(days=7)

        elif new_status == "DELIVERED":
            shipment.delivered_at = datetime.utcnow()
<<<<<<< HEAD
            
            print(f"   ➤ Delivered at: {shipment.delivered_at}")
=======

>>>>>>> abbe713be65c4a56ee72873fbf22dcbe9a8a4f01
        elif new_status == "RETURN_REQUESTED":
            shipment.return_requested_at = datetime.utcnow()
            

        elif new_status == "RETURNED":
            shipment.returned_at = datetime.utcnow()

        elif new_status == "REPLACEMENT_REQUESTED":
            shipment.replacement_requested_at = datetime.utcnow()

        elif new_status == "REPLACED":
            shipment.replaced_at = datetime.utcnow()

        # ❌ NO COMMIT HERE (IMPORTANT FIX)

        # Kafka (keep after commit ideally, but keeping your logic)
        try:
            send_event("shipment-events", {
                "event": "SHIPMENT_STATUS_UPDATED",
                "data": {
                    "shipment_id": shipment.id,
                    "order_id": shipment.order_id,
                    "status": shipment.status,
                    "carrier": shipment.carrier,
                    "tracking_number": shipment.tracking_number,
                    "timestamp": str(datetime.utcnow())
                }
            })
        except Exception as e:
            print("⚠️ Kafka failed but DB is OK:", str(e))

<<<<<<< HEAD
        print("🔵 STEP 9: Committing to DB")
        db.commit()

        print("✅ STEP 10: Commit successful")

        print("🔵 STEP 11: Refreshing object")
        db.refresh(shipment)
    #       kakfa event produceL:
    # 🔥 SEND EVENT AFTER COMMIT
        try:
            send_event("shipment-events", {
                "event": "SHIPMENT_STATUS_UPDATED",
                "data": {
                    "shipment_id": shipment.id,
                    "order_id": shipment.order_id,
                    "status": shipment.status,
                    "carrier": shipment.carrier,
                    "tracking_number": shipment.tracking_number,
                    "timestamp": str(datetime.utcnow())
                }
            })
        except Exception as e:
            print("⚠️ Kafka failed but DB is OK:", str(e))
        print("✅ STEP 12: Returning updated shipment")
=======
>>>>>>> abbe713be65c4a56ee72873fbf22dcbe9a8a4f01
        shipment.allowed_actions = VALID_TRANSITIONS.get(shipment.status, [])

        return shipment

    except HTTPException as http_err:
        print(f"⚠️ HTTPException occurred: {http_err.detail}")
        raise

    except Exception as e:
        print("🔥 STEP ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

def add_tracking_update_service(shipment_id: int, data, db, location: Optional[str] = None):

    shipment = db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()

    if not shipment:
        return None

    status = (data.status or "IN_TRANSIT").upper().strip()

    if status not in VALID_TRACKING_STATUSES:
        raise HTTPException(400, "Invalid tracking status")

    last = db.query(ShipmentTracking)\
        .filter(ShipmentTracking.shipment_id == shipment_id)\
        .order_by(ShipmentTracking.timestamp.desc())\
        .first()

    if last and last.location == data.location and last.status == status:
        raise HTTPException(400, "Duplicate tracking update")

    print("🔵 STEP A: Creating tracking entry")

    # =========================
    # 1️⃣ FIRST: UPDATE SHIPMENT STATUS (ONLY IF VALID)
    # =========================
    if can_transition(shipment.status, status):
        print(f"✅ Updating shipment status: {shipment.status} → {status}")
        shipment.status = status

        if status == "DELIVERED":
            shipment.delivered_at = datetime.utcnow()
        elif status == "RETURNED":
            shipment.returned_at = datetime.utcnow()

    # =========================
    # 2️⃣ THEN: CREATE TRACKING ENTRY (ONCE ONLY)
    # =========================
    tracking = ShipmentTracking(
        shipment_id=shipment_id,
        location=data.location,
        status=status,
        description=data.description,
        event_type="TRACKING_UPDATE",
        timestamp=datetime.utcnow()
    )

    db.add(tracking)

    # =========================
    # 3️⃣ COMMIT ONCE HERE (IMPORTANT FIX)
    # =========================
    db.commit()
    db.refresh(tracking)
    db.refresh(shipment)

    return tracking

# def add_tracking_update_service(shipment_id: int, data, db, location: Optional[str] = None):

#     shipment = db.query(Shipment).filter(
#         Shipment.id == shipment_id
#     ).first()

#     if not shipment:
#         return None

#     status = (data.status or "IN_TRANSIT").upper().strip()

#     # ✅ Validate tracking status
#     if status not in VALID_TRACKING_STATUSES:
#         raise HTTPException(400, "Invalid tracking status")

#     # ✅ Prevent duplicate
#     last = db.query(ShipmentTracking)\
#         .filter(ShipmentTracking.shipment_id == shipment_id)\
#         .order_by(ShipmentTracking.timestamp.desc())\
#         .first()

#     if last and last.location == data.location and last.status == status:
#         raise HTTPException(400, "Duplicate tracking update")

#     try:
#         print("🔵 STEP A: Creating tracking entry")

#         tracking = ShipmentTracking(
#             shipment_id=shipment_id,
#             location=data.location,
#             status=status,
#             description=data.description,
#             event_type="TRACKING_UPDATE",
#             timestamp=datetime.utcnow()
#         )

#         db.add(tracking)

#         # =========================
#         # ✅ SAFE AUTO STATUS UPDATE
#         # =========================
#         print("🔵 STEP B: Checking if status update needed")

#         next_status = status

#         # =========================
#         # ✅ AUTO STATUS UPDATE (INSIDE TRACKING SERVICE)
#         # =========================
#         print("🔵 STEP B: Checking status update")

#         next_status = status

#         if can_transition(shipment.status, next_status):
#             print(f"✅ Updating shipment status: {shipment.status} → {next_status}")

#             # update shipment table
#             shipment.status = next_status

#             # optional timestamps
#             if next_status == "DELIVERED":
#                 shipment.delivered_at = datetime.utcnow()

#             elif next_status == "RETURNED":
#                 shipment.returned_at = datetime.utcnow()
            
#             db.add(shipment)
            

#         else:
#             print(f"⚠️ No status change allowed: {shipment.status} → {next_status}")
        

#         # =========================
#         # ✅ SINGLE COMMIT (IMPORTANT)
#         # =========================
#         print("🔵 STEP C: Committing transaction")
#         # db.commit()

#         # db.refresh(tracking)

#         return tracking

#     except HTTPException as http_err:
#         print(f"⚠️ HTTPException: {http_err.detail}")
#         db.rollback()
#         raise

#     except Exception as e:
#         print("🔥 ERROR:", str(e))
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
# def update_shipment_status_service(shipment_id: int, new_status: str, db):
#     print("🔵 STEP 0: Function called")
#     print(f"➡️ Shipment ID: {shipment_id}, Incoming Status: {new_status}")
#         # 1. Update main shipment table
#     shipment.status = new_status

#     # 2. Add tracking entry (ALWAYS)
#     tracking = ShipmentTracking(
#         shipment_id=shipment.id,
#         status=new_status,
#         description=f"Status changed to {new_status}"
#     )

#     db.add(tracking)

#     try:
#         print("🔵 STEP 1: Fetching shipment from DB") 
#         shipment = db.query(Shipment).filter(
#             Shipment.id == shipment_id
#         ).first()

#         if not shipment:
#             print("❌ STEP FAIL: Shipment not found")
#             return None

#         print(f"✅ STEP 2: Shipment found with current status: {shipment.status}")

#         new_status = new_status.upper()
#         print(f"🔵 STEP 3: Normalized new status: {new_status}")

#         print("🔵 STEP 4: Checking transition validity")
#         if not can_transition(shipment.status, new_status):
#             print(f"❌ STEP FAIL: Invalid transition {shipment.status} → {new_status}")
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Invalid transition from {shipment.status} to {new_status}"
#             )

#         print("✅ STEP 5: Transition valid")

#         # =========================
#         # SPECIAL LOGIC
#         # =========================

#         if new_status == "SHIPPED":
#             print("🔵 STEP 6: Applying SHIPPED logic")

#             shipment.tracking_number = generate_tracking_number()
#             print(f"   ➤ Generated tracking number: {shipment.tracking_number}")

#             city = get_customer_city(shipment.order_id)
#             print(f"   ➤ Customer city: {city}")

#             shipment.carrier = assign_carrier_by_city(city)
#             print(f"   ➤ Assigned carrier: {shipment.carrier}")

#             shipment.estimated_delivery = datetime.utcnow() + timedelta(days=7)
#             print(f"   ➤ Estimated delivery set: {shipment.estimated_delivery}")

#         elif new_status == "DELIVERED":
#             print("🔵 STEP 7: Applying DELIVERED logic")

#             shipment.delivered_at = datetime.utcnow()
            
#             print(f"   ➤ Delivered at: {shipment.delivered_at}")
#         elif new_status == "RETURN_REQUESTED":
#             shipment.return_requested_at = datetime.utcnow()
            

#         elif new_status == "RETURNED":
#             shipment.returned_at = datetime.utcnow()

#         elif new_status == "REPLACEMENT_REQUESTED":
#             shipment.replacement_requested_at = datetime.utcnow()

#         elif new_status == "REPLACED":
#             shipment.replaced_at = datetime.utcnow()

#         # =========================
#         # 🔥 ALWAYS UPDATE STATUS
#         # =========================

#         print("🔵 STEP 8: Updating shipment status")
#         shipment.status = new_status

#         print("🔵 STEP 9: Committing to DB")
#         db.commit()

#         print("✅ STEP 10: Commit successful")

#         print("🔵 STEP 11: Refreshing object")
#         db.refresh(shipment)
#     #       kakfa event produceL:
#     # 🔥 SEND EVENT AFTER COMMIT
#         try: 
#             print("sending event to kakfa---------------------------------------------------------------")
#             send_event("shipment-events", {
#                 "event": "SHIPMENT_STATUS_UPDATED",
#                 "data": {
#                     "shipment_id": shipment.id,
#                     "order_id": shipment.order_id,
#                     "status": shipment.status,
#                     "carrier": shipment.carrier,
#                     "tracking_number": shipment.tracking_number,
#                     "timestamp": str(datetime.utcnow())
#                 }
#             })
#             print(" sent ..event to kakfa---------------------------------------------------------------")

#         except Exception as e:
#             print("⚠️ Kafka failed but DB is OK:", str(e))
#         print("✅ STEP 12: Returning updated shipment")
#         shipment.allowed_actions = VALID_TRANSITIONS.get(shipment.status, [])

#         return shipment

#     except HTTPException as http_err:
#         print(f"⚠️ HTTPException occurred: {http_err.detail}")
#         raise

#     except Exception as e:
#         print("🔥 STEP ERROR: Exception occurred before commit")
#         print(f"❌ Error: {str(e)}")

#         print("🔵 Rolling back transaction")
#         db.rollback()

#         raise HTTPException(status_code=500, detail=str(e))
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
    shipment.allowed_actions = VALID_TRANSITIONS.get(shipment.status, [])

    return shipment

def get_next_actions_service(shipment_id: int, db):
    shipment = db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()

    if not shipment:
        return None

    current = shipment.status

    actions = VALID_TRANSITIONS.get(current, [])

    return {
        "current": current,
        "allowed_actions": actions
    }

def get_shipments_by_order_service(order_id: int, db):
    return db.query(Shipment).filter(
        Shipment.order_id == order_id
    ).all()



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




