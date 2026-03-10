import bcrypt

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Annotated

from app.config.db import get_async_session
from app.models.user import User
from app.schemas.user_dtos import UserAuthDTO, TokenDTO
from app.exception.user_exception import (
    UserCreationExecption, 
    UserNotFoundException, 
    InvalidCredentialsException, 
    UserAlreadyExistsExecption
)
from app.config.settings import settings
from app.util.jwt_util import create_access_token


def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(session)

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, user_auth_dto: UserAuthDTO) -> TokenDTO:
        password_bytes = user_auth_dto.password.encode('utf-8')
        try:
            query_result = await self.session.execute(
                insert(User)
                .values(
                    password=bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)),
                    email=user_auth_dto.email)
                .returning(User.id)
            )
            user_id = query_result.scalar_one()
            
        except IntegrityError as e:
            raise UserAlreadyExistsExecption(email=user_auth_dto.email) from e 
        except NoResultFound as e:
            raise UserCreationExecption(email=user_auth_dto.email) from e
            
        token = create_access_token(user_id=user_id)

        await self.session.commit()
        
        return TokenDTO(access_token=token)
    
    async def login(self, user_auth_dto: UserAuthDTO) -> TokenDTO:
        query_results = await self.session.execute(
            select(User).where(User.email == user_auth_dto.email)
        )
        user = query_results.scalar_one_or_none()

        if user is None:
            raise UserNotFoundException(email=user_auth_dto.email)
        
        if not bcrypt.checkpw(user_auth_dto.password.encode('utf-8'), user.password):
            raise InvalidCredentialsException()
        
        token = create_access_token(user_id=user.id)

        return TokenDTO(access_token=token)
