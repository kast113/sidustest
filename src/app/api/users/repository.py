from datetime import datetime
from typing import Optional
from app.api.users.entity import UserEntity
from app.db import users, database
from app.api.users.input import UserCreateSchema, UserUpdateSchema
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

async def get_user_by_id(user_id: int) -> Optional[UserEntity]:
    """
    Fetch user by id
    """
    query = users.select().where(users.columns.id == user_id)
    result = await database.fetch_one(query=query)
    if not result:
        return None
    return UserEntity(**dict(result))

async def get_user_by_name(username: str) -> Optional[UserEntity]:
    """
    Fetch user by username
    """
    query = users.select().where(users.columns.name == username)
    result = await database.fetch_one(query=query)
    if not result:
        return None
    return UserEntity(**dict(result))

async def create_user(payload: UserCreateSchema) -> int:
    """
    Create user
    """
    print("repository create u")
    query = users.insert().values(
        name=payload.name, 
        email=payload.email,
        password=get_password_hash(payload.password),
    )
    return await database.execute(query=query)

async def update_user(user_id: int, payload: UserUpdateSchema):
    """
    Update user
    """
    query = (
        users
            .update()
            .where(users.columns.id == user_id)
            .values(
                name=payload.name,
                email=payload.email,
                updated_at=datetime.now()
            )
    )
    return await database.execute(query=query)
