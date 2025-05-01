import os
import yaml
import logging
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, logging_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load configuration
def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml"""
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

config = load_config()

# Create FastAPI application
app = FastAPI(
    title=config.get("app", {}).get("name", "Fitness Coach AI"),
    description="An intelligent assistant that helps users manage their fitness journey",
    version=config.get("app", {}).get("version", "0.1.0"),
)

# Configure CORS
origins_str = os.getenv("CORS_ORIGINS", "[]")
try:
    origins_list = eval(origins_str)  # Convert string to list
except:
    origins_list = ["http://localhost:3000"]  # Default fallback

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from src.api.routes.health import router as health_router
from src.api.routes.chat import router as chat_router

# Include routers
app.include_router(health_router)
app.include_router(chat_router, prefix="/api/v1")

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint that welcomes users to the API"""
    return {
        "message": "Welcome to the Fitness Coach AI API",
        "docs": "/docs",
        "health": "/health",
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"Starting Fitness Coach AI API server on {host}:{port}")
    uvicorn.run("src.main:app", host=host, port=port, reload=True)