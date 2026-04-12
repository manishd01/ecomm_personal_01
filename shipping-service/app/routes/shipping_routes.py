from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.shipping_schema import (
    CreateShipment,
    UpdateShipmentStatus,
    ShipmentResponse,
    ShipmentDetailResponse
)
from app.controllers.shipping_controller import (
    get_shipment,
    get_shipments_by_order,
    create_shipment,
    update_shipment_status
)

router = APIRouter()


@router.post("/shipments", response_model=ShipmentResponse)
def create_new_shipment(shipment: CreateShipment, db: Session = Depends(get_db)):
    """Create a new shipment for an order"""
    return create_shipment(shipment.order_id, db)


@router.get("/shipments/{shipment_id}", response_model=ShipmentDetailResponse)
def get_shipment_details(shipment_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific shipment"""
    return get_shipment(shipment_id, db)


from typing import Optional

@router.get("/shipments", response_model=list[ShipmentResponse])
def list_shipments(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    from app.services.shipping_service import list_shipments_service
    return list_shipments_service(db, status, search)

@router.patch("/shipments/{shipment_id}/status", response_model=ShipmentResponse)
def update_status(shipment_id: int, status_update: UpdateShipmentStatus, db: Session = Depends(get_db)):
    """Update shipment status with validation"""
    print ("entering in routesupdate status")
    return update_shipment_status(shipment_id, status_update.status, db)


@router.get("/orders/{order_id}/shipments", response_model=list[ShipmentResponse])
def get_order_shipments(order_id: int, db: Session = Depends(get_db)):
    """Get all shipments for a specific order"""
    return get_shipments_by_order(order_id, db)


@router.get("/health")
def health():
    return {"status": "ok"}
