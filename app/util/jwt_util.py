import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.config.settings import settings
from app.exception.http_exceptions import UnauthorizedException


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    to_encode = {"user_id": user_id}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise UnauthorizedException("The token has expired") from e
    except jwt.InvalidTokenError as e:
        raise UnauthorizedException("Invalid token") from e
        