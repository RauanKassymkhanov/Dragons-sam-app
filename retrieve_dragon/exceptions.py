class ApplicationError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(ApplicationError):
    def __init__(self, item: str):
        super().__init__(f"{item} not found", 404)
