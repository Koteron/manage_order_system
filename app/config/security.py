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
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Could not validate credentials")
    
    user_id = payload.get("user_id")
    user = await session.get(User, user_id)

    if not user:
        raise UnauthorizedException("Invalid authentication credentials")

    return user