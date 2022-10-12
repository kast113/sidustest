from passlib.context import CryptContext

from app.utils.cache import RedisCacheForView


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


class UserCache(RedisCacheForView):
    global_key: str = 'user'

    def get_key(self, *args, **kwargs) -> str:
        user_id = kwargs.get('user_id')
        if not user_id:
            raise Exception('Cache parametr not found: user_id')
        return f'{self.global_key}:{user_id}'


user_cache = UserCache()
