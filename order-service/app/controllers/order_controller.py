from fastapi import HTTPException

from app.services.order_service import (
    get_order_by_id,
    create_new_order,
    update_existing_order,
    delete_order_by_id,
    get_all_orders_Service,
    update_order_status_service
)

def get_order(order_id: int):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_all_orders_con():
    return get_all_orders_Service()

def create_order(order_data):
    print("Data received in controller:", order_data)
    return create_new_order(order_data)

def update_order(order_id: int, order_data):
    updated_order = update_existing_order(order_id, order_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

def delete_order(order_id: int):
    if not delete_order_by_id(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}


def update_order_status_controller(order_id, data):

    try:
        return update_order_status_service(
            order_id,
            data.status,
        
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))