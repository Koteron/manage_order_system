import logging

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from aiocache import Cache
from aiocache.decorators import cached
from fastapi import Depends

from app.config.db import get_async_session
from app.config.settings import settings
from app.schemas.order_dtos import OrderDTO, OrderStatusDTO, OrderCreateDTO
from app.models.order import Order
from app.exception.order_exceptions import OrderNotFoundException, OrderCreationFailExecption


logger = logging.getLogger("app")

def get_order_service(session: AsyncSession = Depends(get_async_session)):
    return OrderService(session)

class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, requester_id: int, order_create_dto: OrderCreateDTO) -> OrderDTO:
        try:
            query_result = await self.session.execute(
                insert(Order)
                .values(user_id=requester_id, **(order_create_dto.model_dump()))
                .returning(Order)
            )
            order = query_result.scalar_one()
        except IntegrityError or NoResultFound as e:
            logger.error("Error while creating order: %s", e)
            raise OrderCreationFailExecption(order_create_dto.model_dump_json()) from e
        
        await self.session.commit()
        logger.info("Created order with id: %d", order.id)

        return OrderDTO.model_validate(order)
    
    def _order_key_builder(func, self, order_id):
        return f"order:{order_id}"

    @cached(ttl=settings.REDIS_TTL, key_builder=_order_key_builder)
    async def get_order(self, order_id: int) -> OrderDTO:
        logger.info("Cache MISS on id: %d, querying database", order_id)
        query_result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = query_result.scalar_one_or_none()

        if order is None:
            raise OrderNotFoundException(order_id=order_id)
        
        return OrderDTO.model_validate(order)
        
    async def update_order_status(self, order_id: int, status_dto: OrderStatusDTO) -> OrderDTO:
        query_result = await self.session.execute(
            select(Order)
            .where(Order.id == order_id)
            .with_for_update()
        )
        order = query_result.scalar_one_or_none()

        if order is None:
            raise OrderNotFoundException(order_id=order_id)
        
        order.status = status_dto.status

        await self.session.commit()
        await Cache().set(f"order:{order_id}", OrderDTO.model_validate(order))
        logger.info("Order with id=%d, set status %s", order_id, status_dto.status)

        return OrderDTO.model_validate(order)
        
    async def get_orders_by_user(self, user_id: int) -> list[OrderDTO]:
        query_result = await self.session.execute(select(Order).where(Order.user_id == user_id))
        orders = query_result.scalars().all()

        order_dtos = list()
        for order in orders:
            order_dtos.append(OrderDTO.model_validate(order))
        
        return order_dtos
