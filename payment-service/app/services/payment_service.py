from sqlalchemy.orm import Session
from app.models.payment_model import Payment

def get_payment_by_id(payment_id: int, db: Session):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_all_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()


def get_payments_by_order(order_id: int, db: Session):
    return db.query(Payment).filter(Payment.order_id == order_id).all()


def create_new_payment(payment_data, db: Session):
    new_payment = Payment(**payment_data.dict())
    print ("data from frontrnd: ", new_payment)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


def update_existing_payment(payment_id: int, payment_data, db: Session):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None

    for key, value in payment_data.dict(exclude_unset=True).items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


def delete_payment_by_id(payment_id: int, db: Session):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return None

    db.delete(payment)
    db.commit()
    return True