from functools import wraps
import pickle
import os

import aioredis


class RedisCache:
    def __init__(self, redis_dsn: str):
        self.redis_cache = aioredis.from_url(redis_dsn)

    async def delete(self, key):
        return await self.redis_cache.delete(key)

    async def set(self, key, value):
        return await self.redis_cache.set(key, value)

    async def get(self, key):
        return await self.redis_cache.get(key)

    async def close(self):
        await self.redis_cache.close()


class RedisCacheForView():

    global_key: str = None
    redis_cache: RedisCache = RedisCache(os.getenv("REDIS_DSN"))

    def __init__(self) -> None:
        print('CACHE INIT')
        if not self.global_key:
            raise Exception("global_key not setted")

    def get_key(self, *args, **kwargs) -> str:
        raise NotImplementedError()

    def cache_one_decorator(self):
        def wrapper(func):
            @wraps(func)
            async def wrapped(*args, **kwargs):
                # TODO dirty hack
                if os.environ.get("IS_TESTING"):
                    return await func(*args, **kwargs)
                key = self.get_key(*args, **kwargs)
                print('key', key)
                data = None
                data = await self.redis_cache.get(key)
                if data:
                    return pickle.loads(data)
                data = await func(*args, **kwargs)
                await self.redis_cache.set(key, pickle.dumps(data))
                return data
            return wrapped
        return wrapper

    def clear_one_decorator(self):
        def wrapper(func):
            @wraps(func)
            async def wrapped(*args, **kwargs):
                # TODO dirty hack
                if os.environ.get("IS_TESTING"):
                    return await func(*args, **kwargs)
                key = self.get_key(*args, **kwargs)
                data = await func(*args, **kwargs)
                await self.redis_cache.delete(key)
                return data
            return wrapped
        return wrapper

