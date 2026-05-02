from sqlalchemy.orm import Session
from app.models.notification_model import Notification

def get_notification_by_id(notification_id: int, db: Session):
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_all_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Notification).offset(skip).limit(limit).all()


def get_customer_notifications(customer_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Notification).filter(Notification.customer_id == customer_id).offset(skip).limit(limit).all()


def get_unread_notifications(customer_id: int, db: Session):
    return db.query(Notification).filter(Notification.customer_id == customer_id, Notification.is_read == 0).all()


def create_new_notification(notification_data, db: Session):
    if hasattr(notification_data, "dict"):     # imp -> for Kafka flow -> sends plain JSON → becomes dict
        notification_data = notification_data.dict()
        
    new_notification = Notification(**notification_data)# no need to convert now
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    print("data saevd for notification")
    return new_notification


def update_existing_notification(notification_id: int, notification_data, db: Session):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        return None

    for key, value in notification_data.dict(exclude_unset=True).items():
        setattr(notification, key, value)

    db.commit()
    db.refresh(notification)
    return notification


def delete_notification_by_id(notification_id: int, db: Session):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        return None

    db.delete(notification)
    db.commit()
    return True
