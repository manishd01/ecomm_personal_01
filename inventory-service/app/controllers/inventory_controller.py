from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.inventory_service import (
    get_inventory_by_id,
    create_new_inventory,
    update_existing_inventory,
    delete_inventory_by_id,
    get_all_inventory_items,
    decrease_inventory_stock
)

def decrease_stock(item_id: int, data, db: Session):
    return decrease_inventory_stock(item_id, data.quantity, db)


def get_inventory(item_id: int, db: Session):
    item = get_inventory_by_id(item_id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
def get_all_inventory(db: Session):
    return get_all_inventory_items(db)


def create_inventory(item_data, db: Session):
    return create_new_inventory(item_data, db)


def update_inventory(item_id: int, item_data, db: Session):
    updated_item = update_existing_inventory(item_id, item_data, db)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


def delete_inventory(item_id: int, db: Session):
    if not delete_inventory_by_id(item_id, db):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted successfully"}