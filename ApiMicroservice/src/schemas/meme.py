import typing as tp
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseMeme(BaseModel):
    title: tp.Annotated[str, Field(max_length=70, min_length=1, default="Untitled")]
    text: tp.Annotated[str | None, Field(max_length=150, default=None)]


class MemeOutput(BaseMeme):
    id: UUID
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class MemeCreate(BaseMeme): ...


class MemeUpdate(BaseMeme): ...


class MemePartialUpdate(BaseModel):
    title: tp.Annotated[str | None, Field(max_length=70, min_length=1, default=None)]
    text: tp.Annotated[str | None, Field(max_length=150, default=None)]


class ApiResponse(BaseModel):
    message: str
    data: tp.Annotated[tp.Any, Field(default=None)]
