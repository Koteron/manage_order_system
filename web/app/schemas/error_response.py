"""
Global Error Response Schema.

Standardizes the structure of 4xx and 5xx HTTP responses to ensure 
consistency for frontend clients and API consumers.
"""
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str