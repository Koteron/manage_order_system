"""
JWT (JSON Web Token) Security Utilities.

This module provides functions for generating and validating 
signed tokens to manage user sessions across the microservices.
"""
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.config.settings import settings
from app.exception.http_exceptions import UnauthorizedException


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    """
    Generates a signed JWT access token for a specific user.

    The token includes a 'user_id' claim and an 'exp' (expiration) timestamp.
    Uses the system's secret key and the HS256 algorithm (by default).

    Args:
        user_id: The unique database identifier for the user.
        expires_delta: Optional override for token duration. 
                       Defaults to settings.JWT_EXPIRE_MINUTES.

    Returns:
        A URL-safe, base64-encoded string representing the signed token.
    """
    to_encode = {"user_id": user_id}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str):
    """
    Decodes and validates a JWT string.

    Performs signature verification and checks the 'exp' claim to ensure 
    the token is still active.

    Args:
        token: The raw bearer token string from the Authorization header.

    Returns:
        dict: The decoded payload containing 'user_id'.

    Raises:
        UnauthorizedException: If the token is expired, has an invalid 
                               signature, or is malformed.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise UnauthorizedException("The token has expired") from e
    except jwt.InvalidTokenError as e:
        raise UnauthorizedException("Invalid token") from e
        