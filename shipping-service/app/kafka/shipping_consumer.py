from kafka import KafkaConsumer
import json
import threading
from datetime import datetime
import random
import string
import time

# from app.database import init_db, SessionLocal
import app.database as database

from app.kafka.shipping_producer import send_event

from app.kafka.shipping_topics import (
    PAYMENT_EVENTS_TOPIC,
    SHIPMENT_EVENTS_TOPIC,
)

from app.services.shipping_service import create_shipment_service

# ====================================
# KAFKA CONSUMER
# ====================================

consumer = None


def create_kafka_consumer():

    global consumer

    max_retries = 10

    for attempt in range(max_retries):

        try:

            print(f"⏳ Connecting to Kafka... attempt {attempt + 1}")

            consumer = KafkaConsumer(
                PAYMENT_EVENTS_TOPIC,
                bootstrap_servers="kafka:9092",
                group_id="shipping-group",
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )

            print("✅ Kafka connected!")

            return

        except Exception as e:

            print(f"❌ Kafka not ready: {e}")

            time.sleep(5)

    raise Exception("🔥 Failed to connect to Kafka after retries")


# ====================================
# GENERATE TRACKING NUMBER
# ====================================


def generate_tracking_number():

    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=12,
        )
    )


# ====================================
# CONSUMER LOGIC
# ====================================


def consume():

    create_kafka_consumer()

    print("🚀 Shipping consumer started...")

    # KEEP CONSUMER ALIVE FOREVER
    while True:

        try:

            for message in consumer:

                db = None
                payment_data = {}

                try:

                    # ====================================
                    # CREATE DB SESSION
                    # ====================================

                    database.init_db()

                    db = database.SessionLocal()
                    # Why this works:
                    # database.SessionLocal always reads latest value
                    # after database.init_db() runs, SessionLocal is initialized correctly

                    event = message.value

                    print(f"📩 Event received: {event}")

                    # ====================================
                    # HANDLE PAYMENT_COMPLETED ONLY
                    # ====================================

                    if event.get("event") != "PAYMENT_COMPLETED":

                        print("⏭️ Skipping non-payment event")

                        consumer.commit()

                        continue

                    payment_data = event.get("data", {})

                    # ====================================
                    # CHECK PAYMENT STATUS
                    # ====================================

                    if payment_data.get("status", "").lower() != "success":

                        print(
                            f"❌ Payment not successful for order_id={payment_data.get('order_id')}"
                        )

                        consumer.commit()

                        continue

                    print(
                        f"🚚 Creating shipment for order_id={payment_data.get('order_id')}"
                    )

                    # ====================================
                    # CREATE SHIPMENT
                    # ====================================

                    shipment = create_shipment_service(
                        payment_data.get("order_id"),
                        db,
                    )

                    print(f"✅ Shipment created id={shipment.id}")

                    # ====================================
                    # EMIT SHIPMENT_CREATED
                    # ====================================

                    send_event(
                        SHIPMENT_EVENTS_TOPIC,
                        {
                            "event": "SHIPMENT_CREATED",
                            "data": {
                                "shipment_id": shipment.id,
                                "order_id": shipment.order_id,
                                "customer_id": payment_data.get("customer_id"),
                                "product_id": payment_data.get("product_id"),
                                "quantity": payment_data.get("quantity"),
                                "status": shipment.status,
                                "timestamp": str(datetime.utcnow()),
                            },
                        },
                    )

                    print("✅ SHIPMENT_CREATED emitted")

                    # ====================================
                    # COMMIT OFFSET
                    # ====================================

                    consumer.commit()

                    print("✅ Kafka offset committed")

                except Exception as e:

                    print(f"❌ Shipment creation failed: {str(e)}")

                    try:

                        send_event(
                            SHIPMENT_EVENTS_TOPIC,
                            {
                                "event": "SHIPMENT_FAILED",
                                "data": {
                                    "order_id": payment_data.get("order_id"),
                                    "customer_id": payment_data.get("customer_id"),
                                    "product_id": payment_data.get("product_id"),
                                    "quantity": payment_data.get("quantity"),
                                    "reason": str(e),
                                    "timestamp": str(datetime.utcnow()),
                                },
                            },
                        )

                        print("❌ SHIPMENT_FAILED emitted")

                    except Exception as kafka_error:

                        print(f"🔥 Failed to emit SHIPMENT_FAILED: {str(kafka_error)}")

                    # IMPORTANT
                    # COMMIT EVEN ON FAILURE
                    # OTHERWISE SAME MESSAGE
                    # WILL BE READ AGAIN FOREVER

                    consumer.commit()

                finally:

                    if db:
                        db.close()

        except Exception as outer_error:

            print(f"🔥 CONSUMER LOOP CRASHED: {str(outer_error)}")

            time.sleep(5)


def start_consumer():

    thread = threading.Thread(
        target=consume,
        daemon=True,
    )

    thread.start()

    print("🔥 Shipping consumer thread started")
