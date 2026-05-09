import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import product_router, auth_router, delivery_router, dispatch_router
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dispatch Management API", version="1.0")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
if isinstance(allowed_origins, str):
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(delivery_router.router)
app.include_router(dispatch_router.router)