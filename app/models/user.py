import re

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, mapped_column, Mapped, validates

from app.models.base import Base
if TYPE_CHECKING:
    from app.models.order import Order
else:
    Order = "Order"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    @validates("email")
    def validate_email(self, key, address):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("Invalid email address")
        return address

    orders: Mapped["Order"] = relationship("Order", back_populates="user")
