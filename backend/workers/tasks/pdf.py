from celery import shared_task


@shared_task
def render_invoice_pdf(invoice_id: int) -> str:
    return f"pdf for invoice {invoice_id} generated"
