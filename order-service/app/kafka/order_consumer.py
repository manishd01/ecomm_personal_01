from kafka import KafkaConsumer
import json
import threading
import time

from app.database import SessionLocal

from app.services.order_service import (
    update_order_status_service,
)

from app.kafka.order_topics import (
    INVENTORY_EVENTS_TOPIC,
    PAYMENT_EVENTS_TOPIC,
    SHIPMENT_EVENTS_TOPIC,
)

consumer_inventory = None
consumer_payment = None
consumer_shipment = None


# ====================================
# START CONSUMER
# ====================================

# //multiple consumers,-> forbetter scaling->  can do i one cosumser also


def start_consumer():

    global consumer_inventory
    global consumer_payment
    global consumer_shipment

    # ====================================
    # CONNECT TO KAFKA
    # ====================================

    for i in range(10):

        try:

            print(f"⏳ Connecting order consumer... attempt {i+1}")

            consumer_inventory = KafkaConsumer(
                INVENTORY_EVENTS_TOPIC,
                bootstrap_servers="kafka:9092",
                group_id="order-group",
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )

            consumer_payment = KafkaConsumer(
                PAYMENT_EVENTS_TOPIC,
                bootstrap_servers="kafka:9092",
                group_id="order-group",
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )

            consumer_shipment = KafkaConsumer(
                SHIPMENT_EVENTS_TOPIC,
                bootstrap_servers="kafka:9092",
                group_id="order-group",
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )

            print("✅ Order consumer connected")

            break

        except Exception as e:

            print("❌ Kafka connection failed:", str(e))

            time.sleep(3)

    # ====================================
    # CONSUME INVENTORY EVENTS
    # ====================================

    def consume_inventory():

        print("🚀 Inventory event consumer started")

        for message in consumer_inventory:

            event = message.value

            print(f"📩 Inventory event: {event}")

            try:

                # ====================================
                # INVENTORY FAILED
                # ====================================

                if event["event"] == "INVENTORY_FAILED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "failed")

                    print("❌ Order marked FAILED from inventory failure")

                consumer_inventory.commit()

            except Exception as e:

                print("❌ Inventory consumer error:", str(e))

    # ====================================
    # CONSUME PAYMENT EVENTS
    # ====================================

    def consume_payment():

        print("🚀 Payment event consumer started")

        for message in consumer_payment:

            event = message.value

            print(f"📩 Payment event: {event}")

            try:

                # ====================================
                # PAYMENT FAILED
                # ====================================

                if event["event"] == "PAYMENT_FAILED":
                    print("inside failing kafka,-> payment failed.")

                    data = event["data"]

                    update_order_status_service(data["order_id"], "failed")

                    print("❌ Order marked FAILED from payment failure")

                consumer_payment.commit()

            except Exception as e:

                print("❌ Payment consumer error:", str(e))

    # ====================================
    # CONSUME SHIPMENT EVENTS
    # ====================================

    def consume_shipment():

        print("🚀 Shipment event consumer started")

        for message in consumer_shipment:

            event = message.value

            print(f"📩 Shipment event: {event}")

            try:

                # ====================================
                # SHIPMENT CREATED
                # ====================================

                if event["event"] == "SHIPMENT_CREATED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "created")

                    print("✅ Order marked CREATED")

                # ====================================
                # SHIPMENT FAILED
                # ====================================

                elif event["event"] == "SHIPMENT_FAILED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "failed")

                    print("❌ Order marked FAILED from shipment failure")

                consumer_shipment.commit()

            except Exception as e:

                print("❌ Shipment consumer error:", str(e))

    # ====================================
    # START THREADS
    # ====================================

    inventory_thread = threading.Thread(
        target=consume_inventory,
        daemon=True,
    )

    payment_thread = threading.Thread(
        target=consume_payment,
        daemon=True,
    )

    shipment_thread = threading.Thread(
        target=consume_shipment,
        daemon=True,
    )

    inventory_thread.start()
    payment_thread.start()
    shipment_thread.start()

    print("🔥 Order consumers running")
