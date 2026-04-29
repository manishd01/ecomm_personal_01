from typing import Optional

from fastapi import HTTPException
from app.exceptions import OrderNotFoundError, ShipmentAlreadyExistsError
from sqlalchemy.orm import Session
from app.schemas.shipping_schema import TrackingCreate
from app.services.shipping_service import (
    create_shipment_service,
    update_shipment_status_service,
    get_shipment_service,
    get_shipments_by_order_service,
    notify_order_shipped,
    add_tracking_update_service,
    get_next_actions_service
)



def get_next_actions_controller(shipment_id: int, db):
    try:
        result = get_next_actions_service(shipment_id, db)

        if not result:
            raise HTTPException(404, "Shipment not found")

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(500, str(e))
# =========================
# CREATE
# =========================
def create_shipment(order_id: int, db: Session):

    try:
        shipment = create_shipment_service(order_id, db)

        notify_order_shipped(order_id)

        return shipment

    except OrderNotFoundError:
        raise HTTPException(404, "Order not found")

    except ShipmentAlreadyExistsError:
        raise HTTPException(400, "Shipment already exists for this order")

    except Exception as e:
        raise HTTPException(500, str(e))


# =========================
# GET ONE
# =========================
def get_shipment(shipment_id: int, db: Session):

    shipment = get_shipment_service(shipment_id, db)

    if not shipment:
        raise HTTPException(404, "Shipment not found")

    return shipment


# =========================
# GET BY ORDER
# =========================
def get_shipments_by_order(order_id: int, db: Session):
    return get_shipments_by_order_service(order_id, db)

def add_tracking_controller(
    shipment_id: int,
    data: TrackingCreate,
    db: Session,
    location: Optional[str] = None
):
    try:
        print(f"Adding tracking update for shipment controller {shipment_id}")
        tracking = add_tracking_update_service(
            shipment_id,
            data,
            db,location
        )

        if not tracking:
            raise HTTPException(404, "Shipment not found")

        return tracking

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(500, str(e))
    
def get_next_actions_controller(shipment_id: int, db):
    try:
        print(f"Fetching next actions for shipment {shipment_id}")

        result = get_next_actions_service(shipment_id, db)

        if not result:
            print("❌ Shipment not found")
            raise HTTPException(404, "Shipment not found")

        print(f"✅ Allowed actions: {result}")

        return result

    except HTTPException:
        raise

    except Exception as e:
        print(f"🔥 Error in get_next_actions_controller: {str(e)}")
        raise HTTPException(500, str(e))

# =========================
# UPDATE STATUS
# =========================
def update_shipment_status(shipment_id: int, new_status: str, db: Session, location: Optional[str] = None):

    try:
        shipment = update_shipment_status_service(
            shipment_id,
            new_status,
            db,
            location
        )

        if not shipment:
            raise HTTPException(404, "Shipment not found")

        return shipment

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(500, str(e))