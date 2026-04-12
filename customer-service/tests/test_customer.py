import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

customers_payload = [
    {
        "first_name": "Amit",
        "last_name": "Sharma",
        "email": "amit.sharma@gmail.com",
        "phone": "9876543210",
        "address": "12 MG Road",
        "city": "Bengaluru",
        "state": "Karnataka",
        "postal_code": "560001",
        "country": "India"
    },
    {
        "first_name": "Priya",
        "last_name": "Verma",
        "email": "priya.verma@yahoo.com",
        "phone": "9123456780",
        "address": "45 Park Street",
        "city": "Kolkata",
        "state": "West Bengal",
        "postal_code": "700016",
        "country": "India"
    },
    {
        "first_name": "Rahul",
        "last_name": "Mehta",
        "email": "rahul.mehta@outlook.com",
        "phone": "9812345678",
        "address": "78 Andheri East",
        "city": "Mumbai",
        "state": "Maharashtra",
        "postal_code": "400069",
        "country": "India"
    },
    {
        "first_name": "Sneha",
        "last_name": "Reddy",
        "email": "sneha.reddy@gmail.com",
        "phone": "9988776655",
        "address": "22 Banjara Hills",
        "city": "Hyderabad",
        "state": "Telangana",
        "postal_code": "500034",
        "country": "India"
    },
    {
        "first_name": "Arjun",
        "last_name": "Singh",
        "email": "arjun.singh@gmail.com",
        "phone": "9090909090",
        "address": "56 Sector 17",
        "city": "Chandigarh",
        "state": "Punjab",
        "postal_code": "160017",
        "country": "India"
    },
    {
        "first_name": "Neha",
        "last_name": "Gupta",
        "email": "neha.gupta@gmail.com",
        "phone": "9345678901",
        "address": "90 Civil Lines",
        "city": "Delhi",
        "state": "Delhi",
        "postal_code": "110054",
        "country": "India"
    },
    {
        "first_name": "Karan",
        "last_name": "Patel",
        "email": "karan.patel@gmail.com",
        "phone": "9871234567",
        "address": "11 SG Highway",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "postal_code": "380015",
        "country": "India"
    },
    {
        "first_name": "Pooja",
        "last_name": "Nair",
        "email": "pooja.nair@gmail.com",
        "phone": "9123987654",
        "address": "33 Marine Drive",
        "city": "Kochi",
        "state": "Kerala",
        "postal_code": "682031",
        "country": "India"
    },
    {
        "first_name": "Rohit",
        "last_name": "Yadav",
        "email": "rohit.yadav@gmail.com",
        "phone": "9988123456",
        "address": "77 Gomti Nagar",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "postal_code": "226010",
        "country": "India"
    },
    {
        "first_name": "kanur",
        "last_name": "Yadav",
        "email": "kunanr.yadav@gmail.com",
        "phone": "9988123456",
        "address": "77 Gomti Nagar",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "postal_code": "226010",
        "country": "India"
    },
    {
        "first_name": "open",
        "last_name": "shukla",
        "email": "jsu.33@gmail.com",
        "phone": "9988123456",
        "address": "77 Gomti Nagar",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "postal_code": "226010",
        "country": "India"
    },
    {
        "first_name": "Anjali",
        "last_name": "Joshi",
        "email": "anjali.joshi@gmail.com",
        "phone": "9811223344",
        "address": "14 FC Road",
        "city": "Pune",
        "state": "Maharashtra",
        "postal_code": "411005",
        "country": "India"
    }
]

created_ids = [1,2,3]

# ✅ 1. Create Customers
def test_create_customers():
    for customer in customers_payload:
        response = client.post("http://localhost:8002/api/customers", json=customer)
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == customer["email"]

        created_ids.append(data["id"])

# ✅ 2. Get All Customers
def test_get_all_customers():
    response = client.get("http://localhost:8002/api/customers")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 10

# ✅ 3. Get Customer By ID
def test_get_customer_by_id():
    customer_id = created_ids[0]

    response = client.get(f"http://localhost:8002/api/customers/{customer_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == customer_id

# ✅ 4. Get Customer By Email
def test_get_customer_by_email():
    email = customers_payload[0]["email"]

    response = client.get(f"http://localhost:8002/api/customers/email/{email}")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == email

# ✅ 5. Update Customer
def test_update_customer():
    customer_id = created_ids[0]

    update_data = {
        "city": "UpdatedCity"
    }

    response = client.put(f"http://localhost:8002/api/customers/{customer_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["city"] == "UpdatedCity"

# ✅ 6. Delete Customer
def test_delete_customer():
    customer_id = created_ids[-1]

    response = client.delete(f"http://localhost:8002/api/customers/{customer_id}")
    assert response.status_code == 200

# =========================
# 🚨 EDGE CASES
# =========================

# ❌ Invalid ID
def test_get_invalid_customer():
    response = client.get("http://localhost:8002/api/customers/99999")
    assert response.status_code in [404, 200]  # depends on your logic

# ❌ Duplicate Email
def test_duplicate_email():
    payload = customers_payload[0]

    response = client.post("http://localhost:8002/api/customers", json=payload)
    assert response.status_code in [400, 409]

# ❌ Invalid Email Format
def test_invalid_email():
    payload = customers_payload[0].copy()
    payload["email"] = "invalid-email"

    response = client.post("http://localhost:8002/api/customers", json=payload)
    assert response.status_code in [400, 422]

# ❌ Missing Required Field
def test_missing_field():
    payload = {
        "first_name": "Test"
    }

    response = client.post("http://localhost:8002/api/customers", json=payload)
    assert response.status_code == 422

# ✅ Health Check
def test_health():
    response = client.get("http://localhost:8002/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"