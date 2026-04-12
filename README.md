# E-Commerce Microservices Application

A full-stack e-commerce microservices application with order management, inventory, customer management, payment processing, and notifications.

## Architecture

This application consists of the following microservices:

### 1. **Order Service** (Port 8000)

- Manages customer orders
- CRUD operations for orders
- Inter-service communication with other services
- **Endpoints:**
  - `GET /api/orders` - List all orders
  - `GET /api/orders/{order_id}` - Get specific order
  - `POST /api/orders` - Create new order
  - `PUT /api/orders/{order_id}` - Update order
  - `DELETE /api/orders/{order_id}` - Delete order
  - `GET /api/health` - Health check

### 2. **Inventory Service** (Port 8001)

- Manages product inventory
- Stock level management
- CRUD operations for inventory items
- **Endpoints:**
  - `GET /api/inventory` - List all items
  - `GET /api/inventory/{item_id}` - Get specific item
  - `POST /api/inventory` - Add new item
  - `PUT /api/inventory/{item_id}` - Update item
  - `DELETE /api/inventory/{item_id}` - Delete item
  - `GET /api/health` - Health check

### 3. **Customer Service** (Port 8002)

- Manages customer information
- Customer profile management
- CRUD operations for customers
- Email validation
- **Endpoints:**
  - `GET /api/customers` - List all customers
  - `GET /api/customers/{customer_id}` - Get specific customer
  - `GET /api/customers/email/{email}` - Get customer by email
  - `POST /api/customers` - Create new customer
  - `PUT /api/customers/{customer_id}` - Update customer
  - `DELETE /api/customers/{customer_id}` - Delete customer
  - `GET /api/health` - Health check

### 4. **Payment Service** (Port 8003)

- Manages payment processing
- Payment status tracking
- CRUD operations for payments
- Query payments by order
- **Endpoints:**
  - `GET /api/payments` - List all payments
  - `GET /api/payments/{payment_id}` - Get specific payment
  - `GET /api/payments/order/{order_id}` - Get payments for order
  - `POST /api/payments` - Create new payment
  - `PUT /api/payments/{payment_id}` - Update payment
  - `DELETE /api/payments/{payment_id}` - Delete payment
  - `GET /api/health` - Health check

### 5. **Notification Service** (Port 8004)

- Manages customer notifications
- Notification delivery tracking
- CRUD operations for notifications
- Query unread notifications
- **Endpoints:**
  - `GET /api/notifications` - List all notifications
  - `GET /api/notifications/{notification_id}` - Get specific notification
  - `GET /api/notifications/customer/{customer_id}` - Get customer notifications
  - `GET /api/notifications/customer/{customer_id}/unread` - Get unread notifications
  - `POST /api/notifications` - Create new notification
  - `PUT /api/notifications/{notification_id}` - Update notification
  - `DELETE /api/notifications/{notification_id}` - Delete notification
  - `GET /api/health` - Health check

### 6. **Frontend** (Port 3000)

- React-based frontend application
- User interface for the e-commerce platform

## Technology Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** MySQL
- **Authentication:** Basic CORS
- **Containerization:** Docker & Docker Compose
- **HTTP Client:** Requests library for inter-service communication

## Prerequisites

- Docker & Docker Compose installed
- Python 3.9+ (if running locally without Docker)
- MySQL 8.0+

## Installation & Running

### Using Docker Compose (Recommended)

1. **Navigate to the project directory:**

   ```bash
   cd ecommerce-microservices
   ```

2. **Start all services:**

   ```bash
   docker-compose up -d --build
   ```

   This will:
   - Build all service images
   - Create and start MySQL database
   - Start all microservices
   - Start the frontend application

3. **Access the services:**
   - Frontend: http://localhost:3000
   - Order Service: http://localhost:8000
   - Inventory Service: http://localhost:8001
   - Customer Service: http://localhost:8002
   - Payment Service: http://localhost:8003
   - Notification Service: http://localhost:8004

4. **View logs:**

   ```bash
   docker-compose logs -f [service-name]
   # Example: docker-compose logs -f order-service
   ```

5. **Stop all services:**

   ```bash
   docker-compose down
   ```

6. **Stop and remove volumes (reset data):**
   ```bash
   docker-compose down -v
   ```

### Running Individual Services Locally

Each service requires the same dependencies:

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run a service:**
   ```bash
   cd [service-name]
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Database Setup

The database is automatically initialized via `init.sql` which creates the following databases:

- `order_db` - Orders database
- `inventory_db` - Inventory database
- `customer_db` - Customers database
- `payment_db` - Payments database
- `notification_db` - Notifications database

## API Documentation

Each service provides automatic API documentation:

- **Swagger UI:** `http://localhost:[port]/docs`
- **ReDoc:** `http://localhost:[port]/redoc`

Example:

- Order Service Docs: http://localhost:8000/docs

## Inter-Service Communication

Services communicate with each other using HTTP requests. A `ServiceClient` utility is available in each service's `services/service_client.py`:

```python
from app.services.service_client import service_client

# Example: Get customer from customer service
customer = service_client.get("customer", "/customers/1")

# Example: Create a payment
payment_data = {
    "order_id": 1,
    "customer_id": 1,
    "amount": 100.00,
    "payment_method": "credit_card"
}
payment = service_client.post("payment", "/payments", payment_data)
```

## Service URLs (Internal Communication)

Services use the following internal URLs for communication:

- Order Service: `http://order-service:8000`
- Inventory Service: `http://inventory-service:8000`
- Customer Service: `http://customer-service:8000`
- Payment Service: `http://payment-service:8000`
- Notification Service: `http://notification-service:8000`

## Health Checks

Each service provides a health check endpoint:

```bash
curl http://localhost:8000/api/health
```

Response:

```json
{
  "status": "Order Service is running"
}
```

## Project Structure

```
ecommerce-microservices/
├── order-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── controllers/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── inventory-service/
├── customer-service/
├── payment-service/
├── notification-service/
├── frontend/
├── docker-compose.yml
├── init.sql
└── README.md
```

## Common Tasks

### Add a New Customer

```bash
curl -X POST http://localhost:8002/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "USA"
  }'
```

### Create an Order

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "product_id": 1,
    "quantity": 2,
    "price": 49.99
  }'
```

### Process a Payment

```bash
curl -X POST http://localhost:8003/api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "customer_id": 1,
    "amount": 99.98,
    "payment_method": "credit_card"
  }'
```

### Send a Notification

```bash
curl -X POST http://localhost:8004/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "subject": "Order Confirmation",
    "message": "Your order has been confirmed",
    "notification_type": "order_confirmation"
  }'
```

## Troubleshooting

### Services not communicating

- Ensure all services are running: `docker-compose ps`
- Check service logs: `docker-compose logs [service-name]`
- Verify MySQL is running: `docker-compose logs mysql`

### Database connection errors

- Reset databases: `docker-compose down -v && docker-compose up -d`
- Check MySQL credentials in each service's `database.py`

### Port conflicts

- Ensure ports 8000-8004 and 3000 are available
- Modify ports in `docker-compose.yml` and service code if needed

## Contributing

When adding new features:

1. Update the appropriate service
2. Add database migrations if needed
3. Update service_client.py in other services if inter-service communication is needed
4. Test with `docker-compose up -d --build`

## License

This project is provided as-is for educational purposes.
