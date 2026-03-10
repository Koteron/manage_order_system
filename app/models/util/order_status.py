from enum import StrEnum, auto

class OrderStatus(StrEnum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    CANCELED = auto()