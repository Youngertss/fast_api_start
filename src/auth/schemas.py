from typing import Optional, List
from datetime import datetime

from fastapi_users import schemas, models
from pydantic import EmailStr
from pydantic import BaseModel

class UserRead(schemas.BaseUser[int]):
    id: models.ID
    username: str
    email: EmailStr
    role_id: int
    # registered_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    # registered_at: Optional[datetime] = datetime.utcnow
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class RoleBase(BaseModel):
    name: str
    permissions: List[str]

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

# class UserUpdate(schemas.BaseUserUpdate):
#     pass