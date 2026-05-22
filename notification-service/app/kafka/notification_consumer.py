from kafka import KafkaConsumer
import json
from .event_handler import handle_event
import time
from .notification_producer import send_event
import threading

consumer = None

# =========================
# CONNECT CONSUMER
# =========================
for i in range(10):

    try:

        print(f"⏳ Connecting to Kafka Consumer... attempt {i+1}")

        consumer = KafkaConsumer(
            "shipment-events",
            "order-events",
            "payment-events",
            "inventory-events",
            "shipment-events-retry",
            "order-events-retry",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            # auto_offset_reset="earliest",
            enable_auto_commit=False,
            # group_id="notification-group"
            group_id="notification-group-retry",
        )

        print("✅ Consumer connected")

        break

    except Exception as e:

        print(f"❌ Kafka not ready: {e}")

        time.sleep(3)

if consumer is None:

    print("🔥 Failed to connect consumer")


# =========================
# START CONSUMER
# =========================
def start_consumer():

    if not consumer:

        print("❌ Consumer not available")

        return

    def consume():

        print("🚀 Consumer thread started")

        try:

            for message in consumer:

                event = message.value

                print("📩 Event received:", event)

                try:
                    # raise Exception("TEST RETRY FAILURE")
                    # =========================
                    # REAL EVENT HANDLER
                    # =========================
                    handle_event(event)

                    print("✅ Event processed successfully")

                except Exception as e:

                    print("❌ Event processing failed:", str(e))

                    retry_count = event.get("retry_count", 0)

                    event["retry_count"] = retry_count + 1

                    print(f"🔢 Retry count = {event['retry_count']}")

                    # =========================
                    # RETRY
                    # =========================
                    if event["retry_count"] < 3:

                        print(
                            f"🔁 Sending to retry topic attempt={event['retry_count']}"
                        )

                        send_event("shipment-events-retry", event)

                    # =========================
                    # DLQ
                    # =========================
                    else:

                        print("☠️ Sending event to DLQ")

                        send_event("shipment-events-dlq", event)

                    # ✅ ONLY AFTER SUCCESS
                    # consumer.commit()

        except Exception as e:

            print("🔥 CONSUMER THREAD CRASHED:", str(e))

        finally:
            consumer.commit()

    thread = threading.Thread(target=consume)

    thread.daemon = True

    thread.start()

    print("✅ Kafka consumer background thread started")
