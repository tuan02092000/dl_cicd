from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path

from app.core.config import get_settings
from app.api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("Starting YOLO26 Object Detection API...")
    print(f"Model path: {settings.MODEL_PATH}")
    
    # Pre-load model
    from app.services.detection_service import detection_service
    print("Model loaded successfully!")
    
    yield
    
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="YOLO26 Object Detection API",
    description="Object detection API using YOLO26 model from Ultralytics",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve static files for web demo
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint - redirect to demo page."""
    demo_path = Path("static/demo.html")
    if demo_path.exists():
        return FileResponse(demo_path)
    return {
        "message": "YOLO26 Object Detection API",
        "docs": "/docs",
        "api": settings.API_V1_STR
    }


@app.get("/demo")
async def demo():
    """Serve demo page."""
    demo_path = Path("static/demo.html")
    if demo_path.exists():
        return FileResponse(demo_path)
    return {"message": "Demo page not found. Please check static/demo.html"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

