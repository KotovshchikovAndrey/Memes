from exceptions.base import ApiException


class MemeNotFoundException(ApiException):
    _message = "Meme not found"

    def __init__(self) -> None:
        super().__init__(status=404, message=self._message)
