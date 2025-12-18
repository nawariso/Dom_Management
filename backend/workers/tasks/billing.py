from celery import shared_task


@shared_task
def generate_billing_cycles() -> str:
    return "billing cycles generated"
