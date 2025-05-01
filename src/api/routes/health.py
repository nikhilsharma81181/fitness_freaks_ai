from fastapi import APIRouter, Depends
from typing import Dict, Any
import os
import yaml

router = APIRouter(tags=["Health"])

def get_config() -> Dict[str, Any]:
    """Load configuration from config.yaml"""
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise {}
      
@router.get("/health")
async def health_check(config: Dict[str, Any] = Depends(get_config)):
    """Health check endpoint for the API"""
    return {
        "status": "ok",
        "version": config.get("app", {}).get("version", "0.1.0"),
        "environment": os.getenv("ENV", "development"),
        "llm_provider": os.getenv("LLM_PROVIDER", config.get("llm", {}).get("default_provider", "gemini")),
    }
    

