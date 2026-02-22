from __future__ import annotations


from sqlalchemy.orm import  DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Annotated
from fastapi import Depends


DATABASE_URL = "sqlite+aiosqlite:///./blog.db"


async_engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
async_session_local = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with async_session_local() as db:
        yield db


SessionDep = Annotated[AsyncSession, Depends(get_session)]
