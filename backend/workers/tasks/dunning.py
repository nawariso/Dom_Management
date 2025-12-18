from celery import shared_task


@shared_task
def apply_dunning(invoice_id: int) -> str:
    return f"dunning workflow applied to invoice {invoice_id}"
