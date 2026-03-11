"""
Order Persistence Model.

Defines the database schema for customer orders, including 
relationships to users and the integration of PostgreSQL-specific 
data types like JSONB for flexible item storage.
"""

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import Any

from app.models.util.order_status import OrderStatus
from app.models.base import Base
if TYPE_CHECKING:
    from app.models.user import User
else:
    User = "User"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    items: Mapped[list[dict[str, Any]]] = mapped_column(JSONB)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, native_enum=False), default=OrderStatus.PENDING)
    total_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    user: Mapped["User"] = relationship("User", back_populates="orders")
