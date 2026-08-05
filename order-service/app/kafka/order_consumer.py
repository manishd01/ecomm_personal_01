from kafka import KafkaConsumer
import json
import threading
import time

from common_logging.logging_config import setup_logger

logger = setup_logger("order-service")

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


def start_consumer():

    global consumer_inventory
    global consumer_payment
    global consumer_shipment

    # ====================================
    # CONNECT TO KAFKA
    # ====================================

    for i in range(10):

        try:

            logger.info(
                "Connecting order consumers to Kafka",
                extra={
                    "component": "kafka_consumer",
                    "operation": "CONNECT",
                    "attempt": i + 1,
                    "topics": [
                        INVENTORY_EVENTS_TOPIC,
                        PAYMENT_EVENTS_TOPIC,
                        SHIPMENT_EVENTS_TOPIC,
                    ],
                    "status": "STARTED",
                },
            )

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

            logger.info(
                "Order Kafka consumers connected successfully",
                extra={
                    "component": "kafka_consumer",
                    "operation": "CONNECT",
                    "status": "SUCCESS",
                },
            )

            break

        except Exception as e:

            logger.exception(
                f"Kafka consumer connection attempt failed: {e}",
                extra={
                    "component": "kafka_consumer",
                    "operation": "CONNECT",
                    "attempt": i + 1,
                    "status": "FAILED",
                },
            )

            time.sleep(3)

    # =====================================================
    # ADD THIS HERE
    # =====================================================

    if (
        consumer_inventory is None
        or consumer_payment is None
        or consumer_shipment is None
    ):
        logger.error(
            "Failed to connect to Kafka after 10 attempts. Consumers not started.",
            extra={
                "component": "kafka_consumer",
                "status": "FAILED",
            },
        )
        return
    # ====================================
    # CONSUME INVENTORY EVENTS
    # ====================================

    def consume_inventory():

        logger.info(
            "Inventory consumer thread started",
            extra={
                "component": "inventory_consumer",
                "topic": INVENTORY_EVENTS_TOPIC,
                "status": "STARTED",
            },
        )
        if consumer_inventory is None:
            return
        for message in consumer_inventory:

            event = message.value

            logger.info(
                "Inventory event received",
                extra={
                    "component": "inventory_consumer",
                    "event": event.get("event"),
                    "status": "RECEIVED",
                },
            )

            try:

                # ====================================
                # INVENTORY FAILED
                # ====================================

                if event["event"] == "INVENTORY_FAILED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "failed")

                    logger.info(
                        "Order marked FAILED due to inventory failure",
                        extra={
                            "order_id": data["order_id"],
                            "component": "inventory_consumer",
                            "status": "SUCCESS",
                        },
                    )

                consumer_inventory.commit()

            except Exception as e:

                logger.exception(
                    "Inventory consumer processing error",
                    extra={
                        "component": "inventory_consumer",
                        "status": "FAILED",
                    },
                )

    # ====================================
    # CONSUME PAYMENT EVENTS
    # ====================================

    def consume_payment():

        logger.info(
            "Payment consumer thread started",
            extra={
                "component": "payment_consumer",
                "topic": PAYMENT_EVENTS_TOPIC,
                "status": "STARTED",
            },
        )

        if consumer_payment is None:
            return

        for message in consumer_payment:

            event = message.value

            logger.info(
                "Payment event received",
                extra={
                    "component": "payment_consumer",
                    "event": event.get("event"),
                    "status": "RECEIVED",
                },
            )

            try:

                # ====================================
                # PAYMENT FAILED
                # ====================================

                if event["event"] == "PAYMENT_FAILED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "failed")

                    logger.info(
                        "Order marked FAILED due to payment failure",
                        extra={
                            "order_id": data["order_id"],
                            "component": "payment_consumer",
                            "status": "SUCCESS",
                        },
                    )

                consumer_payment.commit()

            except Exception as e:

                logger.exception(
                    "Payment consumer processing error",
                    extra={
                        "component": "payment_consumer",
                        "status": "FAILED",
                    },
                )

    # ====================================
    # CONSUME SHIPMENT EVENTS
    # ====================================

    def consume_shipment():

        logger.info(
            "Shipment consumer thread started",
            extra={
                "component": "shipment_consumer",
                "topic": SHIPMENT_EVENTS_TOPIC,
                "status": "STARTED",
            },
        )
        if consumer_shipment is None:
            return
        for message in consumer_shipment:

            event = message.value

            logger.info(
                "Shipment event received",
                extra={
                    "component": "shipment_consumer",
                    "event": event.get("event"),
                    "status": "RECEIVED",
                },
            )

            try:

                # ====================================
                # SHIPMENT CREATED
                # ====================================

                if event["event"] == "SHIPMENT_CREATED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "created")

                    logger.info(
                        "Order marked CREATED from shipment event",
                        extra={
                            "order_id": data["order_id"],
                            "component": "shipment_consumer",
                            "status": "SUCCESS",
                        },
                    )

                # ====================================
                # SHIPMENT FAILED
                # ====================================

                elif event["event"] == "SHIPMENT_FAILED":

                    data = event["data"]

                    update_order_status_service(data["order_id"], "failed")

                    logger.info(
                        "Order marked FAILED from shipment failure",
                        extra={
                            "order_id": data["order_id"],
                            "component": "shipment_consumer",
                            "status": "SUCCESS",
                        },
                    )

                consumer_shipment.commit()

            except Exception as e:

                logger.exception(
                    "Shipment consumer processing error",
                    extra={
                        "component": "shipment_consumer",
                        "status": "FAILED",
                    },
                )

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

    logger.info(
        "Order consumers running successfully",
        extra={
            "component": "kafka_consumer",
            "status": "RUNNING",
        },
    )
