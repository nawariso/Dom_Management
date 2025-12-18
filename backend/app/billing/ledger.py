from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional

from sqlalchemy.orm import Session

from backend.app.models import AuditLog, Invoice, Payment


@dataclass(frozen=True)
class LedgerEntry:
    action: str
    entity_type: str
    entity_id: int
    amount: Decimal
    currency: str
    idempotency_key: str
    created_at: datetime


def record_ledger_entry(
    session: Session,
    invoice: Invoice,
    payment: Payment,
    idempotency_key: str,
    currency: str = "THB",
) -> LedgerEntry:
    """
    Persist an immutable ledger entry keyed by idempotency_key. Subsequent calls with
    the same key will return the existing entry instead of mutating history.
    """

    existing: Optional[AuditLog] = None
    for log in (
        session.query(AuditLog)
        .filter(
            AuditLog.action == "payment_recorded",
            AuditLog.entity_type == "invoice",
            AuditLog.entity_id == invoice.id,
        )
        .all()
    ):
        metadata: Dict = log.metadata or {}
        if metadata.get("idempotency_key") == idempotency_key:
            existing = log
            break

    if existing:
        metadata = existing.metadata or {}
        return LedgerEntry(
            action=existing.action,
            entity_type=existing.entity_type,
            entity_id=existing.entity_id,
            amount=Decimal(str(metadata.get("amount", "0"))),
            currency=str(metadata.get("currency", currency)),
            idempotency_key=idempotency_key,
            created_at=existing.created_at,
        )

    metadata = {
        "payment_id": payment.id,
        "amount": str(payment.amount),
        "currency": currency,
        "idempotency_key": idempotency_key,
    }
    audit = AuditLog(
        actor="system",
        action="payment_recorded",
        entity_type="invoice",
        entity_id=invoice.id,
        metadata=metadata,
    )
    session.add(audit)
    session.flush()

    return LedgerEntry(
        action=audit.action,
        entity_type=audit.entity_type,
        entity_id=audit.entity_id,
        amount=Decimal(str(metadata["amount"])),
        currency=currency,
        idempotency_key=idempotency_key,
        created_at=audit.created_at,
    )
