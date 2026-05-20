from fastapi import HTTPException
from app.models.order_model import Order
import requests
from app.database import SessionLocal
from app.kafka.order_producer import send_event
from datetime import datetime

INVENTORY_SERVICE_URL = "http://inventory-service:8000/api"
CUSTOMER_SERVICE_URL = "http://customer-service:8000/api"


def get_all_orders_Service():
    db = SessionLocal()
    try:
        return db.query(Order).all()
    finally:
        db.close()


def get_order_by_id(order_id: int):
    db = SessionLocal()
    try:
        return db.query(Order).filter(Order.id == order_id).first()
    finally:
        db.close()


def create_new_order(order_data):
    db = SessionLocal()

    try:
        # ✅ Validate customer
        cust_res = requests.get(
            f"{CUSTOMER_SERVICE_URL}/customers/{order_data.customer_id}", timeout=3
        )

        if cust_res.status_code != 200:
            raise HTTPException(status_code=404, detail="Customer not found")

        # ✅ Validate product
        response = requests.get(
            f"{INVENTORY_SERVICE_URL}/inventory/{order_data.product_id}", timeout=3
        )

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")

        product = response.json()

        # # ✅ Stock check   -instant decerae in stock in invntry but need to do it with  kafka topices . so commmenting
        # if order_data.quantity > product["quantity"]:
        #     raise HTTPException(status_code=400, detail="Not enough stock")

        # # ✅ Step 1: Decrease stock
        # update_response = requests.post(
        #     f"{INVENTORY_SERVICE_URL}/inventory/{order_data.product_id}/decrease",
        #     json={"quantity": order_data.quantity},
        #     timeout=3,
        # )

        # if update_response.status_code != 200:
        #     raise HTTPException(status_code=500, detail="Inventory update failed")

        # ✅ Step 2: Create order
        try:
            total_price = product["price"] * order_data.quantity

            new_order = Order(
                customer_id=order_data.customer_id,
                product_id=order_data.product_id,
                quantity=order_data.quantity,
                price=product["price"],
                total_price=total_price,
                status="created",
            )

            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            # =========================
            # SEND ORDER CREATED EVENT
            # =========================

            try:

                send_event(
                    "order-events",
                    {
                        "event": "ORDER_CREATED",
                        "data": {
                            "order_id": new_order.id,
                            "customer_id": new_order.customer_id,
                            "product_id": new_order.product_id,
                            "quantity": new_order.quantity,
                            "amount": new_order.total_price,
                            "status": new_order.status,
                            "timestamp": str(datetime.utcnow()),
                        },
                    },
                )

                print("✅ ORDER_CREATED event sent")

            except Exception as e:

                print("⚠️ Kafka send failed:", str(e))

            return new_order

        except Exception as e:
            db.rollback()

            # 🔥 COMPENSATION: rollback stockimppp
            try:
                requests.post(
                    f"{INVENTORY_SERVICE_URL}/inventory/{order_data.product_id}/increase",
                    json={"quantity": order_data.quantity},
                    timeout=3,
                )
            except Exception:
                # log this failure (important in real systems)
                print("❌ CRITICAL: Failed to rollback stock")

            raise HTTPException(status_code=500, detail="Order creation failed")

    except requests.exceptions.RequestException as e:
        db.rollback()
        raise HTTPException(status_code=503, detail="Service unavailable")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def update_existing_order(order_id: int, order_data):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            return None

        data = order_data.dict(exclude_unset=True)

        for key, value in data.items():
            setattr(order, key, value)

        # 🔥 Recalculate total
        if "quantity" in data or "price" in data:
            order.total_price = order.quantity * order.price

        db.commit()
        db.refresh(order)

        return order

    finally:
        db.close()


def update_order_status_service(order_id, status):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        return {"message": "Order not found"}

    order.status = status

    db.commit()
    db.refresh(order)

    print("✅ Order status updated from shipping-service")

    print("✅ Order status updated from shipping-service")

    # =========================
    # SEND KAFKA EVENT
    # =========================
    try:
        send_event(
            "order-events",
            {
                "event": "ORDER_STATUS_UPDATED",
                "data": {
                    "order_id": order.id,
                    "customer_id": order.customer_id,
                    "status": order.status,
                    "timestamp": str(datetime.utcnow()),
                },
            },
        )

        print("✅ Kafka event sent")

    except Exception as e:
        print("⚠️ Kafka send failed:", str(e))

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "status": order.status,
    }


def delete_order_by_id(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            return None

        db.delete(order)
        db.commit()

        return True

    finally:
        db.close()
