from typing import AsyncGenerator
from datetime import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import Boolean, String, Integer, TIMESTAMP, ForeignKey, Boolean, ARRAY, Column, MetaData

from src.config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from src.database import Base, DATABASE_URL, async_session_maker

# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class Role(Base):
    __tablename__="role"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(ARRAY(String))
    
    users = relationship("User", back_populates = 'roles')

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__="user"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[str] = mapped_column(Boolean, default=False)
    # registered_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    
    role_id = mapped_column(Integer, ForeignKey(Role.id))
    roles = relationship("Role", back_populates = 'users')
    
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
        )


# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# comment 'cause we use alembic.ini
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)