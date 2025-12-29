class BaseError(Exception):
    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(BaseError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND")


class ValidationError(BaseError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "VALIDATION_ERROR")


class AuthenticationError(BaseError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, "AUTHENTICATION_ERROR")


class AuthorizationError(BaseError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, "AUTHORIZATION_ERROR")


class ConflictError(BaseError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "CONFLICT")
