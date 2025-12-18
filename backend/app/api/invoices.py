from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import Invoice
from ..security.rbac import require_roles

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", response_model=List[Invoice])
async def list_invoices(
    session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin", "tenant", "auditor"]))
) -> list[Invoice]:
    return [
        Invoice(
            id=1,
            tenant_id=1,
            amount_due=100.0,
            due_date=datetime.utcnow(),
            status="open",
        )
    ]


@router.post("/", response_model=Invoice)
async def create_invoice(
    invoice: Invoice, session: AsyncSession = Depends(get_session), user=Depends(require_roles(["admin"]))
) -> Invoice:
    return invoice
