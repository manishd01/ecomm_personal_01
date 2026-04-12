from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.payment_service import (
    get_payment_by_id,
    get_all_payments,
    get_payments_by_order,
    create_new_payment,
    update_existing_payment,
    delete_payment_by_id
)


def get_payment(payment_id: int, db: Session):
    payment = get_payment_by_id(payment_id, db)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def list_payments(db: Session, skip: int = 0, limit: int = 100):
    return get_all_payments(db, skip, limit)


def get_order_payments(order_id: int, db: Session):
    return get_payments_by_order(order_id, db)


def create_payment(payment_data, db: Session):
    return create_new_payment(payment_data, db)


def update_payment(payment_id: int, payment_data, db: Session):
    updated_payment = update_existing_payment(payment_id, payment_data, db)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


def delete_payment(payment_id: int, db: Session):
    if not delete_payment_by_id(payment_id, db):
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"detail": "Payment deleted successfully"}