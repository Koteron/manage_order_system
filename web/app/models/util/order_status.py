"""
Order Status Enumerations.

Defines the valid lifecycle states for an order. Using StrEnum 
ensures compatibility with SQLAlchemy (PostgreSQL ENUMs) and 
FastAPI's automatic JSON serialization.
"""
from enum import StrEnum, auto

class OrderStatus(StrEnum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    CANCELED = auto()