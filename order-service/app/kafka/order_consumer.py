# from kafka import KafkaConsumer
# import json

# from kafka.order_producer import send_event
# from kafka.topics import ORDER_EVENTS_TOPIC, PAYMENT_EVENTS_TOPIC

# consumer = KafkaConsumer(
#     ORDER_EVENTS_TOPIC,
#     bootstrap_servers="kafka:9092",
#     group_id="payment-group",
#     #auto_offset_reset="earliest",
# enable_auto_commit = (False,)
#     value_deserializer=lambda m: json.loads(m.decode("utf-8")),
# )

# print("🚀 Payment consumer started...")


# for message in consumer:

#     event = message.value

#     print(f"📩 Event received: {event}")

#     if event["event"] == "ORDER_CREATED":

#         order_data = event["data"]

#         print("💳 Processing payment...")

#         payment_event = {
#             "event": "PAYMENT_COMPLETED",
#             "data": {
#                 "order_id": order_data["order_id"],
#                 "customer_id": order_data["customer_id"],
#                 "amount": order_data["amount"],
#                 "payment_status": "SUCCESS",
#             },
#         }

#         send_event(PAYMENT_EVENTS_TOPIC, payment_event)
