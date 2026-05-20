from kafka import KafkaConsumer
import json
import threading
from datetime import datetime
import random
import string

from app.database import SessionLocal

from app.kafka.shipping_producer import send_event

from app.kafka.shipping_topics import (
    PAYMENT_EVENTS_TOPIC,
    SHIPMENT_EVENTS_TOPIC,
)

# from app.models.shipment_model import Shipment
from app.services.shipping_service import create_shipment_service

consumer = KafkaConsumer(
    PAYMENT_EVENTS_TOPIC,
    SHIPMENT_EVENTS_TOPIC,
    bootstrap_servers="kafka:9092",
    group_id="shipping-group",
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)


def generate_tracking_number():

    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=12,
        )
    )


def consume():

    print("🚀 Shipping consumer started...")

    for message in consumer:

        event = message.value

        print(f"📩 Event received: {event}")

        # ====================================
        # HANDLE PAYMENT COMPLETED
        # ====================================

        if event["event"] == "PAYMENT_COMPLETED":

            db = SessionLocal()

            try:

                payment_data = event["data"]

                print("🚚 Creating shipment...")

                shipment = create_shipment_service(
                    payment_data["order_id"],
                    db,
                )

                print(f"✅ Shipment created id={shipment.id}")

                # ==========================
                # EMIT SHIPMENT_CREATED
                # ==========================

                send_event(
                    SHIPMENT_EVENTS_TOPIC,
                    {
                        "event": "SHIPMENT_CREATED",
                        "data": {
                            "shipment_id": shipment.id,
                            "order_id": shipment.order_id,
                            "customer_id": payment_data["customer_id"],
                            "product_id": payment_data["product_id"],
                            "quantity": payment_data["quantity"],
                            "status": shipment.status,
                            "timestamp": str(datetime.utcnow()),
                        },
                    },
                )

                print("✅ SHIPMENT_CREATED emitted")
                # ✅ ONLY AFTER SUCCESS
                consumer.commit()

            except Exception as e:

                print("❌ Shipment creation failed:", str(e))

                # ==========================
                # EMIT SHIPMENT FAILED
                # ==========================

                send_event(
                    SHIPMENT_EVENTS_TOPIC,
                    {
                        "event": "SHIPMENT_FAILED",
                        "data": {
                            "order_id": payment_data["order_id"],
                            "customer_id": payment_data["customer_id"],
                            "reason": str(e),
                            # "timestamp": str(datetime.utcnow()),
                            # ADD THESE
                            "product_id": payment_data.get("product_id"),
                            "quantity": payment_data.get("quantity"),
                            "timestamp": str(datetime.utcnow()),
                        },
                    },
                )
                print("❌ SHIPMENT_FAILED emitted")

            finally:

                db.close()


def start_consumer():

    thread = threading.Thread(
        target=consume,
        daemon=True,
    )

    thread.start()

    print("🔥 Shipping consumer thread started")
