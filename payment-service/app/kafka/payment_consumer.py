from kafka import KafkaConsumer
import json
import threading
import time
from datetime import datetime

from app.database import SessionLocal
from app.services.payment_service import create_new_payment

from app.kafka.payment_producer import send_event

from app.kafka.payment_topics import (
    INVENTORY_EVENTS_TOPIC,
    PAYMENT_EVENTS_TOPIC,
)

consumer = None


# =========================
# START CONSUMER
# =========================


def start_consumer():

    global consumer

    # =========================
    # RETRY KAFKA CONNECTION
    # =========================

    for i in range(10):

        try:

            print(f"⏳ Connecting to Kafka... attempt {i+1}")

            consumer = KafkaConsumer(
                INVENTORY_EVENTS_TOPIC,
                bootstrap_servers="kafka:9092",
                group_id="payment-group",
                # #auto_offset_reset="earliest",
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )

            print("✅ Payment consumer connected")

            # ✅ ONLY AFTER SUCCESS
            consumer.commit()

        except Exception as e:

            print("❌ Kafka not ready:", str(e))

            time.sleep(3)

    if consumer is None:

        print("❌ Could not connect to Kafka")
        return

    # =========================
    # CONSUMER THREAD
    # =========================

    def consume():
        global consumer

        print("🚀 Payment consumer started...")

        for message in consumer:

            event = message.value

            print(f"📩 Event received: {event}")

            # ====================================
            # HANDLE INVENTORY RESERVED
            # ====================================

            if event["event"] == "INVENTORY_RESERVED":
                print("Inventory reserved successfully")

                consumer.commit()

                # db = SessionLocal()

                # inventory_data = event["data"]

                # try:

                #     print("💳 Processing payment...")

                #     # ==========================
                #     # SAVE PAYMENT
                #     # ==========================

                #     payment_data = {
                #         "order_id": inventory_data["order_id"],
                #         "customer_id": inventory_data["customer_id"],
                #         "amount": inventory_data["amount"],
                #         "status": "SUCCESS",
                #     }

                #     payment = create_new_payment(payment_data, db)

                #     print(f"✅ Payment saved id={payment.id}")

                #     # ==========================
                #     # EMIT PAYMENT COMPLETED
                #     # ==========================

                #     send_event(
                #         PAYMENT_EVENTS_TOPIC,
                #         {
                #             "event": "PAYMENT_COMPLETED",
                #             "data": {
                #                 "payment_id": payment.id,
                #                 "order_id": inventory_data["order_id"],
                #                 "customer_id": inventory_data["customer_id"],
                #                 "product_id": inventory_data["product_id"],
                #                 "quantity": inventory_data["quantity"],
                #                 "amount": inventory_data["amount"],
                #                 "status": "SUCCESS",
                #                 "timestamp": str(datetime.utcnow()),
                #             },
                #         },
                #     )

                #     print("✅ PAYMENT_COMPLETED emitted")
                #     # ✅ ONLY AFTER SUCCESS
                #     consumer.commit()

                #     print("✅ Offset committed")

                # except Exception as e:

                #     print("❌ Payment processing failed:", str(e))

                #     # ==========================
                #     # EMIT PAYMENT FAILED
                #     # ==========================

                #     send_event(
                #         PAYMENT_EVENTS_TOPIC,
                #         {
                #             "event": "PAYMENT_FAILED",
                #             "data": {
                #                 "order_id": inventory_data["order_id"],
                #                 "customer_id": inventory_data["customer_id"],
                #                 "reason": str(e),
                #                 "timestamp": str(datetime.utcnow()),
                #             },
                #         },
                #     )

                #     print("❌ PAYMENT_FAILED emitted")
                #     time.sleep(5)

                # finally:

                #     db.close()

    thread = threading.Thread(
        target=consume,
        daemon=True,
    )

    thread.start()

    print("🔥 Payment consumer thread started")
