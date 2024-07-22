from typing import Annotated

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import Session as SQLModelSession


from app.core.database import engine


SessionLocal = sessionmaker(class_=SQLModelSession, autoflush=False, bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session


QueryDep = Annotated[str, Query()]
SessionDep = Annotated[Session, Depends(get_session)]

