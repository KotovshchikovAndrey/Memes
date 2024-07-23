from fastapi import Request, status
from fastapi.responses import JSONResponse

from exceptions.base import ApiException


def handle_internal_exception(request: Request, exc: Exception) -> None:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
        },
    )


def handle_api_exception(request: Request, exc: ApiException) -> None:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": exc.message,
        },
    )
