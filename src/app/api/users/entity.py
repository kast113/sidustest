from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from app.api.users.models import Users


@dataclass
class UserEntity:
    id: int
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

    def from_raw(user: Users) -> UserEntity:
        return UserEntity(
            user.id,
            user.name,
            user.email,
            user.password,
            user.created_at,
            user.updated_at
        )