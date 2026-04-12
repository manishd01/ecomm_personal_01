from fastapi import FastAPI
from app.routes.customer_routes import router as customer_router
from app.database import Base, engine
from app.models.customer_model import Customer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include customer routes
app.include_router(customer_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "Customer Service is running"}

# @app.on_event("startup")
# def startup():
#     #Base.metadata.create_all(bind=engine)
