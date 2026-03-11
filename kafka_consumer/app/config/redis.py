"""
Async Redis Client Configuration.

Initializes the global 'redis-py' client used for idempotency tracking 
and shared application state. Configured with 'decode_responses=True' 
to ensure all returned values are strings rather than raw bytes.
"""

from redis.asyncio import Redis

from app.config.settings import settings


redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)