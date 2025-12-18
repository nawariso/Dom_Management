from celery import shared_task


@shared_task
def send_notification(target: str, message: str) -> str:
    return f"sent to {target}: {message}"
