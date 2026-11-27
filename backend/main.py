import logging
from fastapi import FastAPI

from backend.config import settings
from backend.schemas import (
    EchoRequest,
    EchoResponse,
    HealthResponse,
    InfoResponse,
    RootResponse,
)
from backend.whatsapp.webhook import router as webhook_router

# Temporary: core/logging.py replaces this on Day 14.
logging.basicConfig(level=logging.INFO)
app = FastAPI(
    title="AK - Study Mate",
    description="AK, the WhatsApp AI study assistant",
    version="1.0.0",
)
app.include_router(webhook_router)


@app.get("/", response_model=RootResponse, summary="Welcome message")
def home():
    return {
        "message": "Hi, I'm AK. Welcome to Study Mate!",
        "status": "Running",
        "project": "Study Mate",
        "agent": "AK",
    }


@app.get("/health", response_model=HealthResponse, summary="Health check")
def health_check():
    return {
        "status": "healthy",
        "application": "Study Mate",
        "agent": "AK",
    }


@app.get("/info", response_model=InfoResponse, summary="App configuration")
def info():
    return {
        "app_name": settings.app_name,
        "agent_name": settings.agent_name,
        "app_version": settings.app_version,
        "debug": settings.debug,
    }


@app.post("/echo", response_model=EchoResponse, summary="Echo a message")
def echo(request: EchoRequest):
    return {
        "message": request.message,
        "length": len(request.message),
        "agent": settings.agent_name,
    }