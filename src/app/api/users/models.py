from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.utils import get_password_hash

from app.db import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), index=True, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        user_id: int
    ) -> Optional[Users]:
        stmt = select(cls).where(cls.id == user_id)
        result = (await session.execute(stmt)).first()
        if not result:
            return None
        print('GET BY ID')
        print(result)
        return result.Users

    @classmethod
    async def get_by_email(
        cls,
        session: AsyncSession,
        email: str
    ) -> Optional[Users]:
        stmt = select(cls).where(cls.email == email.lower())
        result = (await session.execute(stmt)).first()
        if not result:
            return None
        return result.Users

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        email: str,
        password: str
    ) -> Users:
        user = Users(
            name=name,
            email=email.lower(),
            password=get_password_hash(password)
        )
        session.add(user)
        await session.flush()

        new_user = await cls.get_by_id(session, user.id)
        if not new_user:
            raise RuntimeError()
        return new_user

    async def update(
        self,
        session: AsyncSession,
        name: str,
        email: str
    ) -> None:
        self.name = name
        self.email = email
        self.updated_at = datetime.now()
        await session.flush()
