from fastapi import APIRouter, Depends
from typing import Annotated

from app.config.security import get_current_user
from app.services.order_service import get_order_service, OrderService
from app.schemas.order_dtos import OrderDTO, OrderCreateDTO, OrderStatusDTO
from app.schemas.error_response import ErrorResponse
from app.models.user import User

order_router = APIRouter(prefix='/orders', tags=["orders"])

@order_router.get('/{order_id}/', responses={
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Order does not belong to requester"},
    404: {"model": ErrorResponse, "description": "Not found"},
})
async def get_order(
    order_id : int,
    service: Annotated[OrderService, Depends(get_order_service)]
) -> OrderDTO:
    return await service.get_order(
        order_id=order_id
    )

@order_router.get('/user/{user_id}/', responses={
    403: {"model": ErrorResponse, "description": "Order does not belong to requester"},
})
async def get_orders_by_user(
    user_id: int,
    service: Annotated[OrderService, Depends(get_order_service)]
) -> list[OrderDTO]:
    return await service.get_orders_by_user(user_id=user_id)

@order_router.post('/', responses={
    400: {"model": ErrorResponse, "description": "Could not create order"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
})
async def create_order(
    order_creation_dto: OrderCreateDTO,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[OrderService, Depends(get_order_service)]
) -> OrderDTO:
    return await service.create_order(
        requester_id=current_user.id, 
        order_create_dto=order_creation_dto
    )

@order_router.patch('/{order_id}/', responses={
    404: {"model": ErrorResponse, "description": "Not found"},
})
async def update_order_status(
    order_id: int,
    status_dto: OrderStatusDTO,
    service: Annotated[OrderService, Depends(get_order_service)]
):
    return await service.update_order_status(
        order_id=order_id,
        status_dto=status_dto
    )