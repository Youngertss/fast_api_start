from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session

from src.database import get_async_session
from src.auth import crud, schemas

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: AsyncSession = Depends(get_async_session)):
    return crud.create_role(db=db, role=role)

@router.get("/roles/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: AsyncSession = Depends(get_async_session)):
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

