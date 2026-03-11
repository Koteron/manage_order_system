import asyncio
from app.kafka.kafka_consumer import start_consumer
from app.config.logging import setup_logging

async def main():
    await setup_logging()
    await start_consumer()


if __name__ == "__main__":
    asyncio.run(main())