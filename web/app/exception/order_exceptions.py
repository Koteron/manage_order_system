"""
Order-Specific Domain Exceptions.

Specialized exceptions for the order lifecycle that map to 
standardized HTTP responses via their parent classes.
"""

from app.exception.http_exceptions import NotFoundException, BadRequestException


class OrderNotFoundException(NotFoundException):
    """
    Raised when a specific order ID does not exist in the database.
    Maps to **HTTP 404 Not Found**.
    """
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order with id=({order_id}) not found")

class OrderCreationFailExecption(BadRequestException):
    """
    Raised when an order cannot be persisted, typically due to validation 
    or database constraint failures.
    Maps to **HTTP 400 Bad Request**.
    """
    def __init__(self, creation_json: str):
        super().__init__(f"Cound not create a new order from: {creation_json}")
