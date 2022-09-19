from fastapi import HTTPException
from fastapi import Depends
from app.api.users.repository import get_user_by_id, create_user, update_user
from app.api.users.input import UserCreateSchema, UserUpdateSchema
from app.api.users.dependencies import get_current_user
from app.utils.cache import redis_cache, acached

REDIS_KEY='user_redis'

@acached(REDIS_KEY)
async def get_user_view(
    user_id: int,
):
    """Get user view"""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def create_user_view(payload: UserCreateSchema):
    """Create user"""
    print("view create u")
    user_id = await create_user(payload)
    return {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
    }


async def update_user_view(
    user_id: int,
    payload: UserUpdateSchema,
    user: str = Depends(get_current_user),
):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await update_user(user_id, payload)
    await redis_cache.delete(f'{REDIS_KEY}:{user_id}')
    return {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
    }