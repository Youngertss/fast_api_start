from pydantic import BaseModel
from typing import Union
from datetime import datetime

class OperationBase(BaseModel):
    quantity: str
    figi: str
    instriment_type: str
    date: Union[datetime, None] = datetime.utcnow()
    operation_type: str

class OperationCreate(OperationBase):
    pass

class OperationRead(OperationBase):
    id: int
    
    class Config:
        orm_mode = True