from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.entity import UserEntity
from app.api.users.repository import get_user_by_email, verify_password
from app.db import db_session


security = HTTPBasic()

async def get_current_user(
    session: AsyncSession = Depends(db_session),
    credentials: HTTPBasicCredentials = Depends(security)
) -> UserEntity:
    user = await get_user_by_email(session, credentials.username)
    print('DEPENDS')
    print(user)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    print('RETURN')
    return user
