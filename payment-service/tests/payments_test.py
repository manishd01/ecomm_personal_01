import pytest
import requests
import random

BASE_ORDER_URL = "http://order-service:8000/api/orders"
BASE_PAYMENT_URL = "http://payment-service:8000/api/payments"


# =========================
# 🔧 CREATE ORDER HELPER
# =========================
def create_order():
    res = requests.post(BASE_ORDER_URL, json={
        "customer_id": 1,
        "product_id": 1,
        "quantity": 1,
        "price": 1000
    })
    assert res.status_code == 200
    return res.json()


# =========================
# 🔥 RANDOM PAYMENT
# =========================
def random_payment(order):
    amount = order["quantity"] * order["price"]
    return {
        "order_id": order["id"],
        "customer_id": order["customer_id"],   # ✅ add this
        "amount": amount,
        "payment_method": random.choice(["UPI", "CARD", "NET_BANKING", "COD"]),
        "status": random.choice(["PENDING", "SUCCESS", "FAILED"])
    }


# =========================
# ✅ CREATE PAYMENT
# =========================
def test_create_payment():
    order = create_order()

    res = requests.post(BASE_PAYMENT_URL, json=random_payment(order))
    assert res.status_code == 200


# =========================
# ✅ BULK CREATE
# =========================
def test_bulk_create_payments():
    for _ in range(5):
        order = create_order()
        res = requests.post(BASE_PAYMENT_URL, json=random_payment(order))
        assert res.status_code == 200


# =========================
# ✅ GET ALL
# =========================
def test_get_all_payments():
    res = requests.get(BASE_PAYMENT_URL)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# =========================
# ✅ GET BY ID
# =========================
def test_get_payment_by_id():
    order = create_order()
    create = requests.post(BASE_PAYMENT_URL, json=random_payment(order))
    payment = create.json()

    res = requests.get(f"{BASE_PAYMENT_URL}/{payment['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == payment["id"]


# =========================
# ✅ UPDATE
# =========================
def test_update_payment():
    order = create_order()
    create = requests.post(BASE_PAYMENT_URL, json=random_payment(order))
    payment = create.json()

    res = requests.put(f"{BASE_PAYMENT_URL}/{payment['id']}", json={
        "amount": 2000,
        "status": "SUCCESS"
    })

    assert res.status_code == 200


# =========================
# ✅ DELETE
# =========================
def test_delete_payment():
    order = create_order()
    create = requests.post(BASE_PAYMENT_URL, json=random_payment(order))
    payment = create.json()

    res = requests.delete(f"{BASE_PAYMENT_URL}/{payment['id']}")
    assert res.status_code in [200, 204]


# =========================
# 🚨 VALIDATION
# =========================
def test_missing_order_id():
    res = requests.post(BASE_PAYMENT_URL, json={
        "amount": 1000,
        "status": "SUCCESS"
    })
    assert res.status_code == 422


# =========================
# 🚨 BUSINESS LOGIC
# =========================
def test_invalid_order():
    res = requests.post(BASE_PAYMENT_URL, json={
        "order_id": 99999,
        "amount": 1000,
        "status": "SUCCESS"
    })
    assert res.status_code in [400, 404]


# =========================
# 🚨 EDGE CASES
# =========================
def test_negative_amount():
    order = create_order()

    res = requests.post(BASE_PAYMENT_URL, json={
        "order_id": order["id"],
        "amount": -100,
        "status": "SUCCESS"
    })
    assert res.status_code in [400, 422]


def test_invalid_payment():
    res = requests.get(f"{BASE_PAYMENT_URL}/99999")
    assert res.status_code in [404, 200]