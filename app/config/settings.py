from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Optional
from typing_extensions import Self


class Settings(BaseSettings):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_NAME: str = "mydb"
    DB_PORT: int = 5432

    DATABASE_URL: Optional[str] = None

    DOGPILE_EXPIRATION_TIME: int = 3600
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL: float = 300.0
    REDIS_TIMEOUT: float = 10.0

    BCRYPT_ROUNDS: int = 12

    JWT_SECRET_KEY: str = "Yk0WvsJi+02ltLqzasB4UJh043oSbDTx3n2QO2qYijFjWrIm88Qhe5fRVCvPdZKY"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: float = 30.0

    LOG_LEVEL: str = "INFO"

    @model_validator(mode="after")
    def assemble_db_url(self) -> Self:
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return self


settings = Settings()