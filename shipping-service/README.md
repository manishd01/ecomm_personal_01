# Shipping Service

A microservice responsible for handling shipments, tracking deliveries, and coordinating with the Order Service.

## Features

✅ Create shipments for orders  
✅ Update shipment status with validated transitions  
✅ Track delivery status  
✅ Integrate with Order Service  
✅ Database migrations with Alembic

## Architecture

```
Order Service → Shipping Service → Delivery → Order Service updates status
```

## API Endpoints

### Create Shipment

```
POST /api/shipments/
Body: { "order_id": 123 }
Response: { "id": 1, "order_id": 123, "status": "CREATED", ... }
```

### Get Shipment

```
GET /api/shipments/{shipment_id}
Response: { "id": 1, "order_id": 123, "status": "SHIPPED", ... }
```

### Update Status

```
PATCH /api/shipments/{shipment_id}/status
Body: { "status": "SHIPPED" }
Response: { "id": 1, "order_id": 123, "status": "SHIPPED", ... }
```

### Get Order Shipments

```
GET /api/shipments/order/{order_id}
Response: [{ "id": 1, ... }, { "id": 2, ... }]
```

## Status Lifecycle

```
CREATED → SHIPPED → DELIVERED
```

Valid transitions are enforced:

- `CREATED` can transition to `SHIPPED`
- `SHIPPED` can transition to `DELIVERED`
- `DELIVERED` has no valid transitions (final state)

## Database Models

### Shipment

- `id` (Integer, Primary Key)
- `order_id` (Integer)
- `status` (String) - CREATED, SHIPPED, DELIVERED
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start service
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Integration with Order Service

When a shipment is created, the Shipping Service automatically notifies the Order Service:

```python
notify_order_shipped(order_id)
```

This updates the order status to `SHIPPED`.

## Testing

```bash
pytest tests/
```

## Docker

```bash
docker build -t shipping-service:latest .
docker run -e DATABASE_URL=postgresql://... shipping-service:latest
```
