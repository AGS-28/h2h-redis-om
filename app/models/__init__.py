from app.models.base import redis
from app.models.user import User

# Registry — add new models here
MODEL_REGISTRY = {
    "users": User,
    "user": User, # Alias
}

__all__ = ["User", "MODEL_REGISTRY", "redis"]
