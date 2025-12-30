"""Celery tasks package.

This package contains async task definitions for background
processing using Celery.
"""

from src.tasks.celery_app import celery_app
from src.tasks.document_tasks import (
    backup_document_task,
    export_document_task,
    process_document_task,
)
from src.tasks.notification_tasks import (
    send_email_notification,
    send_webhook_notification,
)

__all__ = [
    "celery_app",
    "export_document_task",
    "process_document_task",
    "backup_document_task",
    "send_email_notification",
    "send_webhook_notification",
]
