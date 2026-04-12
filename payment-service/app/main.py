from fastapi import FastAPI
from app.routes.payment_routes import router as payment_router
from app.database import Base, engine
from app.models.payment_model import Payment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include payment routes
app.include_router(payment_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "Payment Service is running"}

# @app.on_event("startup")
# def startup():
#     #Base.metadata.create_all(bind=engine)