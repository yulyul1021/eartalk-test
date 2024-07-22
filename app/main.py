from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.config import settings

app = FastAPI()
app.include_router(api_router)
app.mount("/" + settings.AUDIO_DIR,
                 StaticFiles(directory=settings.AUDIO_DIR_NAME),
                 name=settings.AUDIO_DIR_NAME)
app.mount("/static", StaticFiles(directory="static"), name="static")