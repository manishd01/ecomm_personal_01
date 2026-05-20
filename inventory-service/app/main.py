from fastapi import FastAPI
from app.routes.inventory_routes import router as inventory_router
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.kafka.inventory_consumer import start_consumer

# ✅ ADD THIS (IMPORTANT FIX)
from app.models.inventory_model import Inventory

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(inventory_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "Inventory Service is running"}


# @app.on_event("startup")
# def startup():
#     #Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def kafka_start():
    print("🔥 Starting inventory kafka consumer")
    start_consumer()
