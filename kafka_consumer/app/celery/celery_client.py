"""
Celery Task Client.

Initializes the Celery application instance used for task dispatching. 
Acts as the interface between the Kafka Consumer and the background 
worker pool via RabbitMQ.
"""

from celery import Celery
from app.config.settings import settings

celery_client = Celery(
    "order_client",
    broker=settings.RABBITMQ_URL
)

async def process_order(order_id: int):
    celery_client.send_task(
        "tasks.process_order",
        args=[order_id]
    )