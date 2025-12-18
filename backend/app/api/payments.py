from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import Payment
from ..security.rbac import require_roles

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/", response_model=List[Payment])
async def list_payments(
    session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "tenant", "auditor"]))
) -> list[Payment]:
    return [
        Payment(
            id=1,
            invoice_id=1,
            amount=50.0,
            processed_at=datetime.utcnow(),
            status="pending",
            provider_reference="psp-123",
        )
    ]


@router.post("/", response_model=Payment)
async def create_payment(
    payment: Payment, session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "tenant"]))
) -> Payment:
    return payment
