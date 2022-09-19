from fastapi import FastAPI

from app.api.users.router import router as users_router
from app.api.health_check.router import router as health_check_router
from app.db import database, engine, metadata
from app.utils.cache import redis_cache

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    # postgre
    await database.connect()
    # redis
    redis_cache.init_cache()


@app.on_event("shutdown")
async def shutdown():
    # postgre
    await database.disconnect()
    # redis
    await redis_cache.close()


app.include_router(health_check_router)
app.include_router(users_router)

