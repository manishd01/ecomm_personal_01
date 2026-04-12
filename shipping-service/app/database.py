import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import time

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "shipping_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

# ✅ Lazy initialization with retry
engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    if engine is not None:
        return
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print("DB_HOST:", DB_HOST)
            print("DB_PORT:", DB_PORT)
            print("DB_NAME:", DB_NAME)
            print("DB_USER:", DB_USER)
            print("DB_PASSWORD:", DB_PASSWORD)
            print("DATABASE_URL:", DATABASE_URL)
            print(f"🚀 Connecting to: {DATABASE_URL} (attempt {attempt + 1}/{max_retries})")
            engine = create_engine(DATABASE_URL, echo=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            engine.connect()  # Test connection
            print("✅ Database connected!")
            break
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise

# ✅ IMPORTANT: import models BEFORE create_all
from app.models import shipping_model   # change per service

# ✅ Only for tests
if os.getenv("ENV") == "test":
    init_db()
    print("🔥 Creating tables for TEST")
    print("Tables:", Base.metadata.tables.keys())  # debug
    Base.metadata.create_all(bind=engine)

def get_db():
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()