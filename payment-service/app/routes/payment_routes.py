from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentResponse
from app.controllers.payment_controller import (
    get_payment,
    list_payments,
    get_order_payments,
    create_payment,
    update_payment,
    delete_payment
)

router = APIRouter()


@router.get("/payments", response_model=list[PaymentResponse])
def read_all_payments(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return list_payments(db, skip, limit)


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    return get_payment(payment_id, db)


@router.get("/payments/order/{order_id}", response_model=list[PaymentResponse])
def read_order_payments(order_id: int, db: Session = Depends(get_db)):
    return get_order_payments(order_id, db)


@router.post("/payments", response_model=PaymentResponse)
def add_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment(payment_data, db)


@router.put("/payments/{payment_id}", response_model=PaymentResponse)
def modify_payment(payment_id: int, payment_data: PaymentUpdate, db: Session = Depends(get_db)):
    return update_payment(payment_id, payment_data, db)


@router.delete("/payments/{payment_id}")
def remove_payment(payment_id: int, db: Session = Depends(get_db)):
    return delete_payment(payment_id, db)




@router.get("/health")
def health():
    return {"status": "ok"}