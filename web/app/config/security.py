"""
Authentication and Authorization Security Layer.

Provides FastAPI dependencies for resolving user identity from 
JWT Bearer tokens. Ensures that protected routes only execute 
for verified, active users.
"""
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_async_session
from app.util.jwt_util import decode_access_token
from app.exception.http_exceptions import UnauthorizedException
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> User:
    """
    Dependency for extracting and validating the authenticated user.

    Used by injecting it into route functions: 
    `current_user: Annotated[User, Depends(get_current_user)]`.

    Process:
    1. Extracts the JWT from the 'Authorization' header.
    2. Decodes the token to verify the signature and expiration.
    3. Queries the database to ensure the user still exists.

    Args:
        token: The raw JWT string provided by the client.
        session: Scoped database session for identity lookup.

    Returns:
        User: The authenticated SQLAlchemy model instance.

    Raises:
        UnauthorizedException: If the token is invalid, expired, or 
                               the associated user no longer exists.
    """
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Could not validate credentials")
    
    user_id = payload.get("user_id")
    user = await session.get(User, user_id)

    if not user:
        raise UnauthorizedException("Invalid authentication credentials")

    return user