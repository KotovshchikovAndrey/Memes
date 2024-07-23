import pathlib
import typing as tp

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    db_host: tp.Annotated[str, Field(alias="POSTGRES_HOST")]
    db_port: tp.Annotated[str, Field(alias="POSTGRES_PORT")]
    db_user: tp.Annotated[str, Field(alias="POSTGRES_USER")]
    db_password: tp.Annotated[str, Field(alias="POSTGRES_PASSWORD")]
    db_name: tp.Annotated[str, Field(alias="POSTGRES_DB_NAME")]

    server_host: tp.Annotated[str, Field(alias="SERVER_HOST")]
    server_port: tp.Annotated[int, Field(alias="SERVER_PORT")]
    is_debug: bool = True
    media_path: str = str(pathlib.Path(".").joinpath("media").absolute())

    broker_host: tp.Annotated[str, Field(alias="KAFKA_HOST")]
    broker_port: tp.Annotated[str, Field(alias="KAFKA_PORT")]
    broker_topic: tp.Annotated[str, Field(alias="KAFKA_TOPIC")]

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = AppSettings()
