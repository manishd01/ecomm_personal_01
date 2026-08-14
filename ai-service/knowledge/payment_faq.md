# Payment FAQ

## What Payment Methods Are Supported?

The platform supports common payment methods such as:

- Credit cards
- Debit cards
- UPI
- Other supported online payment methods

Available payment methods may vary depending on the customer's location.

## Payment Failed

If a payment fails, the order should not be treated as successfully paid.

Customers should verify the payment status before attempting another payment.

## Money Deducted but Order Shows Payment Failed

Sometimes a payment provider may temporarily show a deduction even when the application records the payment as failed.

The payment service should verify the final transaction status.

If the transaction is ultimately unsuccessful, the amount should normally be reversed according to the payment provider's processing timeline.

## Duplicate Payment

If a customer believes they were charged more than once for the same order, the payment transaction records should be checked before issuing a refund.

## Payment Statuses

Possible payment statuses include:

- PENDING
- SUCCESS
- FAILED
- REFUND_PENDING
- REFUNDED
