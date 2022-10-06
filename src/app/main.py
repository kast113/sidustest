from fastapi import FastAPI

from app.api.users.router import router as users_router
from app.api.health_check.router import router as health_check_router
# from app.utils.cache import redis_cache

app = FastAPI()


@app.on_event("startup")
async def startup():
    # redis
    # redis_cache.init_cache()
    pass


@app.on_event("shutdown")
async def shutdown():
    # redis
    # await redis_cache.close()
    pass


app.include_router(health_check_router)
app.include_router(users_router)
