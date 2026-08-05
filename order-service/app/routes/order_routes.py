from typing import List

from fastapi import APIRouter
from app.controllers.order_controller import (
    get_order,
    create_order,
    update_order,
    delete_order,
    get_all_orders_con,
    update_order_status_controller,
)
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse

from common_logging.logging_config import setup_logger

logger = setup_logger("order-service")

router = APIRouter()


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders():

    logger.info(
        "Get all orders API invoked",
        extra={
            "endpoint": "/orders",
            "method": "GET",
            "status": "STARTED",
        },
    )

    return get_all_orders_con()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int):

    logger.info(
        "Get order API invoked",
        extra={
            "endpoint": f"/orders/{order_id}",
            "method": "GET",
            "order_id": order_id,
            "status": "STARTED",
        },
    )

    return get_order(order_id)


@router.post("/orders", response_model=OrderResponse)
def add_order(order_data: OrderCreate):

    logger.info(
        "Create order API invoked",
        extra={
            "endpoint": "/orders",
            "method": "POST",
            "user_id": order_data.customer_id,
            "status": "STARTED",
        },
    )

    return create_order(order_data)


@router.put("/orders/{order_id}", response_model=OrderResponse)
def modify_order(order_id: int, order_data: OrderUpdate):

    logger.info(
        "Update order API invoked",
        extra={
            "endpoint": f"/orders/{order_id}",
            "method": "PUT",
            "order_id": order_id,
            "status": "STARTED",
        },
    )

    return update_order(order_id, order_data)


@router.delete("/orders/{order_id}")
def remove_order(order_id: int):

    logger.info(
        "Delete order API invoked",
        extra={
            "endpoint": f"/orders/{order_id}",
            "method": "DELETE",
            "order_id": order_id,
            "status": "STARTED",
        },
    )

    return delete_order(order_id)


@router.post("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    data: OrderUpdate,
):

    logger.info(
        "Update order status API invoked",
        extra={
            "endpoint": f"/orders/{order_id}/status",
            "method": "POST",
            "order_id": order_id,
            "new_status": data.status,
            "status": "STARTED",
        },
    )

    return update_order_status_controller(order_id, data)


@router.get("/health")
def health():

    logger.info(
        "Order service health check API invoked",
        extra={
            "endpoint": "/health",
            "method": "GET",
            "status": "SUCCESS",
        },
    )

    return {"status": "ok"}
