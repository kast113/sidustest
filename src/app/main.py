from fastapi import FastAPI

from app.api.users.router import router as users_router
from app.api.health_check.router import router as health_check_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(health_check_router)
app.include_router(users_router)
