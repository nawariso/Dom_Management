from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import Tenant
from ..security.rbac import require_roles

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("/", response_model=List[Tenant])
async def list_tenants(
    session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "auditor"]))
) -> list[Tenant]:
    return [Tenant(id=1, name="Example Tenant", timezone="UTC")]


@router.post("/", response_model=Tenant)
async def create_tenant(
    tenant: Tenant, session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin"]))
) -> Tenant:
    return tenant
