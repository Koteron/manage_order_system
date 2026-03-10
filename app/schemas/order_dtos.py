from datetime import datetime
from pydantic import BaseModel, Field

from app.models.util.order_status import OrderStatus

class OrderStatusDTO(BaseModel):
    status: OrderStatus

class OrderDTO(BaseModel):
    id: int
    user_id: int
    items: list
    status: OrderStatus
    total_price: float = Field(ge=0.0)
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class OrderCreateDTO(BaseModel):
    items: list
    total_price: float = Field(ge=0.0)
