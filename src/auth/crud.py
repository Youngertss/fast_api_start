# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth import database, schemas

async def get_role(db: AsyncSession, role_id: int):
    result = await db.execute(select(database.Role).filter(database.Role.id == role_id))
    return result.scalars().first()


async def create_role(db: AsyncSession, role: schemas.RoleCreate):
    db_role = database.Role(**role.model_dump())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


# def get_user(db: Session, user_id: int):
#     return db.query(database.User).filter(database.User.id==user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(database.User).filter(database.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(database.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UsersCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = database.User(username = user.username, email=user.email, password=fake_hashed_password, role_id = user.role_id)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user