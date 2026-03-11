"""
RabbitMQ and Broker Infrastructure Settings.

Uses Pydantic-Settings to manage environment-specific variables for 
the message broker. Automatically constructs the AMQP connection string 
to ensure a consistent interface for Celery workers and clients.
"""

from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing_extensions import Self
from typing import Optional


class Settings(BaseSettings):
    
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "admin"
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_URL: Optional[str] = None

    @model_validator(mode="after")
    def assemble_urls(self) -> Self:
        """
        Dynamically constructs the RabbitMQ AMQP URL.

        If 'RABBITMQ_URL' is not explicitly provided in the environment, 
        it is built using the individual host, port, and credential 
        components to create a valid 'amqp://' URI.

        Returns:
            Self: The settings instance with the populated broker URL.
        """
        if not self.RABBITMQ_URL:
            self.RABBITMQ_URL = f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}" \
                f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"
        return self

# Singleton Settings Instance
settings = Settings()