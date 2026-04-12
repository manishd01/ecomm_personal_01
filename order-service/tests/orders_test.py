import pytest
import random
import requests

# since integration test: push elements in inventory and customer first
BASE_ORDER_URL = "http://order-service:8000/api/orders"
BASE_INVENTORY_URL = "http://inventory-service:8000/api/inventory"
BASE_CUSTOMER_URL = "http://customer-service:8000/api/customers"


# =========================
# 🔧 SETUP DEPENDENCIES
# =========================
@pytest.fixture(scope="session", autouse=True)
def setup_dependencies():
    # Create products (inventory)
    for i in range(1, 11):
        requests.post(BASE_INVENTORY_URL, json={
            "product_name": f"Product {i}",
            "quantity": 100,
            "price": 1000 * i
        })

    # Create customers
    for i in range(1, 11):
        requests.post(BASE_CUSTOMER_URL, json={
            "name": f"Customer {i}",
            "email": f"user{i}@test.com"
        })


# =========================
# 🔥 RANDOM ORDER
# =========================
def random_order():
    return {
        "customer_id": random.randint(1, 9),
        "product_id": random.randint(1, 9),
        "quantity": random.randint(1, 5),
        "price": random.randint(1000, 50000)
    }


# =========================
# ✅ CREATE ORDER
# =========================
def test_create_order():
    res = requests.post(BASE_ORDER_URL, json=random_order())
    assert res.status_code == 200


# =========================
# ✅ BULK CREATE
# =========================
def test_bulk_create_orders():
    for _ in range(5):
        res = requests.post(BASE_ORDER_URL, json=random_order())
        assert res.status_code == 200


# =========================
# ✅ GET ALL
# =========================
def test_get_all_orders():
    res = requests.get(BASE_ORDER_URL)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# =========================
# ✅ GET BY ID
# =========================
def test_get_order_by_id():
    create = requests.post(BASE_ORDER_URL, json=random_order())
    order = create.json()

    res = requests.get(f"{BASE_ORDER_URL}/{order['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == order["id"]


# =========================
# ✅ UPDATE
# =========================
def test_update_order():
    create = requests.post(BASE_ORDER_URL, json=random_order())
    order = create.json()

    res = requests.put(f"{BASE_ORDER_URL}/{order['id']}", json={
        "quantity": 2,
        "price": 2000
    })

    assert res.status_code == 200


# =========================
# ✅ DELETE
# =========================
def test_delete_order():
    create = requests.post(BASE_ORDER_URL, json=random_order())
    order = create.json()

    res = requests.delete(f"{BASE_ORDER_URL}/{order['id']}")
    assert res.status_code in [200, 204]


# =========================
# 🚨 VALIDATION
# =========================
def test_missing_customer():
    res = requests.post(BASE_ORDER_URL, json={
        "product_id": 1,
        "quantity": 1,
        "price": 1000
    })
    assert res.status_code == 422


def test_missing_product():
    res = requests.post(BASE_ORDER_URL, json={
        "customer_id": 1,
        "quantity": 1,
        "price": 1000
    })
    assert res.status_code == 422


# =========================
# 🚨 BUSINESS LOGIC
# =========================
def test_invalid_product():
    res = requests.post(BASE_ORDER_URL, json={
        "customer_id": 1,
        "product_id": 9999,
        "quantity": 1,
        "price": 1000
    })
    assert res.status_code in [400, 404]


def test_invalid_customer():
    res = requests.post(BASE_ORDER_URL, json={
        "customer_id": 9999,
        "product_id": 1,
        "quantity": 1,
        "price": 1000
    })
    assert res.status_code in [400, 404]


# =========================
# 🚨 EDGE CASES
# =========================
def test_negative_quantity():
    res = requests.post(BASE_ORDER_URL, json={
        "customer_id": 1,
        "product_id": 1,
        "quantity": -1,
        "price": 1000
    })
    assert res.status_code in [400, 422]


def test_invalid_order():
    res = requests.get(f"{BASE_ORDER_URL}/99999")
    assert res.status_code in [404, 200]

# import pytest
# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# created_order_ids = []

# # 🔥 Sample Orders (10 items)
# orders_payload = [
#     {"customer_id": 1, "product_id": 1, "quantity": 1, "price": 70000},
#     {"customer_id": 2, "product_id": 2, "quantity": 2, "price": 120000},
#     {"customer_id": 3, "product_id": 3, "quantity": 1, "price": 50000},
#     {"customer_id": 4, "product_id": 4, "quantity": 1, "price": 80000},
#     {"customer_id": 5, "product_id": 5, "quantity": 2, "price": 150000},
#     {"customer_id": 6, "product_id": 6, "quantity": 3, "price": 30000},
#     {"customer_id": 7, "product_id": 7, "quantity": 4, "price": 8000},
#     {"customer_id": 8, "product_id": 8, "quantity": 1, "price": 35000},
#     {"customer_id": 9, "product_id": 9, "quantity": 1, "price": 90000},
#     {"customer_id": 10, "product_id": 10, "quantity": 2, "price": 3000},
# ]


# # ✅ 1. Bulk Create Orders
# def test_bulk_create_orders():
#     for order in orders_payload:
#         response = client.post("/api/orders", json=order)
#         assert response.status_code == 200

#         data = response.json()

#         # Basic validation
#         assert data["customer_id"] == order["customer_id"]
#         assert data["product_id"] == order["product_id"]

#         created_order_ids.append(data["id"])


# # ✅ 2. Get All Orders
# def test_get_all_orders():
#     response = client.get("/api/orders")
#     assert response.status_code == 200

#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) >= 10


# # ✅ 3. Get Order By ID
# def test_get_order_by_id():
#     order_id = created_order_ids[0]

#     response = client.get(f"/api/orders/{order_id}")
#     assert response.status_code == 200

#     data = response.json()
#     assert data["id"] == order_id


# # =========================
# # 🚨 BUSINESS VALIDATIONS
# # =========================

# # ❌ Missing customer_id
# def test_missing_customer():
#     payload = {
#         "product_id": 1,
#         "quantity": 1,
#         "price": 1000
#     }

#     response = client.post("/api/orders", json=payload)
#     assert response.status_code == 422


# # ❌ Missing product_id
# def test_missing_product():
#     payload = {
#         "customer_id": 1,
#         "quantity": 1,
#         "price": 1000
#     }

#     response = client.post("/api/orders", json=payload)
#     assert response.status_code == 422


# # ❌ Quantity > stock (assuming validation exists)
# def test_quantity_exceeds_stock():
#     payload = {
#         "customer_id": 1,
#         "product_id": 1,
#         "quantity": 9999,  # unrealistic
#         "price": 999999
#     }

#     response = client.post("/api/orders", json=payload)

#     # depends on your API logic
#     assert response.status_code in [400, 409]


# # ❌ Price mismatch (quantity * unit_price validation)
# def test_price_mismatch():
#     payload = {
#         "customer_id": 1,
#         "product_id": 1,
#         "quantity": 2,
#         "price": 10  # WRONG price
#     }

#     response = client.post("/api/orders", json=payload)

#     # Expect validation failure
#     assert response.status_code in [400, 422]


# # ❌ Negative quantity
# def test_negative_quantity():
#     payload = {
#         "customer_id": 1,
#         "product_id": 1,
#         "quantity": -1,
#         "price": 1000
#     }

#     response = client.post("/api/orders", json=payload)
#     assert response.status_code in [400, 422]


# # ❌ Invalid Order ID
# def test_invalid_order():
#     response = client.get("/api/orders/99999")
#     assert response.status_code in [404, 200]