from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("BetMind is starting up...")
    yield
    # Shutdown
    print("BetMind is shutting down...")

app = FastAPI(
    title="BetMind",
    description="AI-powered sports betting prediction engine",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "BetMind"}