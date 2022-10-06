from functools import wraps
import os

import pickle
import aioredis


REDIS_DSN = os.getenv("REDIS_DSN")


class RedisCache:
    def __init__(self):
        self.redis_cache = None

    def init_cache(self):
        self.redis_cache = aioredis.from_url(REDIS_DSN)

    # async def keys(self, pattern):
    #     return await self.redis_cache.keys(pattern)

    async def delete(self, key):
        return await self.redis_cache.delete(key)

    async def set(self, key, value):
        return await self.redis_cache.set(key, value)

    async def get(self, key):
        return await self.redis_cache.get(key)

    async def close(self):
        await self.redis_cache.close()


redis_cache = RedisCache()


def acached(rkey):
    """Redis cache decorator"""
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            # TODO dirty hack
            if os.environ.get("IS_TESTING"):
                return await func(*args, **kwargs)
            key = f'{rkey}:{kwargs["user_id"]}'
            data = None
            data = await redis_cache.get(key)
            if data:
                return pickle.loads(data)
            data = await func(*args, **kwargs)
            await redis_cache.set(key, pickle.dumps(data))
            return data
        return wrapped
    return wrapper
