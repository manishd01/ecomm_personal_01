from datetime import datetime

from app.kafka.payment_topics import *
from app.kafka.payment_producer import send_event
from sqlalchemy.orm import Session
from app.models.payment_model import Payment
import requests


def get_payment_by_id(payment_id: int, db: Session):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_all_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()


def get_payments_by_order(order_id: int, db: Session):
    return db.query(Payment).filter(Payment.order_id == order_id).all()


def create_new_payment(payment_data, db: Session):

    try:

        # =========================
        # CONVERT TO DICT
        # =========================

        if hasattr(payment_data, "dict"):
            payment_data = payment_data.dict()

        # =========================
        # SAVE PAYMENT
        # =========================

        new_payment = Payment(**payment_data)

        print("data from frontend:", new_payment)

        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        print("✅ Payment saved")

        # =========================
        # EMIT SUCCESS EVENT
        # =========================

        # =========================================
        # FETCH ORDER DETAILS
        # =========================================

        response = requests.get(
            f"http://order-service:8000/api/orders/{new_payment.order_id}"
        )

        order_data = response.json()

        print("📦 Order data fetched:", order_data)

        if new_payment.status.lower() == "success":

            send_event(
                PAYMENT_EVENTS_TOPIC,
                {
                    "event": "PAYMENT_COMPLETED",
                    "data": {
                        "payment_id": new_payment.id,
                        "order_id": new_payment.order_id,
                        "customer_id": new_payment.customer_id,
                        "amount": new_payment.amount,
                        "payment_method": new_payment.payment_method,
                        "status": new_payment.status,
                        "timestamp": str(datetime.utcnow()),
                        # FETCHED FROM ORDER SERVICE
                        "product_id": order_data["product_id"],
                        "quantity": order_data["quantity"],
                    },
                },
            )

            print("✅ PAYMENT_COMPLETED emitted")

        else:

            send_event(
                PAYMENT_EVENTS_TOPIC,
                {
                    "event": "PAYMENT_FAILED",
                    "data": {
                        "payment_id": new_payment.id,
                        "order_id": new_payment.order_id,
                        "customer_id": new_payment.customer_id,
                        "amount": new_payment.amount,
                        "payment_method": new_payment.payment_method,
                        "status": new_payment.status,
                        "timestamp": str(datetime.utcnow()),
                        # FETCHED FROM ORDER SERVICE
                        "product_id": order_data["product_id"],
                        "quantity": order_data["quantity"],
                    },
                },
            )

            print("❌ PAYMENT_FAILED emitted")

        return new_payment

    except Exception as e:

        # =========================
        # ROLLBACK
        # =========================

        db.rollback()

        print("❌ Payment failed:", str(e))

        # =========================
        # EMIT FAILURE EVENT
        # =========================

        send_event(
            PAYMENT_EVENTS_TOPIC,
            {
                "event": "PAYMENT_FAILED",
                "data": {
                    "order_id": payment_data.get("order_id"),
                    "customer_id": payment_data.get("customer_id"),
                    "reason": str(e),
                    "timestamp": str(datetime.utcnow()),
                },
            },
        )

        print("❌ PAYMENT_FAILED emitted")

        raise e


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
