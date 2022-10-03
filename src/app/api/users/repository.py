from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


from app.api.users.entity import UserEntity
from app.api.users.models import Users
from app.api.users.input import UserCreateSchema, UserUpdateSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def get_user_by_id(
    session: AsyncSession,
    user_id: int
) -> Optional[UserEntity]:
    """
    Fetch user by id
    """
    query = await session.execute(select(Users).where(Users.id == user_id))
    result = query.scalars().first()
    if not result:
        return None
    return UserEntity.from_raw(result)


async def get_user_by_email(
    session: AsyncSession,
    email: str
) -> Optional[UserEntity]:
    """
    Fetch user by username
    """
    query = await session.execute(select(Users).where(Users.email == email))
    result = query.scalars().first()
    if not result:
        return None
    return UserEntity.from_raw(result)


async def create_user(
    session: AsyncSession,
    payload: UserCreateSchema,
) -> Users:
    """
    Create user
    """
    # TODO check email before insert
    user = Users(
        name=payload.name,
        email=payload.email,
        password=get_password_hash(payload.password),
    )
    session.add(user)
    return user


async def update_user(
    session: AsyncSession,
    user_id: int,
    payload: UserUpdateSchema
) -> Users:
    """
    Update user
    """
    # check email before update
    query = await session.execute(select(Users).where(Users.id == user_id))
    user = query.scalars().first()
    user.name = payload.name
    user.email=payload.email
    user.updated_at=datetime.now()

    session.add(user)
    return user
