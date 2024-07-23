import typing as tp

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: tp.Annotated[int | None, Field(gt=0, default=None)]
    offset: tp.Annotated[int, Field(default=0)]
