"""
User Authentication and Identity Routes.

This module provides the public endpoints for user lifecycle management, 
including account registration and OAuth2-compatible token exchange.
Exempt from standard rate limits to ensure accessibility during login.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.user_dtos import TokenDTO
from app.services.user_service import UserService, get_user_service
from app.schemas.user_dtos import UserAuthDTO
from app.schemas.error_response import ErrorResponse
from app.util.limiter import limiter


user_router = APIRouter(tags=["users"])

@user_router.post("/register/", responses={
    400: {"model": ErrorResponse, "description": "Could not create user"},
    403: {"model": ErrorResponse, "description": "Email taken"},
})
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_auth_dto: UserAuthDTO,
    service: Annotated[UserService, Depends(get_user_service)],
) -> TokenDTO:
    """
    Create a new user account.

    Validates that the email is unique and hashes the password 
    before storage. Returns a JWT access token upon successful registration.
    """
    return await service.register(user_auth_dto)

@user_router.post("/token/", responses={
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    404: {"model": ErrorResponse, "description": "Not found"},
})
@limiter.limit("5/minute")
async def token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
) -> TokenDTO:
    """
    OAuth2 compatible token login.

    Exchanges a username (email) and password for a JWT access token. 
    This token should be included in the 'Authorization: Bearer <token>' 
    header for protected routes.
    """
    return await service.login(
        user_auth_dto=UserAuthDTO(
            email=form_data.username,
            password=form_data.password,
        ),
    )