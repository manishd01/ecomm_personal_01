from sqlalchemy.orm import Session
from app.models.customer_model import Customer

def get_customer_by_id(customer_id: int, db: Session):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_all_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer_by_email(email: str, db: Session):
    return db.query(Customer).filter(Customer.email == email).first()


def create_new_customer(customer_data, db: Session):
    new_customer = Customer(**customer_data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def update_existing_customer(customer_id: int, customer_data, db: Session):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


def delete_customer_by_id(customer_id: int, db: Session):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return None

    db.delete(customer)
    db.commit()
    return True
