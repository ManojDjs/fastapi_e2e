"""
# celery_app.py
# This module initializes the Celery application for the FastAPI project.
# It configures the broker and result backend, and sets the task serializer.
#"""

from celery import Celery

from .config.config import config

# Initialize Celery
celery_app = Celery(
    "tasks",
    broker=config.get_celery_broker_url(),
    backend=config.get_celery_results_backend(),
)
celery_app.autodiscover_tasks(packages=["src"])
celery_app.conf.update(task_serializer="json", accept_content=["json"])
