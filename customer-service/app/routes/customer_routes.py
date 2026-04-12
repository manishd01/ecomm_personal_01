from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from app.controllers.customer_controller import (
    get_customer,
    list_customers,
    get_customer_by_email_controller,
    create_customer,
    update_customer,
    delete_customer
)

router = APIRouter()


@router.get("/customers", response_model=list[CustomerResponse])
def read_all_customers(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return list_customers(db, skip, limit)


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_customer(customer_id, db)


@router.get("/customers/email/{email}", response_model=CustomerResponse)
def read_customer_by_email(email: str, db: Session = Depends(get_db)):
    return get_customer_by_email_controller(email, db)


@router.post("/customers", response_model=CustomerResponse)
def add_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(customer_data, db)


@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def modify_customer(customer_id: int, customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    return update_customer(customer_id, customer_data, db)


@router.delete("/customers/{customer_id}")
def remove_customer(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(customer_id, db)

@router.get("/health")
def health():
    return {"status": "ok"}