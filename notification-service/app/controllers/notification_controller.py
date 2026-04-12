from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.notification_service import (
    get_notification_by_id,
    get_all_notifications,
    get_customer_notifications,
    get_unread_notifications,
    create_new_notification,
    update_existing_notification,
    delete_notification_by_id
)


def get_notification(notification_id: int, db: Session):
    notification = get_notification_by_id(notification_id, db)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


def list_notifications(db: Session, skip: int = 0, limit: int = 100):
    return get_all_notifications(db, skip, limit)


def list_customer_notifications(customer_id: int, db: Session, skip: int = 0, limit: int = 100):
    return get_customer_notifications(customer_id, db, skip, limit)


def list_unread_notifications(customer_id: int, db: Session):
    return get_unread_notifications(customer_id, db)


def create_notification(notification_data, db: Session):
    return create_new_notification(notification_data, db)


def update_notification(notification_id: int, notification_data, db: Session):
    updated_notification = update_existing_notification(notification_id, notification_data, db)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification


def delete_notification(notification_id: int, db: Session):
    if not delete_notification_by_id(notification_id, db):
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"detail": "Notification deleted successfully"}