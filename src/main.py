from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import sleep

from fastapi import Depends, FastAPI#, HTTPException
# from sqlalchemy.orm import Session

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from src import database#, schemas, crud
from src.database import engine#, SessionLocal, engine
from src.auth.auth import auth_backend, fastapi_users, current_user
from src.auth.schemas import UserRead, UserCreate
from src.auth.database import User#, get_user_db
from src.auth.routers_role import router as routers_role
from src.operations.routers import router as router_operation
from src.operations.models import Operation
from src.tasks.router import router as router_tasks


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
# database.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event('startup')
async def startup() -> None:
    await create_tables()
    # Кэширование
    redis = aioredis.from_url("redis://localhost", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/lo")
@cache(expire=60)
def long_operation():
    sleep(4)
    return "long text with long time!!!!"


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)
app.include_router(routers_role)
app.include_router(router_tasks)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, it is unp-ted route"

# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield
# if __name__ == "__main__":
#     run(create_tables())
