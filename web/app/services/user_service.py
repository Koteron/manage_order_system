"""
User Identity Business Logic.

Manages sensitive data operations including secure password hashing 
(Bcrypt) and JWT issuance. Acts as the gatekeeper for user 
authentication before any order-related operations can occur.
"""
import bcrypt
import logging

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import Annotated

from app.config.db import get_async_session
from app.models.user import User
from app.schemas.user_dtos import UserAuthDTO, TokenDTO
from app.exception.user_exception import (
    UserCreationException , 
    UserNotFoundException, 
    InvalidCredentialsException, 
    UserAlreadyExistsExecption
)
from app.config.settings import settings
from app.util.jwt_util import create_access_token
from app.util.limiter import limiter


logger = logging.getLogger("app")

def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(session)

class UserService:
    """
    Service layer for User Authentication and Management.
    
    Handles secure password hashing using bcrypt and manages the generation 
    of JWT (JSON Web Tokens) for session management.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    @limiter.exempt
    async def register(self, user_auth_dto: UserAuthDTO) -> TokenDTO:
        """
        Registers a new user and returns an initial access token.

        Salts and hashes the password using bcrypt with a configurable 
        work factor (rounds). Performs a unique constraint check on 
        the email address.

        Args:
            user_auth_dto: Object containing the raw password and unique email.

        Returns:
            TokenDTO: A bearer token containing the new user's identity.

        Raises:
            UserAlreadyExistsExecption: If the email is already registered.
            UserCreationExecption: If a database error occurs during insertion.
        """
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
            raise UserCreationException (email=user_auth_dto.email) from e
            
        await self.session.commit()
        logger.info("Created user with id: %s", user_auth_dto.email)

        token = create_access_token(user_id=user_id)
        
        return TokenDTO(access_token=token)
    
    @limiter.exempt
    async def login(self, user_auth_dto: UserAuthDTO) -> TokenDTO:
        """
        Authenticates a user and generates a JWT access token.

        Performs a constant-time password comparison to prevent timing 
        attacks. If successful, issues a signed token for subsequent 
        authenticated requests.

        Args:
            user_auth_dto: The user's login credentials.

        Returns:
            TokenDTO: The signed JWT access token.

        Raises:
            UserNotFoundException: If the email does not exist in the system.
            InvalidCredentialsException: If the password hash does not match.
        """
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
