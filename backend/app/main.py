from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import engine, Base
from .routers import alerts, incidents, reports

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SentinelLab API",
    description="Security Operations Center API for SentinelLab",
    version="1.0.0"
)

# CORS setup
origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts.router)
app.include_router(incidents.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SentinelLab API", "docs": "/docs"}
