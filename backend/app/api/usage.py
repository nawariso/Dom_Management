from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import UsageRecord
from ..security.rbac import require_roles

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("/", response_model=List[UsageRecord])
async def list_usage(
    session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "tenant", "auditor"]))
) -> list[UsageRecord]:
    return [
        UsageRecord(
            id=1,
            meter_id=1,
            consumed_kwh=42.5,
            recorded_at=datetime.utcnow(),
        )
    ]


@router.post("/", response_model=UsageRecord)
async def record_usage(
    record: UsageRecord,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles(["admin", "tenant"])),
) -> UsageRecord:
    return record
