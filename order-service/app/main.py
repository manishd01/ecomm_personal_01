from fastapi import FastAPI
from app.routes.order_routes import router as order_router
from app.database import Base, engine
from app.models.order_model import Order
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include order routes
app.include_router(order_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "Order Service is running"}

# @app.on_event("startup")
# def startup():
#     #Base.metadata.create_all(bind=engine)



# cd ecommerce-microservices

# # Start all services (fresh build)
# docker-compose up -d --build

# # Or restart existing containers
# docker-compose restart

# # Check service status
# docker-compose ps

# docker-compose down -v
# docker-compose up --build
