import uuid

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_producer
from broker.base import IBrokerProducer
from database.connection import database
from schemas.base import Pagination
from schemas.meme import ApiResponse, MemeCreate, MemePartialUpdate, MemeUpdate
from services import meme as meme_services

router = APIRouter(prefix="/memes")


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def get_memes(
    limit: int | None = Query(default=None),
    offset: int = Query(default=0),
    session: AsyncSession = Depends(database.get_session),
):
    memes, total = await meme_services.get_memes(
        session=session,
        pagination=Pagination(limit=limit, offset=offset),
    )

    return {
        "message": "Success",
        "data": {
            "memes": memes,
            "total": total,
        },
    }


@router.get(
    path="/{meme_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def get_meme(
    meme_id: uuid.UUID,
    session: AsyncSession = Depends(database.get_session),
):
    meme = await meme_services.get_meme(session=session, meme_id=meme_id)
    return {
        "message": "Success",
        "data": meme,
    }


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse,
)
async def create_meme(
    title: str = Form(...),
    text: str | None = Form(default=None),
    image: UploadFile = File(...),
    session: AsyncSession = Depends(database.get_session),
    producer: IBrokerProducer = Depends(get_producer),
):
    new_meme = await meme_services.create_meme(
        session=session,
        prodcuer=producer,
        meme_create=MemeCreate(title=title, text=text),
        image=image,
    )

    return {
        "message": "Meme created successfully",
        "data": new_meme,
    }


@router.put(
    path="/{meme_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def update_meme(
    meme_id: uuid.UUID,
    meme_update: MemeUpdate,
    session: AsyncSession = Depends(database.get_session),
):
    updated_meme = await meme_services.update_meme(
        session=session,
        meme_id=meme_id,
        meme_update=meme_update,
    )

    return {
        "message": "Success",
        "data": updated_meme,
    }


@router.patch(
    path="/{meme_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def update_meme_partially(
    meme_id: uuid.UUID,
    meme_update: MemePartialUpdate,
    session: AsyncSession = Depends(database.get_session),
):
    updated_meme = await meme_services.update_meme(
        session=session,
        meme_id=meme_id,
        meme_update=meme_update,
        is_partil=True,
    )

    return {
        "message": "Success",
        "data": updated_meme,
    }


@router.delete(
    path="/{meme_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_meme(
    meme_id: uuid.UUID,
    session: AsyncSession = Depends(database.get_session),
):
    await meme_services.delete_meme(session=session, meme_id=meme_id)


@router.get(
    path="/images/{image_name:str}",
    status_code=status.HTTP_200_OK,
)
async def download_image(image_name: str) -> None:
    return StreamingResponse(
        meme_services.download_image(image_name),
        media_type="application/octet-stream",
    )


@router.delete(path="/images/{image_name:str}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(image_name: str) -> None:
    await meme_services.delete_image(image_name)
