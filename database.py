from __future__ import annotations


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session


DATABASE_URL = "sqlite:///./blog.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    with session_local() as db:
        yield db


SessionDep = Annotated[Session, Depends(get_db)]
