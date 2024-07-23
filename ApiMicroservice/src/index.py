from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.routes import router
from config.settings import settings
from database.connection import database
from exceptions.base import ApiException
from exceptions.handlers import handle_api_exception, handle_internal_exception


def run_uvicorn_server():
    uvicorn.run(
        "index:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_debug,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.create_tables()
    yield
    await database.close()


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(ApiException, handle_api_exception)
app.add_exception_handler(Exception, handle_internal_exception)
app.include_router(prefix="/api/v1", router=router)
