from dataclasses import dataclass


@dataclass
class UserOutSchema:
    id: int
    name: str
    email: str
