"""
User Authentication and Identity DTOs.

Provides Pydantic schemas for account registration, login credentials, 
and the standardized OAuth2 token response format.
"""
from pydantic import BaseModel, EmailStr

class UserAuthDTO(BaseModel):
    email: EmailStr
    password: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"