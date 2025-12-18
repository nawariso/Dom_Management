import os

from celery import Celery

BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
BACKEND_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("dom_management", broker=BROKER_URL, backend=BACKEND_URL)
celery_app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json", timezone="UTC")

celery_app.autodiscover_tasks(["backend.workers.tasks"])
