import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Service URLs mapping
SERVICES = {
    "order": "http://order-service:8000",
    "inventory": "http://inventory-service:8000",
    "payment": "http://payment-service:8000",
    "customer": "http://customer-service:8000",
    "notification": "http://notification-service:8000",
}


class ServiceClient:
    """Client for making inter-service HTTP calls"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get(self, service: str, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make GET request to another service"""
        try:
            url = f"{SERVICES.get(service, '')}/api{endpoint}"
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling {service} service: {str(e)}")
            return None

    def post(self, service: str, endpoint: str, data: Dict) -> Optional[Dict]:
        """Make POST request to another service"""
        try:
            url = f"{SERVICES.get(service, '')}/api{endpoint}"
            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling {service} service: {str(e)}")
            return None

    def put(self, service: str, endpoint: str, data: Dict) -> Optional[Dict]:
        """Make PUT request to another service"""
        try:
            url = f"{SERVICES.get(service, '')}/api{endpoint}"
            response = requests.put(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling {service} service: {str(e)}")
            return None

    def delete(self, service: str, endpoint: str) -> Optional[Dict]:
        """Make DELETE request to another service"""
        try:
            url = f"{SERVICES.get(service, '')}/api{endpoint}"
            response = requests.delete(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling {service} service: {str(e)}")
            return None


# Singleton instance
service_client = ServiceClient()


# Helper functions for common operations
def get_customer(customer_id: int) -> Optional[Dict]:
    """Get customer from customer service"""
    return service_client.get("customer", f"/customers/{customer_id}")


def get_inventory_item(item_id: int) -> Optional[Dict]:
    """Get inventory item from inventory service"""
    return service_client.get("inventory", f"/inventory/{item_id}")


def create_payment(payment_data: Dict) -> Optional[Dict]:
    """Create payment in payment service"""
    return service_client.post("payment", "/payments", payment_data)


def get_order_payments(order_id: int) -> Optional[Dict]:
    """Get payments for an order"""
    return service_client.get("payment", f"/payments/order/{order_id}")


def send_notification(notification_data: Dict) -> Optional[Dict]:
    """Send notification through notification service"""
    return service_client.post("notification", "/notifications", notification_data)


def get_customer_notifications(customer_id: int) -> Optional[Dict]:
    """Get customer notifications"""
    return service_client.get("notification", f"/notifications/customer/{customer_id}")
