"""
Main Application Entrypoint.

Configures the FastAPI instance with:
1.  **Lifespan Management**: Handles startup tasks (DB verification, background workers).
2.  **Middleware**: CORS policy for frontend integration.
3.  **Security**: Global Rate Limiting via SlowAPI.
4.  **Routing**: Aggregates Order and User service modules.
5.  **Error Handling**: Centralized exception mapping.
"""
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.config.db import verify_schema
from app.config.logging import setup_logging
from app.routers.order_router import order_router
from app.routers.user_router import user_router
from app.exception.global_handler import register_global_exception_handler
from app.util.outbox_worker import start_outbox_publisher
from app.util.limiter import limiter
from app.config import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown lifecycle.

    Startup Actions:
    - **Schema Verification**: Ensures PostgreSQL tables exist and match models.
    - **Background Task**: Spawns the 'Outbox Publisher' as a non-blocking 
      asyncio task to relay events to Kafka.
    - **Logging**: Initializes the structured application logger.
    
    Shutdown:
    - Yields control back to the server; implicitly handles cleanup when 
      the context manager exits.
    """
    await verify_schema()
    asyncio.create_task(start_outbox_publisher())
    await setup_logging()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://dummy_origin:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(order_router)
app.include_router(user_router)

register_global_exception_handler(app)