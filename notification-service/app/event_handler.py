from app.database import SessionLocal
from app.services.notification_service import create_new_notification

def handle_event(event):
    event_type = event.get("event")
    data = event.get("data")

    if event_type == "SHIPMENT_STATUS_UPDATED":
        db = SessionLocal()

        try:
            status = data.get("status")

            if status == "SHIPPED":
                create_new_notification({
                    "customer_id": data["order_id"],   # adjust mapping if needed
                    "order_id": data["order_id"],
                    "subject": "Order Shipped",
                    "message": "Your order has been shipped 🚚",
                    "notification_type": "SHIPMENT"
                }, db)

            elif status == "DELIVERED":
                create_new_notification({
                    "customer_id": data["order_id"],
                    "order_id": data["order_id"],
                    "subject": "Order Delivered",
                    "message": "Your order has been delivered ✅",
                    "notification_type": "SHIPMENT"
                }, db)

        finally:
            db.close()


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