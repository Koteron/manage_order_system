"""
User-Specific Domain Exceptions.

Specialized exceptions for user management that map to specific 
HTTP responses via their parent classes.
"""
from app.exception.http_exceptions import (
    NotFoundException, 
    ForbiddenException, 
    UnauthorizedException, 
    BadRequestException
)


class UserNotFoundException(NotFoundException):
    """
    Raised when a user lookup fails by ID or Email.
    Maps to **HTTP 404 Not Found**.
    """
    def __init__(self, user_id: int = None, email: str = None):
        if user_id is not None:
            self.user_id = user_id
            super().__init__(f"User with id=({user_id}) not found")    
        elif email is not None:
            self.email = email
            super().__init__(f"User with email=({email}) not found")

class InvalidCredentialsException(UnauthorizedException):
    """
    Raised during failed login attempts (wrong password).
    Maps to **HTTP 401 Unauthorized**.
    """
    def __init__(self):
        super().__init__(f"Invalid login credentials")

class UserAlreadyExistsExecption(ForbiddenException):
    """
    Raised when registering an email that is already in the database.
    Maps to **HTTP 403 Forbidden**.
    """
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email=({email}) already exists")

class UserCreationException(BadRequestException):
    """
    Raised when user persistence fails for non-constraint reasons.
    Maps to **HTTP 400 Bad Request**.
    """
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Cound not create a new user with email=({email})")