import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.routes import router
from config.settings import settings
from services import consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consumer.download_images())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


def run_uvicorn_server():
    uvicorn.run(
        "index:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_debug,
    )
