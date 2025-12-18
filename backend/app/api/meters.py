from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import Meter
from ..security.rbac import require_roles

router = APIRouter(prefix="/meters", tags=["meters"])


@router.get("/", response_model=List[Meter])
async def list_meters(
    session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "tenant", "auditor"]))
) -> list[Meter]:
    return [Meter(id=1, serial_number="MTR-001", room_id=1)]


@router.post("/", response_model=Meter)
async def register_meter(
    meter: Meter, session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin"]))
) -> Meter:
    return meter
