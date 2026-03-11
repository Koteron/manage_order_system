"""
Transactional Outbox Persistence Model.

This module provides the schema for staging events that need to be 
relayed to Kafka. It acts as a temporary buffer to ensure atomicity 
between database updates and message production.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.models.base import Base


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str]
    payload: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    processed: Mapped[bool] = mapped_column(default=False)