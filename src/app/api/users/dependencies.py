from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.api.users.entity import UserEntity

from app.api.users.repository import get_user_by_name, verify_password


security = HTTPBasic()

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserEntity:
    user = await get_user_by_name(credentials.username)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
