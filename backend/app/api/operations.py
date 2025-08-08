from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.schemas.operation import OperationCreate, OperationRead
from backend.app.models.operation import Operation
from backend.app.core.database import get_async_session

router = APIRouter()

@router.post("/operations", response_model=OperationRead)
async def create_operation(operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    new_operation = Operation(**operation.dict())
    session.add(new_operation)
    await session.commit()
    await session.refresh(new_operation)
    return new_operation

@router.get("/assemblies/{assembly_id}/operations", response_model=list[OperationRead])
async def get_operations_by_assembly(assembly_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Operation).where(Operation.assembly_id == assembly_id))
    return result.scalars().all()

@router.delete("/operations/{id}", status_code=204)
async def delete_operation(id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Operation).where(Operation.id == id))
    operation = result.scalar_one_or_none()
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    await session.delete(operation)
    await session.commit()
