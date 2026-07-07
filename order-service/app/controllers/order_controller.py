from fastapi import HTTPException

from app.services.order_service import (
    get_order_by_id,
    create_new_order,
    update_existing_order,
    delete_order_by_id,
    get_all_orders_Service,
    update_order_status_service,
)

from common_logging.logging_config import setup_logger

logger = setup_logger("order-service")


def get_order(order_id: int):

    logger.info(
        "Fetching order",
        extra={
            "order_id": order_id,
            "status": "STARTED",
        },
    )

    order = get_order_by_id(order_id)

    if not order:

        logger.warning(
            "Order not found",
            extra={
                "order_id": order_id,
                "status": "FAILED",
            },
        )

        raise HTTPException(status_code=404, detail="Order not found")

    logger.info(
        "Order fetched successfully",
        extra={
            "order_id": order_id,
            "status": "SUCCESS",
        },
    )

    return order


def get_all_orders_con():

    logger.info(
        "Fetching all orders",
        extra={
            "status": "STARTED",
        },
    )

    orders = get_all_orders_Service()

    logger.info(
        "All orders fetched successfully",
        extra={
            "order_count": len(orders),
            "status": "SUCCESS",
        },
    )

    return orders


def create_order(order_data):

    logger.info(
        "Order creation requested",
        extra={
            "customer_id": order_data.customer_id,
            "status": "STARTED",
        },
    )

    order = create_new_order(order_data)

    logger.info(
        "Order created successfully",
        extra={
            "order_id": order.id,
            "customer_id": order.customer_id,
            "status": "SUCCESS",
        },
    )

    return order


def update_order(order_id: int, order_data):

    logger.info(
        "Order update requested",
        extra={
            "order_id": order_id,
            "status": "STARTED",
        },
    )

    updated_order = update_existing_order(order_id, order_data)

    if not updated_order:

        logger.warning(
            "Order update failed because order was not found",
            extra={
                "order_id": order_id,
                "status": "FAILED",
            },
        )

        raise HTTPException(status_code=404, detail="Order not found")

    logger.info(
        "Order updated successfully",
        extra={
            "order_id": order_id,
            "status": "SUCCESS",
        },
    )

    return updated_order


def delete_order(order_id: int):

    logger.info(
        "Order deletion requested",
        extra={
            "order_id": order_id,
            "status": "STARTED",
        },
    )

    if not delete_order_by_id(order_id):

        logger.warning(
            "Order deletion failed because order was not found",
            extra={
                "order_id": order_id,
                "status": "FAILED",
            },
        )

        raise HTTPException(status_code=404, detail="Order not found")

    logger.info(
        "Order deleted successfully",
        extra={
            "order_id": order_id,
            "status": "SUCCESS",
        },
    )

    return {"detail": "Order deleted successfully"}


def update_order_status_controller(order_id, data):

    logger.info(
        "Order status update requested",
        extra={
            "order_id": order_id,
            "new_status": data.status,
            "status": "STARTED",
        },
    )

    try:

        updated_order = update_order_status_service(
            order_id,
            data.status,
        )

        logger.info(
            "Order status updated successfully",
            extra={
                "order_id": order_id,
                "new_status": data.status,
                "status": "SUCCESS",
            },
        )

        return updated_order

    except Exception as e:

        logger.exception(
            "Order status update failed",
            extra={
                "order_id": order_id,
                "new_status": data.status,
                "status": "FAILED",
            },
        )

        raise HTTPException(status_code=500, detail=str(e))
