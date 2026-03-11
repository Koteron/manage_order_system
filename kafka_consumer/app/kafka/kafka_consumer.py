"""
Kafka Event Consumer Service.

This module implements an asynchronous consumer that listens for 
business events (e.g., 'new_order'). It uses a distributed 
idempotency check via Redis to prevent duplicate processing.
"""
import json
import logging
import asyncio

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError

from app.config.redis import redis_client
from app.config.settings import settings
from app.celery.celery_client import process_order

logger = logging.getLogger("app")

async def start_consumer():
    """
    Main loop for consuming and dispatching Kafka messages.

    This consumer is designed for reliability and consistency using 
    Manual Commits and Redis-based deduplication.

    Process Flow:
    1. Subscribes to configured topics (e.g., 'new_order') using a fixed group ID.
    2. Fetches messages with 'enable_auto_commit=False' to ensure 
       processing completes before marking the offset as read.
    3. **Idempotency Check**: Attempts to set a 'processed:{id}' key in 
       Redis with 'nx=True'.
    4. If the key is new: Dispatches a Celery task and commits the Kafka offset.
    5. If the key exists: Skips the message (already processed by another instance).

    Args:
        None (Uses global settings for bootstrap servers and topics).

    Raises:
        KafkaConnectionError: If the broker cluster is unreachable.
        JSONDecodeError: If the message payload is malformed.
    """
    consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPICS,
        bootstrap_servers=settings.KAFKA_URL,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        enable_auto_commit=False
    )

    while True:
        try:
            await consumer.start()
            logger.info("Consumer set up, waiting for events...")
            break
        except (KafkaConnectionError, ConnectionRefusedError):
            logger.warning("Kafka not ready... retrying in 5 seconds")
            await asyncio.sleep(5)

    try:
        async for msg in consumer:
            event = json.loads(msg.value)
            logger.info("Recieved event with order_id: %s", event['order_id'])
            created = await redis_client.set(f"processed:{event['order_id']}", "1", nx=True, ex=settings.REDIS_TTL)
            if created:
                await process_order(event['order_id'])
                await consumer.commit()
                logger.info("Processed event with order_id: %s", event['order_id'])

    finally:
        await consumer.stop()