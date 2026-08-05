from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.order_routes import router as order_router
from app.database import Base, engine
from app.models.order_model import Order
from app.kafka.order_consumer import start_consumer

from common_logging.logging_config import setup_logger

logger = setup_logger("order-service")

app = FastAPI()


logger.info(
    "Order service initialization started",
    extra={
        "status": "STARTED",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger.info(
    "CORS middleware configured",
    extra={
        "component": "cors_middleware",
        "status": "SUCCESS",
    },
)


# Include order routes
app.include_router(order_router, prefix="/api")


logger.info(
    "Order routes registered",
    extra={
        "component": "order_routes",
        "route_prefix": "/api",
        "status": "SUCCESS",
    },
)


@app.get("/health")
def health():

    logger.info(
        "Health check endpoint invoked",
        extra={
            "endpoint": "/health",
            "method": "GET",
            "status": "SUCCESS",
        },
    )

    return {"status": "Order Service is running"}


@app.on_event("startup")
def start_kafka():

    logger.info(
        "Starting Kafka consumer",
        extra={
            "component": "kafka_consumer",
            "status": "STARTING",
        },
    )

    try:

        start_consumer()

        logger.info(
            "Kafka consumer started",
            extra={
                "component": "kafka_consumer",
                "status": "SUCCESS",
            },
        )

    except Exception:

        logger.exception(
            "Kafka consumer startup failed",
            extra={
                "component": "kafka_consumer",
                "status": "FAILED",
            },
        )

        raise


# cd ecommerce-microservices

# # Start all services (fresh build)
# docker-compose up -d --build

# # Or restart existing containers
# docker-compose restart

# # Check service status
# docker-compose ps

# docker-compose down -v
# docker-compose up --build
