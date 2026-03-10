from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.db import verify_schema
from app.config.logging import setup_logging
from app.routers.order_router import order_router
from app.routers.user_router import user_router
from app.exception.global_handler import register_global_exception_handler
from app.config import redis


setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await verify_schema()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(order_router)
app.include_router(user_router)

register_global_exception_handler(app)