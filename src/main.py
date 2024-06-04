from fastapi import Depends, FastAPI#, HTTPException
# from sqlalchemy.orm import Session
from fastapi_users import FastAPIUsers

from src import database#, schemas, crud
from src.database import engine#, SessionLocal, engine

from src.auth.manager import get_user_manager
from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.auth.database import User#, get_user_db
from src.auth.routers_role import router as routers_role
from src.operations.routers import router as router_operation
from src.operations.models import Operation

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
# database.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event('startup')
async def init_db() -> None:
    await create_tables()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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


current_active_user = fastapi_users.current_user(active=True)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, it is unp-ted route"

# if __name__ == "__main__":
#     run(create_tables())