from fastapi import FastAPI
from app.routes.notification_routes import router as notification_router
from app.database import Base, engine
from app.models.notification_model import Notification
from fastapi.middleware.cors import CORSMiddleware
import threading
from app.kafka.notification_consumer import start_consumer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include notification routes
app.include_router(notification_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "Notification Service is running"}


# @app.on_event("startup")
# def startup():
#     #Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def start_kafka():
    print("🔥 FASTAPI STARTUP RUNNING")
    start_consumer()
