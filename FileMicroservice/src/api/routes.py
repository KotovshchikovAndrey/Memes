from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from services import storage

router = APIRouter(prefix="/memes")


@router.get("/{image_name:str}")
async def get_image(image_name: str):
    url = await storage.get_image_url(image_name)
    return RedirectResponse(url=url)
