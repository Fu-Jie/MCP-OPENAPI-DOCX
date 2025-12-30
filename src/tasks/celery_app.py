"""Celery application configuration.

This module configures the Celery application for background
task processing.
"""

from celery import Celery

from src.core.config import get_settings

settings = get_settings()

# Create Celery application
celery_app = Celery(
    "docx_tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_default_queue="docx_default",
    task_queues={
        "docx_default": {},
        "docx_export": {},
        "docx_process": {},
        "docx_notification": {},
    },
    task_routes={
        "src.tasks.document_tasks.*": {"queue": "docx_process"},
        "src.tasks.notification_tasks.*": {"queue": "docx_notification"},
    },
    beat_schedule={
        "cleanup-temp-files": {
            "task": "src.tasks.maintenance_tasks.cleanup_temp_files",
            "schedule": 3600.0,  # Every hour
        },
        "backup-documents": {
            "task": "src.tasks.document_tasks.scheduled_backup",
            "schedule": 86400.0,  # Every day
        },
    },
)

# Auto-discover tasks in the tasks package
celery_app.autodiscover_tasks(["src.tasks"])
