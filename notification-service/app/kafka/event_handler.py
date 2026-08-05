from app.database import SessionLocal
from app.services.notification_service import create_new_notification

import requests
from app.models.notification_model import Notification

ORDER_SERVICE_URL = "http://order-service:8000/api"


def handle_event(event):

    event_type = event.get("event")
    data = event.get("data")

    db = SessionLocal()

    try:
        order_id = data["order_id"]

        if not order_id:
            print("❌ order_id missing in event")
            return
        response = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", timeout=3)
        if response.status_code != 200:
            raise Exception("Order service failed")

        order = response.json()

        customer_id = order["customer_id"]
        print("getting customer_id:", customer_id)
        print("other details get form eventL ----- :", data)
        # =========================
        # SHIPMENT STATUS EVENTS
        # =========================
        if event_type in ["SHIPMENT_STATUS_UPDATED", "TRACKING_UPDATED"]:

            status = data.get("status")

            notification_map = {
                "SHIPPED": {
                    "subject": "Order Shipped",
                    "message": "Your order has been shipped 🚚",
                },
                "IN_TRANSIT": {
                    "subject": "Order In Transit",
                    "message": "Your package is currently in transit 📦",
                },
                "OUT_FOR_DELIVERY": {
                    "subject": "Out For Delivery",
                    "message": "Your package is out for delivery 🚚",
                },
                "DELIVERED": {
                    "subject": "Order Delivered",
                    "message": "Your order has been delivered ✅",
                },
                "RETURN_REQUESTED": {
                    "subject": "Return Requested",
                    "message": "Your return request has been created ↩️",
                },
                "RETURNED": {
                    "subject": "Order Returned",
                    "message": "Your order has been returned successfully 📦",
                },
                "REPLACEMENT_REQUESTED": {
                    "subject": "Replacement Requested",
                    "message": "Your replacement request has been created 🔁",
                },
                "REPLACED": {
                    "subject": "Replacement Completed",
                    "message": "Your replacement order has been completed ✅",
                },
            }

            print("insite  stsatus- trakcing evetns ----")

            if status in notification_map:

                notify = notification_map[status]

            #   Before creating notification:

            existing = (
                db.query(Notification)
                .filter(
                    Notification.order_id == data["order_id"],
                    Notification.subject == notify["subject"],
                )
                .first()
            )

            if existing:
                print("⚠️ Notification already exists")
                return

            # This is called idempotency.
            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": notify["subject"],
                    "message": notify["message"],
                    "notification_type": "SHIPMENT",
                },
                db,
            )

        # =========================
        # ORDER STATUS EVENTS
        # =========================
        elif event_type == "ORDER_STATUS_UPDATED":

            status = data.get("status")

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": f"Order {status}",
                    "message": f"Your order status changed to {status} 📦",
                    "notification_type": "ORDER",
                },
                db,
            )

        elif event_type == "ORDER_CREATED":
            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Order Created",
                    "message": "Your order has been created successfully 🛒",
                    "notification_type": "ORDER",
                },
                db,
            )

        elif event_type == "PAYMENT_COMPLETED":

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Payment Successful",
                    "message": "Your payment was completed successfully 💳",
                    "notification_type": "PAYMENT",
                },
                db,
            )

        elif event_type == "INVENTORY_RESERVED":

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Inventory Reserved",
                    "message": "Items have been reserved for your order 📦",
                    "notification_type": "INVENTORY",
                },
                db,
            )

        elif event_type == "SHIPMENT_CREATED":

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Shipment Created",
                    "message": "Shipment has been created 🚚",
                    "notification_type": "SHIPMENT",
                },
                db,
            )
        elif event_type == "PAYMENT_FAILED":

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Payment Failed",
                    "message": f"Payment failed ❌ Reason: {data.get('reason')}",
                    "notification_type": "PAYMENT",
                },
                db,
            )

        elif event_type == "INVENTORY_FAILED":

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Inventory Failed",
                    "message": "Product is out of stock ❌",
                    "notification_type": "INVENTORY",
                },
                db,
            )

        elif event_type == "SHIPMENT_FAILED":

            create_new_notification(
                {
                    "customer_id": customer_id,
                    "order_id": data["order_id"],
                    "subject": "Shipment Failed",
                    "message": f"Shipment creation failed ❌ Reason: {data.get('reason')}",
                    "notification_type": "SHIPMENT",
                },
                db,
            )

    finally:
        # consumer.commit()
        db.close()


# -----


# old-> normal printing in console  only

# def handle_event(event):
#     event_type = event.get("event")
#     data = event.get("data")

#     if event_type == "SHIPMENT_STATUS_UPDATED":
#         status = data.get("status")

#         if status == "SHIPPED":
#             print(f"📦 Notification: Order {data['order_id']} has been shipped!")

#         elif status == "DELIVERED":
#             print(f"✅ Notification: Order {data['order_id']} has been delivered!")
