import uuid

from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import UUID


class Base(orm.DeclarativeBase):
    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.replace("Model", "").lower()
