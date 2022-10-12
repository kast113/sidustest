from typing import AsyncIterator

from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException

from app.api.users.entity import UserEntity
from app.api.users.input import UserCreateSchema, UserUpdateSchema
from app.api.users.models import Users
from app.db import db_session


class ServiceBase():

    def __init__(self, session: sessionmaker = Depends(db_session)) -> None:
        self.db_session = session


class UserGetAll(ServiceBase):

    async def execute(self) -> AsyncIterator[UserEntity]:
        async with self.db_session() as session:
            async for user in Users.get_all(session):
                yield UserEntity.from_raw(user)


class UserGetOne(ServiceBase):

    async def execute(self, user_id: int) -> UserEntity:
        async with self.db_session() as session:
            user = await Users.get_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404)
            return UserEntity.from_raw(user)


class UserCreate(ServiceBase):

    async def execute(self, payload: UserCreateSchema) -> UserEntity:
        async with self.db_session.begin() as session:
            user = await Users.get_by_email(session, payload.email)
            if user:
                raise HTTPException(
                    status_code=400, detail='email is already registered')
            user = await Users.create(
                session,
                payload.name,
                payload.email,
                payload.password)
            return UserEntity.from_raw(user)


class UserUpdate(ServiceBase):

    async def execute(
        self,
        user_id: int,
        payload: UserUpdateSchema
    ) -> UserEntity:
        async with self.db_session.begin() as session:
            user = await Users.get_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404, detail='User not found')

            if user.email != payload.email:
                # TODO is_exists
                user = await Users.get_by_email(session, payload.email)
                if user:
                    raise HTTPException(
                        status_code=404,
                        detail='User with new email already registered')

            await user.update(session, payload.name, payload.email)
            await session.refresh(user)
            return UserEntity.from_raw(user)


class UserDelete(ServiceBase):

    async def execute(self, user_id: int) -> None:
        async with self.db_session.begin() as session:
            user = await Users.get_by_id(session, user_id)
            if not user:
                return
            await Users.delete(session, user)
