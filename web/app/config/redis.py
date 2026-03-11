"""
Distributed Cache Configuration.

Initializes the global 'aiocache' settings to use Redis as the primary 
data store. Provides high-speed access to frequently requested data 
(e.g., Order details) to reduce database load.
"""
from aiocache import caches

from app.config.settings import settings


caches.set_config({
        "default": {
            "cache": "aiocache.RedisCache",
            "endpoint": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "timeout": settings.REDIS_TIMEOUT,
            "serializer": {
                "class": "aiocache.serializers.PickleSerializer"
            },
        }
    }
)

