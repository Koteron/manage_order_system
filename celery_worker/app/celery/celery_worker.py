"""
Celery Worker Configuration.

This module initializes the Celery app instance for the worker process. 
It establishes the connection to the message broker and triggers 
automatic task discovery across the application's task modules.
"""
from celery import Celery

from app.config.settings import settings

celery_app = Celery(
    "worker",
    broker=settings.RABBITMQ_URL
)

celery_app.autodiscover_tasks(['app.tasks'], force=True) 