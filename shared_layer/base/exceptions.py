class ApplicationError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidInputError(ApplicationError):
    def __init__(self, message: str = "Invalid input format, check your JSON payload"):
        super().__init__(message, 400)


class DatabaseError(ApplicationError):
    def __init__(self, message: str = "Failed to create dragon", details: str = ""):
        self.details = details
        error_message = f"{message}: {details}" if details else message
        super().__init__(error_message, 500)


class NotFoundError(ApplicationError):
    def __init__(self, item: str):
        super().__init__(f"{item} not found", 404)


class ForbiddenError(ApplicationError):
    def __init__(self, message: str = "You are not authorized to perform this action."):
        super().__init__(message, 403)


class UnauthorizedError(ApplicationError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)
