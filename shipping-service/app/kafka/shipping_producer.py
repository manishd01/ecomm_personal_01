from kafka import KafkaProducer
import json
import time

producer = None

# 🔥 RETRY LOGIC
for i in range(10):
    try:
        print(f"⏳ Connecting to Kafka... attempt {i+1}")

        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5
        )

        print("✅ Connected to Kafka")
        break

    except Exception as e:
        print(f"❌ Kafka not ready: {e}")
        time.sleep(3)

# ❗ If still not connected
if producer is None:
    print("🔥 Failed to connect to Kafka after retries")


def send_event(topic, data):
    
    if not producer:
        print("❌ Kafka producer not available")
        return

    try:
        if "retry_count" not in data:
            data["retry_count"] = 0
        
        
        producer.send(topic, data)
        producer.flush()
        print(f"📤 Event sent to {topic}: {data}")
    except Exception as e:
        print(f"❌ Failed to send event: {e}")