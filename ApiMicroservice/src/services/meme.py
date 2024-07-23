import pathlib
import uuid

import aiofiles
import aiofiles.os
from fastapi import UploadFile
from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from broker.base import IBrokerProducer
from config.settings import settings
from database.models.meme import MemeModel
from exceptions.meme import MemeNotFoundException
from schemas.base import Pagination
from schemas.meme import MemeCreate, MemeOutput, MemePartialUpdate, MemeUpdate


async def get_memes(
    session: AsyncSession, pagination: Pagination
) -> tuple[list[MemeOutput], int]:
    stmt = select(MemeModel).offset(pagination.offset)
    if pagination.limit is not None:
        stmt = stmt.limit(pagination.limit)

    memes = await session.scalars(stmt)
    count_stmt = select(func.count(MemeModel.id)).select_from(MemeModel)
    total = await session.scalar(count_stmt)

    return [MemeOutput.model_validate(meme) for meme in memes], total


async def get_meme(session: AsyncSession, meme_id: uuid.UUID) -> MemeOutput:
    stmt = select(MemeModel).where(MemeModel.id == meme_id)
    meme = await session.scalar(stmt)
    if meme is None:
        raise MemeNotFoundException()

    return MemeOutput.model_validate(meme)


async def create_meme(
    session: AsyncSession,
    prodcuer: IBrokerProducer,
    meme_create: MemeCreate,
    image: UploadFile,
) -> MemeOutput:
    image_name = uuid.uuid4().hex + "." + image.filename.split(".")[-1]
    image_path = settings.media_path + f"/{image_name}"
    async with aiofiles.open(image_path, "wb") as io:
        await io.write(await image.read())

    await prodcuer.produce(message=image_name)
    meme = MemeModel(
        title=meme_create.title,
        text=meme_create.text,
        image_url=f"/{image_name}",
    )

    session.add(meme)
    await session.commit()

    return MemeOutput.model_validate(meme)


async def update_meme(
    session: AsyncSession,
    meme_id: uuid.UUID,
    meme_update: MemeUpdate | MemePartialUpdate,
    is_partil: bool = False,
) -> MemeOutput:
    stmt = select(MemeModel).where(MemeModel.id == meme_id)
    meme = await session.scalar(stmt)
    if meme is None:
        raise MemeNotFoundException()

    if not is_partil:
        meme.title = meme_update.title
        meme.text = meme_update.text

    else:
        meme.title = meme_update.title or meme.title
        meme.text = meme_update.text or meme.text

    await session.commit()
    return MemeOutput.model_validate(meme)


async def delete_meme(session: AsyncSession, meme_id: uuid.UUID):
    stmt = delete(MemeModel).where(MemeModel.id == meme_id)
    await session.execute(stmt)
    await session.commit()


async def download_image(image_name: str):
    image_path = f"{settings.media_path}/{image_name}"
    if not pathlib.Path(image_path).exists():
        raise MemeNotFoundException()

    async with aiofiles.open(image_path, "rb") as io:
        while chunk := await io.read(1024):
            yield chunk


async def delete_image(image_name: str) -> None:
    image_path = f"{settings.media_path}/{image_name}"
    if pathlib.Path(image_path).exists():
        await aiofiles.os.remove(image_path)
