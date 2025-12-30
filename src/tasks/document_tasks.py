"""Document-related Celery tasks.

This module contains background tasks for document
processing, export, and backup operations.
"""

import os
import shutil
from datetime import datetime
from typing import Any

from src.tasks.celery_app import celery_app
from src.core.config import get_settings
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)
settings = get_settings()


@celery_app.task(bind=True, name="document.export")
def export_document_task(
    self,
    document_id: str,
    format: str,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Export a document to specified format.

    Args:
        self: Celery task instance.
        document_id: Document ID to export.
        format: Export format (pdf, html, markdown, text).
        options: Optional export options.

    Returns:
        Export result with file path.
    """
    logger.info(
        "Starting document export",
        document_id=document_id,
        format=format,
    )

    try:
        # Import here to avoid circular imports
        from src.handlers.document_handler import DocumentHandler

        handler = DocumentHandler()

        # Get document path (simplified for async context)
        doc_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

        if not os.path.exists(doc_path):
            return {
                "success": False,
                "error": f"Document {document_id} not found",
            }

        # Generate output path
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(settings.export_dir, document_id)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"export_{timestamp}.{format}")

        # Perform export based on format
        if format == "html":
            doc = handler.load_document(doc_path)
            html = _convert_to_html(doc)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
        elif format == "text":
            doc = handler.load_document(doc_path)
            text = "\n".join(p.text for p in doc.paragraphs)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
        elif format == "markdown":
            doc = handler.load_document(doc_path)
            md = _convert_to_markdown(doc)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md)
        else:
            return {
                "success": False,
                "error": f"Unsupported format: {format}",
            }

        logger.info(
            "Document export completed",
            document_id=document_id,
            output_path=output_path,
        )

        return {
            "success": True,
            "document_id": document_id,
            "format": format,
            "output_path": output_path,
        }

    except Exception as e:
        logger.error(
            "Document export failed",
            document_id=document_id,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


@celery_app.task(bind=True, name="document.process")
def process_document_task(
    self,
    document_id: str,
    operations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Process document with batch operations.

    Args:
        self: Celery task instance.
        document_id: Document ID to process.
        operations: List of operations to perform.

    Returns:
        Processing result.
    """
    logger.info(
        "Starting document processing",
        document_id=document_id,
        operations_count=len(operations),
    )

    try:
        from src.handlers.document_handler import DocumentHandler

        handler = DocumentHandler()
        doc_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

        if not os.path.exists(doc_path):
            return {
                "success": False,
                "error": f"Document {document_id} not found",
            }

        doc = handler.load_document(doc_path)
        results = []

        for i, op in enumerate(operations):
            self.update_state(
                state="PROGRESS",
                meta={"current": i + 1, "total": len(operations)},
            )

            op_type = op.get("type")
            op_params = op.get("params", {})

            try:
                # Process operation based on type
                result = _process_operation(doc, op_type, op_params)
                results.append({"index": i, "success": True, "result": result})
            except Exception as e:
                results.append({"index": i, "success": False, "error": str(e)})

        handler.save_document(doc, doc_path)

        logger.info(
            "Document processing completed",
            document_id=document_id,
            results_count=len(results),
        )

        return {
            "success": True,
            "document_id": document_id,
            "results": results,
        }

    except Exception as e:
        logger.error(
            "Document processing failed",
            document_id=document_id,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


@celery_app.task(bind=True, name="document.backup")
def backup_document_task(
    self,
    document_id: str,
    backup_dir: str | None = None,
) -> dict[str, Any]:
    """Backup a document.

    Args:
        self: Celery task instance.
        document_id: Document ID to backup.
        backup_dir: Optional backup directory.

    Returns:
        Backup result with path.
    """
    logger.info(
        "Starting document backup",
        document_id=document_id,
    )

    try:
        doc_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

        if not os.path.exists(doc_path):
            return {
                "success": False,
                "error": f"Document {document_id} not found",
            }

        # Create backup directory
        backup_base = backup_dir or os.path.join(settings.upload_dir, "backups")
        backup_folder = os.path.join(backup_base, document_id)
        os.makedirs(backup_folder, exist_ok=True)

        # Create backup with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_folder, f"backup_{timestamp}.docx")

        shutil.copy2(doc_path, backup_path)

        logger.info(
            "Document backup completed",
            document_id=document_id,
            backup_path=backup_path,
        )

        return {
            "success": True,
            "document_id": document_id,
            "backup_path": backup_path,
        }

    except Exception as e:
        logger.error(
            "Document backup failed",
            document_id=document_id,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


@celery_app.task(name="document.scheduled_backup")
def scheduled_backup() -> dict[str, Any]:
    """Scheduled task to backup all documents.

    Returns:
        Backup summary.
    """
    logger.info("Starting scheduled backup")

    try:
        upload_dir = settings.upload_dir
        backed_up = 0
        failed = 0

        for filename in os.listdir(upload_dir):
            if filename.endswith(".docx"):
                doc_id = filename[:-5]
                result = backup_document_task.delay(doc_id)
                if result:
                    backed_up += 1
                else:
                    failed += 1

        logger.info(
            "Scheduled backup completed",
            backed_up=backed_up,
            failed=failed,
        )

        return {
            "success": True,
            "backed_up": backed_up,
            "failed": failed,
        }

    except Exception as e:
        logger.error("Scheduled backup failed", error=str(e))
        return {"success": False, "error": str(e)}


def _convert_to_html(doc) -> str:
    """Convert document to HTML."""
    html_parts = ["<!DOCTYPE html><html><body>"]
    for para in doc.paragraphs:
        html_parts.append(f"<p>{para.text}</p>")
    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def _convert_to_markdown(doc) -> str:
    """Convert document to Markdown."""
    md_parts = []
    for para in doc.paragraphs:
        style = para.style.name if para.style else ""
        if "Heading 1" in style:
            md_parts.append(f"# {para.text}")
        elif "Heading 2" in style:
            md_parts.append(f"## {para.text}")
        else:
            md_parts.append(para.text)
        md_parts.append("")
    return "\n".join(md_parts)


def _process_operation(doc, op_type: str, params: dict[str, Any]) -> Any:
    """Process a single operation."""
    # Placeholder for operation processing
    return {"type": op_type, "params": params}
