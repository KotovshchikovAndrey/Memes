import typing as tp

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    broker_host: tp.Annotated[str, Field(alias="KAFKA_HOST")]
    broker_port: tp.Annotated[str, Field(alias="KAFKA_PORT")]
    broker_topic: tp.Annotated[str, Field(alias="KAFKA_TOPIC")]

    s3_host: tp.Annotated[str, Field(alias="MINIO_HOST")]
    s3_port: tp.Annotated[str, Field(alias="MINIO_PORT")]
    s3_bucket: tp.Annotated[str, Field(alias="MINIO_BUCKET")]
    s3_access_key: tp.Annotated[str, Field(alias="MINIO_ACCESS_KEY")]
    s3_secret_key: tp.Annotated[str, Field(alias="MINIO_SECRET_KEY")]

    server_host: tp.Annotated[str, Field(alias="SERVER_HOST")]
    server_port: tp.Annotated[int, Field(alias="SERVER_PORT")]
    is_debug: bool = True
    api_service_url: str

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = AppSettings()
