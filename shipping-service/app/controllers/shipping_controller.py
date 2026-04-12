from fastapi import HTTPException
from app.exceptions import OrderNotFoundError, ShipmentAlreadyExistsError
from sqlalchemy.orm import Session
from app.services.shipping_service import (
    create_shipment_service,
    update_shipment_status_service,
    get_shipment_service,
    get_shipments_by_order_service,
    notify_order_shipped
)


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


# =========================
# UPDATE STATUS
# =========================
def update_shipment_status(shipment_id: int, new_status: str, db: Session):

    try:
        shipment = update_shipment_status_service(
            shipment_id,
            new_status,
            db
        )

        if not shipment:
            raise HTTPException(404, "Shipment not found")

        return shipment

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(500, str(e))