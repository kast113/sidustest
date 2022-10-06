from fastapi import HTTPException
from fastapi import Depends
from app.api.users.entity import UserEntity

from app.api.users.input import UserCreateSchema, UserUpdateSchema
from app.api.users.dependencies import get_current_user
from app.api.users.service import UserCreate, UserGetOne, UserUpdate
# from app.utils.cache import redis_cache, acached


REDIS_KEY = 'user_redis'


# @acached(REDIS_KEY)
async def get_user_view(
    user_id: int,
    service_user_one: UserGetOne = Depends(UserGetOne),
) -> UserEntity:
    """Get user view"""
    return await service_user_one.execute(user_id)


async def create_user_view(
    payload: UserCreateSchema,
    service_user_create: UserCreate = Depends(UserCreate)
) -> UserEntity:
    """Create user"""
    return await service_user_create.execute(payload)


async def update_user_view(
    user_id: int,
    payload: UserUpdateSchema,
    user: str = Depends(get_current_user),
    service_user_update: UserUpdate = Depends(UserUpdate)
) -> UserEntity:
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    # await redis_cache.delete(f'{REDIS_KEY}:{user_id}')
    return await service_user_update.execute(user_id, payload)
