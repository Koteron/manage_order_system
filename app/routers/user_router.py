from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.user_dtos import TokenDTO
from app.services.user_service import UserService, get_user_service
from app.schemas.user_dtos import UserAuthDTO
from app.schemas.error_response import ErrorResponse


user_router = APIRouter(tags=["users"])

@user_router.post("/register/", responses={
    400: {"model": ErrorResponse, "description": "Could not create user"},
    403: {"model": ErrorResponse, "description": "Email taken"},
})
async def register(
    user_auth_dto: UserAuthDTO,
    service: Annotated[UserService, Depends(get_user_service)],
) -> TokenDTO:
    return await service.register(user_auth_dto)

@user_router.post("/token/", responses={
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    404: {"model": ErrorResponse, "description": "Not found"},
})
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
) -> TokenDTO:
    return await service.login(
        user_auth_dto=UserAuthDTO(
            email=form_data.username,
            password=form_data.password,
        ),
    )