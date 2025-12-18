from celery import shared_task


@shared_task
def handle_psp_webhook(event: dict) -> dict:
    return {"status": "processed", "event": event}
