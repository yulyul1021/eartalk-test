from datetime import datetime

from fastapi import UploadFile
from sqlmodel import Field, SQLModel


class AudioBase(SQLModel):
    text:       str
    original:   str | None = Field(default=None) # filepath
    processed:  str # filepath


class AudioCreate(SQLModel):
    text:   str | None = Field(default=None)
    audio:  UploadFile | None = Field(default=None)


class Audio(AudioBase, table=True):
    id:             int | None = Field(default=None, primary_key=True)
    create_date:    datetime


class AudioPublic(AudioBase):
    id:         int
    owner_id:   int


class Message(SQLModel):
    message: str
