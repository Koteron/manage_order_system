"""
Global Application Settings.

Uses Pydantic-Settings to manage environment variables for Database, 
Redis, Kafka, and Security configurations. Automatically assembles 
connection URLs during initialization to ensure consistency.
"""

from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Optional
from typing_extensions import Self


class Settings(BaseSettings):
    """
    Application Configuration Schema.

    Environment variables matching these keys (case-insensitive) will 
    override the default values. For example, setting 'DB_PASSWORD' 
    in your .env or Docker-Compose will update the 'DB_PASSWORD' attribute.

    Attributes:
        DATABASE_URL: Assembled PostgreSQL async connection string.
        REDIS_TTL: Global cache expiration time in seconds.
        JWT_SECRET_KEY: Key used for signing session tokens (Keep Secret!).
        KAFKA_URL: Assembled bootstrap server string for the producer/consumer.
        BCRYPT_ROUNDS: Work factor for password hashing security.
    """

    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_NAME: str = "mydb"
    DB_PORT: int = 5432

    DATABASE_URL: Optional[str] = None

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL: int = 300
    REDIS_TIMEOUT: float = 10.0

    BCRYPT_ROUNDS: int = 12

    JWT_SECRET_KEY: str = "Yk0WvsJi+02ltLqzasB4UJh043oSbDTx3n2QO2qYijFjWrIm88Qhe5fRVCvPdZKY"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: float = 30.0

    KAFKA_HOST: str = "kafka"
    KAFKA_PORT: int = 9092

    KAFKA_URL: Optional[str] = None

    LOG_LEVEL: str = "INFO"

    @model_validator(mode="after")
    def assemble_urls(self) -> Self:
        """
        Dynamically constructs connection strings after field validation.

        If 'DATABASE_URL' or 'KAFKA_URL' are not explicitly provided 
        as environment variables, they are built using the individual 
        host, port, and credential components.
        
        Returns:
            The initialized settings instance with validated URLs.
        """
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        if not self.KAFKA_URL:
            self.KAFKA_URL = (
                f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"
            )
        return self

# Singleton Settings Instance
settings = Settings()