from typing import List

from fastapi import APIRouter
from app.controllers.order_controller import (
    get_order, create_order, update_order, delete_order,get_all_orders_con
)
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter()

@router.get("/orders",response_model=List[OrderResponse])
def get_all_orders():
    return get_all_orders_con()

@router.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int):
    return get_order(order_id)


@router.post("/orders", response_model=OrderResponse)
def add_order(order_data: OrderCreate):
    
    print("data recieved in route:---", order_data)
    return create_order(order_data)


@router.put("/orders/{order_id}", response_model=OrderResponse)
def modify_order(order_id: int, order_data: OrderUpdate):
    return update_order(order_id, order_data)


@router.delete("/orders/{order_id}")
def remove_order(order_id: int):
    return delete_order(order_id)



@router.get("/health")
def health():
    return {"status": "ok"}