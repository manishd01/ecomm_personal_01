from kafka import KafkaConsumer
import json
from .event_handler import handle_event
import time

consumer = None

for i in range(10):
    try:
        print(f"⏳ Connecting to Kafka Consumer... attempt {i+1}")

        consumer = KafkaConsumer(
            "shipment-events",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="notification-group"
        )

        print("✅ Consumer connected")
        break

    except Exception as e:
        print(f"❌ Kafka not ready: {e}")
        time.sleep(3)

if consumer is None:
    print("🔥 Failed to connect consumer")
    
    
    
import threading

def start_consumer():
    if not consumer:
        print("❌ Consumer not available")
        return

    def consume():
        print("🚀 Consumer started...")

        for message in consumer:
            event = message.value
            print("📩 Event received:", event)

            handle_event(event)   # ✅ NOW THIS WORKS

    thread = threading.Thread(target=consume, daemon=True)
    thread.start()