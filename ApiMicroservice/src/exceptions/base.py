class ApiException(Exception):
    status: int
    message: str

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        self.message = message
