from fastapi import APIRouter

from app.api.routes import audio
from app.core.database import engine

api_router = APIRouter()
api_router.include_router(audio.router, tags=["audio"])

from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)