from dataclasses import dataclass


@dataclass
class UserCreateSchema:
    name: str
    email: str
    password: str


@dataclass
class UserUpdateSchema:
    name: str
    email: str
