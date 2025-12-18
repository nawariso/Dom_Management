from datetime import date
from decimal import Decimal
from typing import Iterable, List

from sqlalchemy.orm import Session

from backend.app.billing import calculate_tariff_charge, prorate_amount, record_ledger_entry
from backend.app.models import Invoice, Payment, Tariff, UsageRecord


class BillingService:
    def __init__(self, session: Session):
        self.session = session

    def compute_usage_cost(self, usage: UsageRecord, tariff: Tariff) -> Decimal:
        usage.cost = calculate_tariff_charge(usage.consumption, tariff)
        usage.tariff = tariff
        self.session.add(usage)
        return usage.cost

    def generate_invoice(
        self,
        tenant_id: int,
        room_id: int,
        period_start: date,
        period_end: date,
        usage_records: Iterable[UsageRecord],
        base_amount: Decimal = Decimal("0.00"),
        status: str = "pending",
    ) -> Invoice:
        total = base_amount
        for record in usage_records:
            total += Decimal(record.cost)
        invoice = Invoice(
            tenant_id=tenant_id,
            room_id=room_id,
            period_start=period_start,
            period_end=period_end,
            total_amount=total,
            status=status,
            due_date=period_end,
        )
        self.session.add(invoice)
        return invoice

    def apply_proration(self, amount: Decimal, active_from: date, active_to: date, period_start: date, period_end: date) -> Decimal:
        return prorate_amount(amount, active_from, active_to, period_start, period_end)

    def record_payment(self, invoice: Invoice, payment: Payment, idempotency_key: str) -> None:
        record_ledger_entry(self.session, invoice, payment, idempotency_key)
        payment.status = "succeeded"
        invoice.status = "paid"
        self.session.add(payment)
        self.session.add(invoice)
