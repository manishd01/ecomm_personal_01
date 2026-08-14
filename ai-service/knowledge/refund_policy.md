# Refund Policy

## Refund Eligibility

A refund may be issued when:

- An eligible product is successfully returned.
- An order is cancelled before shipment.
- A payment was successfully charged but the order could not be fulfilled.
- The customer receives an incorrect or damaged product and the claim is approved.

## Refund Method

Refunds are normally processed using the original payment method.

For example:

- Credit card payment → refund to the same card.
- Debit card payment → refund to the same card.
- UPI payment → refund to the original UPI payment source.

## Refund Processing Time

After a return is approved and the returned product passes inspection, the refund is initiated.

The time required for the amount to appear in the customer's account depends on the payment provider.

## Refund Status

Possible refund states include:

- REFUND_PENDING
- REFUND_INITIATED
- REFUND_PROCESSING
- REFUND_COMPLETED
- REFUND_FAILED

## Failed Refunds

If a refund fails, the payment service should record the failure and the customer should be notified.

Customers should not be charged again for a failed refund attempt.
