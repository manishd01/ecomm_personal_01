
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.schemas.shipping_schema import *
# from app.controllers.shipping_controller import *

# router = APIRouter()


# @router.post("/shipments", response_model=ShipmentResponse)
# def create_shipment_route(data: CreateShipment, db: Session = Depends(get_db)):
#     return create_shipment_controller(data.order_id, db)


# @router.get("/shipments/{shipment_id}", response_model=ShipmentDetailResponse)
# def get_shipment_route(shipment_id: int, db: Session = Depends(get_db)):
#     return get_shipment_controller(shipment_id, db)


# @router.patch("/shipments/{shipment_id}/status")
# def update_status_route(shipment_id: int, data: UpdateShipmentStatus, db: Session = Depends(get_db)):
#     return update_status_controller(shipment_id, data, db)


# @router.post("/shipments/{shipment_id}/tracking")
# def add_tracking_route(shipment_id: int, data: TrackingCreate, db: Session = Depends(get_db)):
#     return add_tracking_controller(shipment_id, data, db)


# @router.get("/shipments/{shipment_id}/next-actions")
# def next_actions_route(shipment_id: int, db: Session = Depends(get_db)):
#     return get_next_actions_controller(shipment_id, db)

# # ✅ LIST ALL SHIPMENTS (RESTORED)
# @router.get("/shipments", response_model=list[ShipmentDetailResponse])
# def list_shipments_route(
#     status: Optional[str] = None,
#     search: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     return list_shipments_service(db, status, search)


# # ✅ HEALTH CHECK (RESTORED)
# @router.get("/health")
# def health_check():
#     return {"status": "ok"}

# # 

# 30apr:
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.shipping_schema import (
    CreateShipment,
    TrackingCreate,
    TrackingResponse,
    UpdateShipmentStatus,
    ShipmentResponse,
    ShipmentDetailResponse,
    
)
from app.controllers.shipping_controller import (
    get_shipment,
    get_shipments_by_order,
    create_shipment,
    update_shipment_status,
    add_tracking_controller,
    get_next_actions_controller
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

@router.get("/shipments", response_model=list[ShipmentDetailResponse])
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
    location=status_update.location
    return update_shipment_status(shipment_id, status_update.status, db, location)

@router.post(
    "/shipments/{shipment_id}/tracking",
    response_model=TrackingResponse
)
def add_tracking(
    shipment_id: int,
    data: TrackingCreate,
    db: Session = Depends(get_db)
):
    location=data.location
    print("data came in trakcing addding:----", data)
    return add_tracking_controller(shipment_id, data, db,location)

@router.get("/orders/{order_id}/shipments", response_model=list[ShipmentResponse])
def get_order_shipments(order_id: int, db: Session = Depends(get_db)):
    """Get all shipments for a specific order"""
    return get_shipments_by_order(order_id, db)



@router.get("/shipments/{shipment_id}/next-actions")
def get_next_actions(shipment_id: int, db: Session = Depends(get_db)):
    return get_next_actions_controller(shipment_id, db)

@router.get("/health")
def health():
    return {"status": "ok"}
