"""
Infrastructure Settings and URL Assembler.

Centralizes all environment-specific variables. Uses Pydantic-Settings 
to automatically inject values from the OS environment or .env files, 
ensuring a '12-Factor App' configuration style.
"""
from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Optional
from typing_extensions import Self


class Settings(BaseSettings):
    
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "admin"
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_URL: Optional[str] = None

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 1
    REDIS_TTL: int = 86000

    KAFKA_HOST: str = "kafka"
    KAFKA_PORT: int = 9092
    KAFKA_URL: Optional[str] = None
    KAFKA_TOPICS: tuple = ("new_order",)
    KAFKA_CONSUMER_GROUP: str = "kafka-consumer-service"

    @model_validator(mode="after")
    def assemble_urls(self) -> Self:
        """
        Dynamically constructs RabbitMQ and Kafka connection strings.

        This validator runs after basic field validation, concatenating 
        host, port, and credentials into standard protocol formats 
        (AMQP and Plaintext).

        Returns:
            Self: The settings instance with fully populated URL fields.
        """
        if not self.KAFKA_URL:
            self.KAFKA_URL = f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"
        if not self.RABBITMQ_URL:
            self.RABBITMQ_URL = f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}" \
                f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"
        return self

# Singleton Settings Instance
settings = Settings()