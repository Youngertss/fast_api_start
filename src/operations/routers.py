from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.database import get_async_session
from src.operations.models import Operation
from src.operations.schemas import OperationCreate, OperationRead

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get('/')
async def get_specific_operations(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Operation).where(Operation.id == operation_id)
    result = await session.execute(query)
    # return result.scalars().first()
    return {
            "status": "success",
            "data": result.scalars().all(),
            "details": None
        }


@router.post('/')
async def add_specific_operations(operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(Operation).values(**operation.dict())
    await session.execute(statement)
    await session.commit()
    return {"status":"success"}
