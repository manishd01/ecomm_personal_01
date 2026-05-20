from kafka import KafkaProducer
import json
import time

producer = None
# A realistic ecommerce flow:

# 1. Order Created
#         |
#         v
# 2. Inventory Reserved
#         |
#         v
# 3. Payment Processed
#         |
#         v
# 4. Shipment Created
#         |
#         v
# 5. Shipment Delivered
#         |
#         v
# 6. Notification Sent


def get_producer():

    global producer

    # already connected
    if producer is not None:
        return producer

    # retry connection
    for i in range(10):

        try:

            print(f"⏳ Connecting to Kafka... attempt {i+1}")

            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=5,
            )

            print("✅ Kafka producer connected")

            return producer

        except Exception as e:

            print(f"❌ Kafka not ready: {e}")

            time.sleep(3)

    return None


def send_event(topic: str, data: dict):

    try:

        producer = get_producer()

        if producer is None:

            print("❌ Producer unavailable")

            return

        producer.send(topic, value=data)

        producer.flush()

        print(f"✅ Event sent to Kafka topic={topic}")

    except Exception as e:

        print("⚠️ Kafka producer error:", str(e))


# from kafka import KafkaProducer
# import json


# producer = None


# def get_producer():
#     global producer

#     if producer is None:
#         producer = KafkaProducer(
#             bootstrap_servers="kafka:9092",
#             value_serializer=lambda v: json.dumps(v).encode("utf-8")
#         )

#     return producer


# def send_event(topic: str, data: dict):

#     try:
#         producer = get_producer()

#         producer.send(topic, value=data)

#         producer.flush()

#         print(f"✅ Event sent to Kafka topic={topic}")

#     except Exception as e:
#         print("⚠️ Kafka producer error:", str(e))
