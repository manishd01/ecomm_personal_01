from kafka import KafkaConsumer
import json
import threading
from datetime import datetime

from app.database import SessionLocal

from app.kafka.inventory_producer import send_event

from app.kafka.inventory_topics import (
    INVENTORY_EVENTS_TOPIC,
    ORDER_EVENTS_TOPIC,
)

from app.services.inventory_service import (
    decrease_inventory_stock,
)

consumer = None


def start_consumer():

    global consumer

    try:

        consumer = KafkaConsumer(
            ORDER_EVENTS_TOPIC,
            bootstrap_servers="kafka:9092",
            group_id="inventory-group",
            # auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

        print("✅ Inventory consumer connected")

    except Exception as e:

        print("❌ Kafka connection failed:", str(e))
        return

    def consume():

        print("🚀 Inventory consumer started...")

        for message in consumer:

            event = message.value

            print(f"📩 Event received: {event}")

            # =========================
            # HANDLE ORDER CREATED
            # =========================

            if event["event"] == "ORDER_CREATED":

                db = SessionLocal()

                order_data = event["data"]

                try:

                    print("📦 Reserving inventory...")

                    item = decrease_inventory_stock(
                        item_id=order_data["product_id"],
                        quantity=order_data["quantity"],
                        db=db,
                    )

                    print("✅ Inventory updated")

                    # =========================
                    # SUCCESS EVENT
                    # =========================

                    send_event(
                        INVENTORY_EVENTS_TOPIC,
                        {
                            "event": "INVENTORY_RESERVED",
                            "data": {
                                "order_id": order_data["order_id"],
                                "customer_id": order_data["customer_id"],
                                "product_id": order_data["product_id"],
                                "quantity": order_data["quantity"],
                                "remaining_stock": item.quantity,
                                "amount": order_data["amount"],
                                "timestamp": str(datetime.utcnow()),
                            },
                        },
                    )

                    print("✅ INVENTORY_RESERVED emitted")

                    # ✅ ONLY AFTER SUCCESS
                    consumer.commit()

                except Exception as e:

                    print("❌ Inventory failed:", str(e))

                    # =========================
                    # FAILURE EVENT
                    # =========================

                    send_event(
                        INVENTORY_EVENTS_TOPIC,
                        {
                            "event": "INVENTORY_FAILED",
                            "data": {
                                "order_id": order_data["order_id"],
                                "customer_id": order_data["customer_id"],
                                "product_id": order_data["product_id"],
                                "reason": str(e),
                                "timestamp": str(datetime.utcnow()),
                            },
                        },
                    )

                    print("❌ INVENTORY_FAILED emitted")

                    consumer.commit()
                finally:
                    db.close()

    thread = threading.Thread(target=consume)

    thread.daemon = True

    thread.start()

    print("✅ Inventory consumer running in background")


# from kafka import KafkaConsumer
# import json
# from datetime import datetime

# from app.database import SessionLocal

# from app.kafka.inventory_producer import send_event

# from app.kafka.inventory_topics import (
#     PAYMENT_EVENTS_TOPIC,
#     INVENTORY_EVENTS_TOPIC,
# )

# from app.services.inventory_service import (
#     decrease_inventory_stock,
# )

# consumer = KafkaConsumer(
#     PAYMENT_EVENTS_TOPIC,
#     bootstrap_servers="kafka:9092",
#     group_id="inventory-group",
#     value_deserializer=lambda m: json.loads(m.decode("utf-8")),
# )

# print("🚀 Inventory consumer started...")


# for message in consumer:

#     event = message.value

#     print(f"📩 Event received: {event}")

#     # ====================================
#     # HANDLE PAYMENT COMPLETED
#     # ====================================

#     if event["event"] == "PAYMENT_COMPLETED":

#         db = SessionLocal()

#         try:

#             payment_data = event["data"]

#             print("📦 Reserving inventory...")

#             # ==========================
#             # DECREASE STOCK
#             # ==========================

#             item = decrease_inventory_stock(
#                 item_id=payment_data["product_id"],
#                 quantity=payment_data["quantity"],
#                 db=db,
#             )

#             print("✅ Inventory updated")

#             # ==========================
#             # EMIT INVENTORY EVENT
#             # ==========================

#             inventory_event = {
#                 "event": "INVENTORY_RESERVED",
#                 "data": {
#                     "order_id": payment_data["order_id"],
#                     "customer_id": payment_data["customer_id"],
#                     "product_id": payment_data["product_id"],
#                     "quantity": payment_data["quantity"],
#                     "remaining_stock": item.quantity,
#                     "timestamp": str(datetime.utcnow()),
#                 },
#             }

#             send_event(
#                 INVENTORY_EVENTS_TOPIC,
#                 inventory_event,
#             )

#             print("✅ INVENTORY_RESERVED event sent")

#         except Exception as e:

#             print("❌ Inventory processing failed:", str(e))

#         finally:

#             db.close()
