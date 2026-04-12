from fastapi import FastAPI
from app.routes.shipping_routes import router as shipping_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Shipping Service",
    description="Microservice for handling shipments and delivery tracking",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include shipping routes
app.include_router(shipping_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "Shipping Service is running"}
