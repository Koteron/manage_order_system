from app.exception.http_exceptions import NotFoundException, ForbiddenException, BadRequestException


class OrderNotFoundException(NotFoundException):
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order with id=({order_id}) not found")

class OrderCreationFailExecption(BadRequestException):
    def __init__(self, creation_json: str):
        super().__init__(f"Cound not create a new order from: {creation_json}")
