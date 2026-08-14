# Cancellation Policy

## When Can an Order Be Cancelled?

Customers can normally cancel an order before it has been shipped.

Cancellation availability depends on the current order status.

## Cancellation Rules

| Order Status     | Cancellation         |
| ---------------- | -------------------- |
| CREATED          | Allowed              |
| CONFIRMED        | Allowed              |
| SHIPPED          | Normally not allowed |
| OUT_FOR_DELIVERY | Not allowed          |
| DELIVERED        | Not allowed          |

## Cancellation Process

When a cancellation request is received:

1. The order status is checked.
2. Cancellation eligibility is verified.
3. Payment status is checked.
4. If eligible, the order is cancelled.
5. A refund may be initiated if payment was already completed.
6. A cancellation event is published.
7. The customer receives a notification.

## Cancellation After Shipment

An order that has already been shipped normally cannot be cancelled through the standard cancellation process.

The customer may instead need to wait for delivery and request a return if the product is eligible.

## Payment During Cancellation

If payment has already been completed and the cancellation is approved, the refund process follows the refund policy.
