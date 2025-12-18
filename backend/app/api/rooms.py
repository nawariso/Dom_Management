from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import Room
from ..security.rbac import require_roles

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/", response_model=List[Room])
async def list_rooms(
    session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "tenant", "auditor"]))
) -> list[Room]:
    return [Room(id=1, name="101A", tenant_id=1)]


@router.post("/", response_model=Room)
async def create_room(
    room: Room, session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin"]))
) -> Room:
    return room
