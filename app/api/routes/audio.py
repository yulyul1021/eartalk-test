import uuid
from datetime import datetime
from typing import Any, Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Form
from starlette.templating import Jinja2Templates

from app.api.dependencies import SessionDep
from app.core.config import settings
from app.models import AudioPublic, Audio

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def read_audio(*, request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/")
async def create_audio(
    request: Request,
    session: SessionDep,
    input_text: Annotated[str | None, Form()] = None,
    audio: Annotated[UploadFile | None, File()] = None
) -> Any:
    """
    Create new audio.
    """
    if not input_text and not audio:
        raise HTTPException(status_code=400, detail="텍스트 혹은 음성 둘 중 하나를 입력해주세요.")
    if input_text and audio:
        raise HTTPException(status_code=400, detail="텍스트 혹은 음성 둘 중 하나만 입력해주세요.")

    original_filepath = None
    if audio:
        # 원본 wav 저장
        original_filepath = f"{settings.ORIGINAL_AUDIO_DIR}{str(uuid.uuid4())}.wav"
        original_full_filepath = f"{settings.AUDIO_DIR}{original_filepath}"
        data = await audio.read()
        with open(original_full_filepath, "wb") as f:
            f.write(data)

    # TODO 가공 wav 저장
    processed_filepath = f"{settings.PROCESSED_AUDIO_DIR}{str(uuid.uuid4())}.wav"
    processed_full_filepath = f"{settings.AUDIO_DIR}{processed_filepath}"

    audio = Audio(
        text=           "임시 text입니다.",  # TODO 수정 모델 거쳐 나온 text 혹은 사용자가 입력한 text
        original=       original_filepath,
        processed=      processed_filepath,
        create_date=    datetime.now()
    )
    session.add(audio)
    session.commit()
    session.refresh(audio)
    return templates.TemplateResponse("index.html", {"request": request, "data": audio})