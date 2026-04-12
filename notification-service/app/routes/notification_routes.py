from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.notification_schema import NotificationCreate, NotificationUpdate, NotificationResponse
from app.controllers.notification_controller import (
    get_notification,
    list_notifications,
    list_customer_notifications,
    list_unread_notifications,
    create_notification,
    update_notification,
    delete_notification
)

router = APIRouter()


@router.get("/notifications", response_model=list[NotificationResponse])
def read_all_notifications(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return list_notifications(db, skip, limit)


@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    return get_notification(notification_id, db)


@router.get("/notifications/customer/{customer_id}", response_model=list[NotificationResponse])
def read_customer_notifications(customer_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return list_customer_notifications(customer_id, db, skip, limit)


@router.get("/notifications/customer/{customer_id}/unread", response_model=list[NotificationResponse])
def read_unread_notifications(customer_id: int, db: Session = Depends(get_db)):
    return list_unread_notifications(customer_id, db)


@router.post("/notifications", response_model=NotificationResponse)
def add_notification(notification_data: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(notification_data, db)


@router.put("/notifications/{notification_id}", response_model=NotificationResponse)
def modify_notification(notification_id: int, notification_data: NotificationUpdate, db: Session = Depends(get_db)):
    return update_notification(notification_id, notification_data, db)


@router.delete("/notifications/{notification_id}")
def remove_notification(notification_id: int, db: Session = Depends(get_db)):
    return delete_notification(notification_id, db)



@router.get("/health")
def health():
    return {"status": "ok"}