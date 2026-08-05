from kafka import KafkaProducer
import json
import time

producer = None

# Retry Kafka connection
for i in range(10):

    try:
        print(f"⏳ Connecting Producer... attempt {i+1}")

        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
        )

        print("✅ Producer connected")
        break

    except Exception as e:

        print(f"❌ Kafka producer not ready: {e}")
        time.sleep(3)

if producer is None:
    print("🔥 Failed to connect producer")


def send_event(topic, data):

    if not producer:
        print("❌ Producer unavailable")
        return

    try:

        if "retry_count" not in data:
            data["retry_count"] = 0

        producer.send(topic, data)
        producer.flush()

        print(f"📤 Event sent to {topic}: {data}")

    except Exception as e:

        print(f"❌ Failed to send event: {e}")
