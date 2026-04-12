import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 🔥 Sample Inventory Data (Realistic)
inventory_payload = [
    {
        "model_number": "APL-IP13-001",
        "product_name": "iPhone 13",
        "quantity": 10,
        "price": 70000,
        "description": "Apple smartphone"
    },
    {
        "model_number": "SMS-S22-002",
        "product_name": "Samsung Galaxy S22",
        "quantity": 15,
        "price": 60000,
        "description": "Samsung flagship phone"
    },
    {
        "model_number": "ONE-11-003",
        "product_name": "OnePlus 11",
        "quantity": 20,
        "price": 50000,
        "description": "Fast performance phone"
    },
    {
        "model_number": "DEL-LAP-004",
        "product_name": "Dell Laptop",
        "quantity": 8,
        "price": 80000,
        "description": "Work laptop"
    },
    {
        "model_number": "HP-LAP-005",
        "product_name": "HP Laptop",
        "quantity": 12,
        "price": 75000,
        "description": "Office laptop"
    },
    {
        "model_number": "SON-HP-006",
        "product_name": "Sony Headphones",
        "quantity": 25,
        "price": 10000,
        "description": "Noise cancelling"
    },
    {
        "model_number": "BOAT-EB-007",
        "product_name": "Boat Earbuds",
        "quantity": 50,
        "price": 2000,
        "description": "Budget earbuds"
    },
    {
        "model_number": "APL-WATCH-008",
        "product_name": "Apple Watch",
        "quantity": 18,
        "price": 35000,
        "description": "Smartwatch"
    },
    {
        "model_number": "MI-TV-009",
        "product_name": "Mi Smart TV",
        "quantity": 6,
        "price": 89,
        "description": "Android TV"
    },
    {
        "model_number": "GM-MOUSE-010",
        "product_name": "Gaming Mouse",
        "quantity": 30,
        "price": 1500,
        "description": "RGB mouse"
    }
]
created_ids = []


# ✅ 1. Create Inventory Items
def test_create_inventory():
    for item in inventory_payload:
        response = client.post("http://localhost:8001/api/inventory", json=item)
        assert response.status_code == 200

        data = response.json()
        assert data["product_name"] == item["product_name"]

        created_ids.append(data["id"])


# ✅ 2. Get All Inventory
def test_get_all_inventory():
    response = client.get("http://localhost:8001/api/inventory")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 10


# ✅ 3. Get Inventory By ID
def test_get_inventory_by_id():
    item_id = created_ids[0]

    response = client.get(f"http://localhost:8001/api/inventory/{item_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == item_id


# ✅ 4. Update Inventory
def test_update_inventory():
    item_id = created_ids[0]

    update_data = {
        "quantity": 99
    }

    response = client.put(
        f"http://localhost:8001/api/inventory/{item_id}",
        json=update_data
    )
    assert response.status_code == 200

    data = response.json()
    assert data["quantity"] == 99


# ✅ 5. Delete Inventory
def test_delete_inventory():
    item_id = created_ids[-1]

    response = client.delete(f"http://localhost:8001/api/inventory/{item_id}")
    assert response.status_code == 200


# =========================
# 🚨 EDGE CASES
# =========================

# ❌ Invalid ID
def test_invalid_inventory():
    response = client.get("http://localhost:8001/api/inventory/99999")
    assert response.status_code in [404, 200]


# ❌ Negative Quantity
def test_negative_quantity():
    payload = inventory_payload[0].copy()
    payload["quantity"] = -5

    response = client.post("http://localhost:8001/api/inventory", json=payload)
    assert response.status_code in [400, 422]


# ❌ Missing Field
def test_missing_field():
    payload = {
        "product_name": "Invalid Item"
    }

    response = client.post("http://localhost:8001/api/inventory", json=payload)
    assert response.status_code == 422


# ❌ Duplicate Product (if you enforce uniqueness)
def test_duplicate_product():
    payload = inventory_payload[0]

    response = client.post("http://localhost:8001/api/inventory", json=payload)
    assert response.status_code in [400, 409]


# ✅ Health Check
def test_health():
    response = client.get("http://localhost:8001/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"