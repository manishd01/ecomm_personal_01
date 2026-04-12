from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.customer_service import (
    get_customer_by_id,
    get_all_customers,
    get_customer_by_email,
    create_new_customer,
    update_existing_customer,
    delete_customer_by_id
)


def get_customer(customer_id: int, db: Session):
    customer = get_customer_by_id(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def list_customers(db: Session, skip: int = 0, limit: int = 100):
    return get_all_customers(db, skip, limit)


def get_customer_by_email_controller(email: str, db: Session):
    customer = get_customer_by_email(email, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def create_customer(customer_data, db: Session):
    # Check if customer with this email already exists
    existing = get_customer_by_email(customer_data.email, db)
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this email already exists")
    return create_new_customer(customer_data, db)


def update_customer(customer_id: int, customer_data, db: Session):
    updated_customer = update_existing_customer(customer_id, customer_data, db)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


def delete_customer(customer_id: int, db: Session):
    if not delete_customer_by_id(customer_id, db):
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": "Customer deleted successfully"}
