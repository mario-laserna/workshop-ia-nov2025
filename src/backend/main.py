"""Top SaaS Backend - Main Application."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.companies import router as companies_router
from backend.api.health import router as health_router
from backend.api.industries import router as industries_router
from backend.api.locations import router as locations_router
from backend.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📝 Environment: {settings.environment}")
    yield
    print("👋 Shutting down...")

# inicializacion
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(companies_router, prefix="/api/v1", tags=["companies"])
app.include_router(industries_router, prefix="/api/v1", tags=["industries"])
app.include_router(locations_router, prefix="/api/v1", tags=["locations"])
