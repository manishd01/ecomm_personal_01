from sqlalchemy.orm import Session
from app.models.inventory_model import Inventory
from fastapi import HTTPException


def decrease_inventory_stock(item_id: int, quantity: int, db: Session):
    item = (
        db.query(Inventory)
        .filter(Inventory.id == item_id)
        .with_for_update()  # 🔐 prevents race condition
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Product not found")

    if item.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    item.quantity -= quantity  # ✅ correct logic

    db.commit()
    db.refresh(item)

    return item


def get_inventory_by_id(item_id: int, db: Session):
    return db.query(Inventory).filter(Inventory.id == item_id).first()


def get_all_inventory_items(db: Session):
    return db.query(Inventory).all()


def create_new_inventory(item_data, db):
    existing = (
        db.query(Inventory)
        .filter(Inventory.model_number == item_data.model_number)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Product with this model_number already exists"
        )

    new_item = Inventory(**item_data.dict())

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def update_existing_inventory(item_id: int, item_data, db: Session):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        return None

    for key, value in item_data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


def delete_inventory_by_id(item_id: int, db: Session):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        return None

    db.delete(item)
    db.commit()
    return True
