# backend/app/services/operation_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from backend.app.models.operation import Operation
from backend.app.models.component import Component
from backend.app.models.audit_log import AuditLog
from backend.app.schemas.operation import OperationCreate
from backend.app.core.database import async_session
from backend.app.utils.notifications import notify_technologist

async def apply_operation(operation: OperationCreate):
    async with async_session() as session:
        async with session.begin():
            stmt = select(Component).where(Component.id.in_(operation.component_ids))
            result = await session.execute(stmt)
            components = result.scalars().all()

            if len(components) != len(operation.component_ids):
                raise ValueError("One or more components not found")

            if any(c.state != "available" for c in components):
                raise ValueError("One or more components are not available")

            op = Operation(
                assembly_id=operation.assembly_id,
                performed_by=operation.performed_by,
                timestamp=operation.timestamp,
                notes=operation.notes,
                deviation=operation.deviation
            )
            session.add(op)
            await session.flush()

            update_stmt = (
                update(Component)
                .where(Component.id.in_(operation.component_ids))
                .values(state="used", operation_id=op.id)
            )
            await session.execute(update_stmt)

            audit = AuditLog(
                action="apply_operation",
                performed_by=operation.performed_by,
                details=f"Operation {op.id} applied to components {operation.component_ids}"
            )
            session.add(audit)

        if operation.deviation:
            await notify_technologist(op.id)
