from kafka import KafkaProducer
import json
import time

from common_logging.logging_config import setup_logger

# from ....common_logging.logging_config import setup_logger
#
logger = setup_logger("order-service")

producer = None


def get_producer():

    global producer

    # already connected
    if producer is not None:

        logger.info(
            "Kafka producer reused (already connected)",
            extra={
                "component": "kafka_producer",
                "operation": "GET_PRODUCER",
                "status": "SUCCESS",
            },
        )

        return producer

    # retry connection
    for i in range(10):

        try:

            logger.info(
                "Attempting Kafka connection",
                extra={
                    "component": "kafka_producer",
                    "operation": "CONNECT",
                    "attempt": i + 1,
                    "bootstrap_servers": "kafka:9092",
                    "status": "STARTED",
                },
            )

            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=5,
            )

            logger.info(
                "Kafka producer connected successfully",
                extra={
                    "component": "kafka_producer",
                    "operation": "CONNECT",
                    "status": "SUCCESS",
                },
            )

            return producer

        except Exception as e:

            logger.warning(
                "Kafka connection attempt failed",
                extra={
                    "component": "kafka_producer",
                    "operation": "CONNECT",
                    "attempt": i + 1,
                    "status": "FAILED",
                },
            )

            time.sleep(3)

    logger.error(
        "Kafka producer failed after max retries",
        extra={
            "component": "kafka_producer",
            "operation": "CONNECT",
            "status": "FAILED",
        },
    )

    return None


def send_event(topic: str, data: dict):

    try:

        producer = get_producer()

        if producer is None:

            logger.error(
                "Kafka producer unavailable, event not sent",
                extra={
                    "component": "kafka_producer",
                    "operation": "SEND_EVENT",
                    "topic": topic,
                    "status": "FAILED",
                },
            )

            return

        producer.send(topic, value=data)
        producer.flush()

        logger.info(
            "Kafka event published successfully",
            extra={
                "component": "kafka_producer",
                "operation": "SEND_EVENT",
                "topic": topic,
                "status": "SUCCESS",
            },
        )

    except Exception as e:

        logger.exception(
            "Kafka producer error while sending event",
            extra={
                "component": "kafka_producer",
                "operation": "SEND_EVENT",
                "topic": topic,
                "status": "FAILED",
            },
        )


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
