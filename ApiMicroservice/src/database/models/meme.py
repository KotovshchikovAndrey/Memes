from datetime import datetime

from sqlalchemy import DateTime, String, Text, orm, sql

from database.models.base import Base


class MemeModel(Base):
    title: orm.Mapped[str] = orm.mapped_column(String(70), nullable=False)

    text: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)

    image_url: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=False),
        server_default=sql.text("TIMEZONE('UTC', NOW())"),
    )
