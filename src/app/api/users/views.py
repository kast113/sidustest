from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.api.users.repository import get_user_by_id, create_user, update_user
from app.api.users.input import UserCreateSchema, UserUpdateSchema
from app.api.users.dependencies import get_current_user
from app.utils.cache import redis_cache, acached

from app.db import db_session

REDIS_KEY = 'user_redis'

# @acached(REDIS_KEY)


async def get_user_view(
    user_id: int,
    session: AsyncSession = Depends(db_session)
):
    """Get user view"""
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_user_view(
    payload: UserCreateSchema,
    session: AsyncSession = Depends(db_session)
):
    """Create user"""
    try:
        user = await create_user(session, payload)
        await session.commit()
        return {
            "id": user.id,
            "name": payload.name,
            "email": payload.email,
        }
    except SQLAlchemyError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Swrong")


async def update_user_view(
    user_id: int,
    payload: UserUpdateSchema,
    user: str = Depends(get_current_user),
    session: AsyncSession = Depends(db_session)
):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        await update_user(session, user_id, payload)
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Swrong")
    # await redis_cache.delete(f'{REDIS_KEY}:{user_id}')
    return {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
    }
