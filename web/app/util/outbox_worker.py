"""
Transactional Outbox Publisher.

This module implements the 'Polled Outbox' pattern. It monitors the 
database for pending events and publishes them to Kafka using 
distributed transactions (Exactly-Once Semantics).
"""
import json
import asyncio
import logging

from aiokafka import AIOKafkaProducer
from sqlalchemy import select, update

from app.models.outbox import Outbox
from app.config.db import get_async_session
from app.config.settings import settings


logger = logging.getLogger("app")

async def start_outbox_publisher():
    """
    Main background worker loop for relaying events from Postgres to Kafka.

    This worker ensures that messages are only marked as 'processed' in 
    the database if they have been successfully acknowledged by the 
    Kafka cluster.

    Process Flow:
    1. Polls the 'Outbox' table for up to 100 unprocessed events.
    2. Opens a Kafka transaction.
    3. Produces all events to their respective topics (based on event_type).
    4. Updates the database records to 'processed = True'.
    5. Commits both the Kafka transaction and the DB transaction.

    Retry Logic:
    In case of failure (Kafka down or DB error), the transaction is 
    aborted, and the events remain 'unprocessed' to be retried in 
    the next iteration.
    
    Notes:
        Requires a 'transactional_id' to prevent 'Zombie' producers 
        from interfering with the stream.
    """
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.KAFKA_URL}",
        transactional_id="outbox-worker"
    )
    await producer.start()

    try:
        while True:
            async for session in get_async_session():
                logger.info("Background: Checking for outbox events")
                result = await session.execute(
                    select(Outbox)
                    .where(Outbox.processed == False)
                    .limit(100)
                )

                events = result.scalars().all()

                if not events:
                    logger.info("Background: No outbox events found")
                    await asyncio.sleep(1)
                    continue

                await producer.begin_transaction()

                try:
                    for event in events:
                        await producer.send_and_wait(
                            topic=event.event_type,
                            value=json.dumps(event.payload).encode()
                        )
                    
                    event_ids = [event.id for event in events]

                    await session.execute(
                        update(Outbox)
                        .where(Outbox.id.in_(event_ids))
                        .values(processed=True)
                    )
                    await producer.commit_transaction()
                    await session.commit()
                    logger.info("Background: Processed %d event(s)", len(events))

                except Exception:
                    await producer.abort_transaction()
                    raise

            await asyncio.sleep(1)
    finally:
        await producer.stop()
