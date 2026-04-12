from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate, InventoryResponse, DecreaseStockRequest
from app.controllers.inventory_controller import (
    get_inventory,
    create_inventory,
    update_inventory,
    delete_inventory,
    get_all_inventory,
    decrease_stock
)
 
router = APIRouter()


@router.post("/inventory/{item_id}/decrease", response_model=InventoryResponse)
def decrease_stock_inventory(item_id: int, data: DecreaseStockRequest, db: Session = Depends(get_db)):
    return decrease_stock(item_id, data, db)

@router.get("/inventory", response_model=List[InventoryResponse])
def read_all_inventory(db: Session = Depends(get_db)):
    ans=get_all_inventory(db)
    print(ans, "Size is", len(ans))
    return  ans
@router.get("/inventory/{item_id}", response_model=InventoryResponse)
def read_inventory(item_id: int, db: Session = Depends(get_db)):
    return get_inventory(item_id, db)


@router.post("/inventory", response_model=InventoryResponse)
def add_inventory(item_data: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(item_data, db)


@router.put("/inventory/{item_id}", response_model=InventoryResponse)
def modify_inventory(item_id: int, item_data: InventoryUpdate, db: Session = Depends(get_db)):
    return update_inventory(item_id, item_data, db)


@router.delete("/inventory/{item_id}")
def remove_inventory(item_id: int, db: Session = Depends(get_db)):
    return delete_inventory(item_id, db)


@router.get("/health")
def health():
    return {"status": "ok"}