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

