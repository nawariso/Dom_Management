from datetime import date
from decimal import Decimal

from backend.app.billing import record_ledger_entry
from backend.app.models import Invoice, Payment


def test_record_payment_is_idempotent(db_session):
    invoice = Invoice(
        total_amount=Decimal("100.00"),
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        due_date=date(2024, 2, 7),
        status="pending",
    )
    payment = Payment(invoice=invoice, amount=Decimal("100.00"), transaction_ref="abc", status="initiated")
    db_session.add_all([invoice, payment])
    db_session.flush()

    first = record_ledger_entry(db_session, invoice, payment, idempotency_key="ref-1")
    second = record_ledger_entry(db_session, invoice, payment, idempotency_key="ref-1")

    assert first == second
    assert first.idempotency_key == "ref-1"
    assert payment.invoice_id == invoice.id
