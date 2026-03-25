from redis_om import get_redis_connection
from app.core.config import settings

# Redis Connection
redis = get_redis_connection(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)

class BaseMeta:
    database = redis
    global_key_prefix = settings.GLOBAL_KEY_PREFIX
