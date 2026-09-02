import uuid

from fastapi import HTTPException
from app.models.order_model import Order
import requests
from app.database import SessionLocal
from app.kafka.order_producer import send_event
from datetime import datetime

from common_logging.logging_config import setup_logger

logger = setup_logger("order-service")

INVENTORY_SERVICE_URL = "http://inventory-service:8000/api"
CUSTOMER_SERVICE_URL = "http://customer-service:8000/api"


def get_all_orders_Service():

    logger.info(
        "Fetching all orders",
        extra={
            "operation": "GET_ALL_ORDERS",
            "status": "STARTED",
        },
    )

    db = SessionLocal()

    try:

        orders = db.query(Order).all()

        logger.info(
            "Orders fetched successfully",
            extra={
                "operation": "GET_ALL_ORDERS",
                "orders_count": len(orders),
                "status": "SUCCESS",
            },
        )

        return orders

    finally:
        db.close()


def get_order_by_id(order_id: int):

    logger.info(
        "Fetching order by ID",
        extra={
            "order_id": order_id,
            "operation": "GET_ORDER",
            "status": "STARTED",
        },
    )

    db = SessionLocal()

    try:

        order = db.query(Order).filter(Order.id == order_id).first()

        if order:

            logger.info(
                "Order fetched successfully",
                extra={
                    "order_id": order_id,
                    "operation": "GET_ORDER",
                    "status": "SUCCESS",
                },
            )

        else:

            logger.warning(
                "Order not found",
                extra={
                    "order_id": order_id,
                    "operation": "GET_ORDER",
                    "status": "FAILED",
                },
            )

        return order

    finally:
        db.close()


def create_new_order(order_data):

    logger.info(
        "Order creation started",
        extra={
            "customer_id": order_data.customer_id,
            "product_id": order_data.product_id,
            "quantity": order_data.quantity,
            "operation": "CREATE_ORDER",
            "status": "STARTED",
        },
    )

    db = SessionLocal()

    try:
        # ✅ Validate customer

        cust_res = requests.get(
            f"{CUSTOMER_SERVICE_URL}/customers/{order_data.customer_id}", timeout=3
        )

        if cust_res.status_code != 200:

            logger.warning(
                "Customer validation failed during order creation",
                extra={
                    "customer_id": order_data.customer_id,
                    "operation": "CUSTOMER_VALIDATION",
                    "status": "FAILED",
                },
            )

            raise HTTPException(status_code=404, detail="Customer not found")

        logger.info(
            "Customer validated successfully",
            extra={
                "customer_id": order_data.customer_id,
                "operation": "CUSTOMER_VALIDATION",
                "status": "SUCCESS",
            },
        )

        # ✅ Validate product
        response = requests.get(
            f"{INVENTORY_SERVICE_URL}/inventory/{order_data.product_id}", timeout=3
        )

        if response.status_code != 200:

            logger.warning(
                "Product validation failed during order creation",
                extra={
                    "product_id": order_data.product_id,
                    "operation": "PRODUCT_VALIDATION",
                    "status": "FAILED",
                },
            )

            raise HTTPException(status_code=404, detail="Product not found")

        product = response.json()

        logger.info(
            "Product validated successfully",
            extra={
                "product_id": order_data.product_id,
                "operation": "PRODUCT_VALIDATION",
                "status": "SUCCESS",
            },
        )

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
            order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"

            new_order = Order(
                order_number=order_number,
                customer_id=order_data.customer_id,
                product_id=order_data.product_id,
                quantity=order_data.quantity,
                price=product["price"],
                total_price=total_price,
                status="pending",
            )

            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            logger.info(
                "Order created successfully",
                extra={
                    "order_id": new_order.id,
                    "customer_id": new_order.customer_id,
                    "product_id": new_order.product_id,
                    "total_price": new_order.total_price,
                    "status": "SUCCESS",
                },
            )

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

                logger.info(
                    "ORDER_CREATED Kafka event sent successfully",
                    extra={
                        "order_id": new_order.id,
                        "topic": "order-events",
                        "event": "ORDER_CREATED",
                        "status": "SUCCESS",
                    },
                )

            except Exception as e:

                logger.exception(
                    "Failed to send ORDER_CREATED Kafka event",
                    extra={
                        "order_id": new_order.id,
                        "topic": "order-events",
                        "event": "ORDER_CREATED",
                        "status": "FAILED",
                    },
                )

            return new_order

        except Exception as e:

            db.rollback()

            logger.exception(
                "Order creation failed",
                extra={
                    "customer_id": order_data.customer_id,
                    "product_id": order_data.product_id,
                    "operation": "CREATE_ORDER",
                    "status": "FAILED",
                },
            )

            # 🔥 COMPENSATION: rollback stockimppp
            try:

                requests.post(
                    f"{INVENTORY_SERVICE_URL}/inventory/{order_data.product_id}/increase",
                    json={"quantity": order_data.quantity},
                    timeout=3,
                )

                logger.info(
                    "Inventory rollback completed successfully",
                    extra={
                        "product_id": order_data.product_id,
                        "quantity": order_data.quantity,
                        "operation": "INVENTORY_ROLLBACK",
                        "status": "SUCCESS",
                    },
                )

            except Exception:

                # log this failure (important in real systems)
                logger.exception(
                    "Critical failure during inventory rollback",
                    extra={
                        "product_id": order_data.product_id,
                        "operation": "INVENTORY_ROLLBACK",
                        "status": "FAILED",
                    },
                )

            raise HTTPException(status_code=500, detail="Order creation failed")

    except requests.exceptions.RequestException as e:

        db.rollback()

        logger.exception(
            "Dependent service unavailable during order creation",
            extra={
                "operation": "CREATE_ORDER",
                "status": "FAILED",
            },
        )

        raise HTTPException(status_code=503, detail="Service unavailable")

    except Exception as e:

        db.rollback()

        logger.exception(
            "Unexpected error during order creation",
            extra={
                "operation": "CREATE_ORDER",
                "status": "FAILED",
            },
        )

        raise e

    finally:
        db.close()


def update_existing_order(order_id: int, order_data):

    logger.info(
        "Order update started",
        extra={
            "order_id": order_id,
            "operation": "UPDATE_ORDER",
            "status": "STARTED",
        },
    )

    db = SessionLocal()

    try:

        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:

            logger.warning(
                "Order update failed because order was not found",
                extra={
                    "order_id": order_id,
                    "operation": "UPDATE_ORDER",
                    "status": "FAILED",
                },
            )

            return None

        data = order_data.dict(exclude_unset=True)

        for key, value in data.items():
            setattr(order, key, value)

        # 🔥 Recalculate total
        if "quantity" in data or "price" in data:
            order.total_price = order.quantity * order.price

        db.commit()
        db.refresh(order)

        logger.info(
            "Order updated successfully",
            extra={
                "order_id": order.id,
                "operation": "UPDATE_ORDER",
                "status": "SUCCESS",
            },
        )

        return order

    finally:
        db.close()


def update_order_status_service(order_id, status):

    logger.info(
        "Order status update started",
        extra={
            "order_id": order_id,
            "new_status": status,
            "operation": "UPDATE_ORDER_STATUS",
            "status": "STARTED",
        },
    )

    db = SessionLocal()

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:

        logger.warning(
            "Order status update failed because order was not found",
            extra={
                "order_id": order_id,
                "operation": "UPDATE_ORDER_STATUS",
                "status": "FAILED",
            },
        )

        return {"message": "Order not found"}

    order.status = status

    db.commit()
    db.refresh(order)

    logger.info(
        "Order status updated successfully",
        extra={
            "order_id": order.id,
            "new_status": order.status,
            "operation": "UPDATE_ORDER_STATUS",
            "status": "SUCCESS",
        },
    )

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

        logger.info(
            "ORDER_STATUS_UPDATED Kafka event sent successfully",
            extra={
                "order_id": order.id,
                "topic": "order-events",
                "event": "ORDER_STATUS_UPDATED",
                "status": "SUCCESS",
            },
        )

    except Exception as e:

        logger.exception(
            "Failed to send ORDER_STATUS_UPDATED Kafka event",
            extra={
                "order_id": order.id,
                "topic": "order-events",
                "event": "ORDER_STATUS_UPDATED",
                "status": "FAILED",
            },
        )

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "status": order.status,
    }


def delete_order_by_id(order_id: int):

    logger.info(
        "Order deletion started",
        extra={
            "order_id": order_id,
            "operation": "DELETE_ORDER",
            "status": "STARTED",
        },
    )

    db = SessionLocal()

    try:

        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:

            logger.warning(
                "Order deletion failed because order was not found",
                extra={
                    "order_id": order_id,
                    "operation": "DELETE_ORDER",
                    "status": "FAILED",
                },
            )

            return None

        db.delete(order)
        db.commit()

        logger.info(
            "Order deleted successfully",
            extra={
                "order_id": order_id,
                "operation": "DELETE_ORDER",
                "status": "SUCCESS",
            },
        )

        return True

    finally:
        db.close()
