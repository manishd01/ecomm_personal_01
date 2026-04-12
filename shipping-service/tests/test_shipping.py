import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.shipping_model import Shipment

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Create tables before each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_health_check(setup_database):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_shipment(setup_database):
    """Test creating a new shipment"""
    payload = {"order_id": 123}
    response = client.post("/api/shipments/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == 123
    assert data["status"] == "CREATED"
    assert "id" in data


def test_get_shipment(setup_database):
    """Test retrieving a shipment"""
    # First create a shipment
    payload = {"order_id": 456}
    create_response = client.post("/api/shipments/", json=payload)
    shipment_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/shipments/{shipment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == shipment_id
    assert data["order_id"] == 456
    assert data["status"] == "CREATED"


def test_update_shipment_status(setup_database):
    """Test updating shipment status"""
    # Create shipment
    payload = {"order_id": 789}
    create_response = client.post("/api/shipments/", json=payload)
    shipment_id = create_response.json()["id"]
    
    # Update status CREATED -> SHIPPED
    update_payload = {"status": "SHIPPED"}
    response = client.patch(f"/api/shipments/{shipment_id}/status", json=update_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SHIPPED"


def test_invalid_status_transition(setup_database):
    """Test invalid status transition"""
    # Create shipment
    payload = {"order_id": 999}
    create_response = client.post("/api/shipments/", json=payload)
    shipment_id = create_response.json()["id"]
    
    # Try invalid transition CREATED -> DELIVERED (should be CREATED -> SHIPPED -> DELIVERED)
    update_payload = {"status": "DELIVERED"}
    response = client.patch(f"/api/shipments/{shipment_id}/status", json=update_payload)
    
    assert response.status_code == 400


def test_get_order_shipments(setup_database):
    """Test retrieving all shipments for an order"""
    order_id = 111
    
    # Create multiple shipments
    client.post("/api/shipments/", json={"order_id": order_id})
    client.post("/api/shipments/", json={"order_id": order_id})
    
    # Retrieve shipments
    response = client.get(f"/api/shipments/order/{order_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_shipment_not_found(setup_database):
    """Test retrieving non-existent shipment"""
    response = client.get("/api/shipments/9999")
    assert response.status_code == 404
