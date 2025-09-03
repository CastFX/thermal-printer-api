"""Main FastAPI application."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import router

app = FastAPI(
    title="Thermal Printer API",
    description="Local REST API for thermal printer management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


# Add health check at root level
@app.get("/health")
async def health():
    """Root level health check."""
    from .routes import health_check

    return await health_check()


# Add API overview at root level
@app.get("/")
async def root():
    """Root endpoint with API overview."""
    from .routes import api_overview

    return await api_overview()


def start_server():
    """Start the FastAPI server."""
    uvicorn.run(
        "thermal_printer_api.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=False,
    )


def start_dev_server():
    """Start the FastAPI server in development mode with auto-reload."""
    uvicorn.run(
        "thermal_printer_api.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=True,
    )


if __name__ == "__main__":
    start_server()
