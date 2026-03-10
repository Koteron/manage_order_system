from app.exception.http_exceptions import NotFoundException, ForbiddenException, UnauthorizedException, BadRequestException


class UserNotFoundException(NotFoundException):
    def __init__(self, user_id: int = None, email: str = None):
        if user_id is not None:
            self.user_id = user_id
            super().__init__(f"User with id=({user_id}) not found")    
        elif email is not None:
            self.email = email
            super().__init__(f"User with email=({email}) not found")

class InvalidCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__(f"Invalid login credentials")

class UserAlreadyExistsExecption(ForbiddenException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email=({email}) already exists")

class UserCreationExecption(BadRequestException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Cound not create a new user with email=({email})")