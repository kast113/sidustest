from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import sessionmaker

from app.api.users.entity import UserEntity
from app.api.users.models import Users
from app.api.users.utils import verify_password
from app.db import db_session


security = HTTPBasic()


async def get_current_user(
    db_session: sessionmaker = Depends(db_session),
    credentials: HTTPBasicCredentials = Depends(security)
) -> UserEntity:
    async with db_session() as session:
        user = await Users.get_by_email(session, credentials.username)
        if not user or not verify_password(credentials.password,
                                           user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return user
