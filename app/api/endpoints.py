from fastapi import APIRouter, HTTPException
from typing import Any
from app.schemas.query import QueryRequest
from app.services.query_service import execute_query
from app.models.base import redis
from loguru import logger

router = APIRouter()

@router.post("/query")
async def query_endpoint(req: QueryRequest):
    """
    Query models with dynamic filters (ORM-style).
    """
    try:
        results, total = execute_query(
            req.model, 
            req.filters, 
            req.limit, 
            req.offset, 
            req.sort_by, 
            req.sort_asc, 
            req.fields
        )
        return {"data": results, "total": total}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/key/{full_key:path}")
async def get_key_endpoint(full_key: str):
    """
    Directly retrieve a Redis key value.
    """
    from app.core.config import settings
    
    # Auto-prefix logic
    prefix = settings.GLOBAL_KEY_PREFIX
    actual_key = full_key if full_key.startswith(f"{prefix}:") else f"{prefix}:{full_key}"
    
    try:
        key_type = redis.type(actual_key)
        if key_type == "none":
            raise HTTPException(status_code=404, detail=f"Key '{actual_key}' not found")
        
        # Handle different Redis types
        if key_type == "ReJSON-RL":
            value = redis.json().get(actual_key)
        elif key_type == "string":
            value = redis.get(actual_key)
        elif key_type == "list":
            value = redis.lrange(actual_key, 0, -1)
        elif key_type == "hash":
            value = redis.hgetall(actual_key)
        else:
            value = redis.get(actual_key)
        
        return {
            "key": actual_key, 
            "type": key_type, 
            "value": value
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving key {actual_key}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Service health check."""
    return {"status": "ok", "service": "sian-redis-om-service"}
