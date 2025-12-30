"""Export routes.

This module provides endpoints for document export operations.
"""

import os
import uuid
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.enums import ExportFormat
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.models.schemas import ExportRequest, ExportResponse

router = APIRouter(prefix="/documents/{document_id}/export")


@router.post(
    "",
    summary="Export Document",
    description="Export document to a different format.",
)
async def export_document(
    document_id: str,
    data: ExportRequest,
) -> ExportResponse:
    """Export a document.

    Args:
        document_id: Document UUID.
        data: Export request data.

    Returns:
        Export response with task ID and status.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    task_id = str(uuid.uuid4())

    # For now, return a placeholder response
    # Full implementation would use Celery for async export
    return ExportResponse(
        task_id=task_id,
        status="pending",
        download_url=None,
    )


@router.get(
    "/html",
    summary="Export to HTML",
    description="Export document to HTML format.",
)
async def export_to_html(document_id: str) -> dict[str, Any]:
    """Export to HTML.

    Args:
        document_id: Document UUID.

    Returns:
        HTML content.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)

    # Simple HTML conversion
    paragraphs = handler.document.paragraphs
    html_parts = ["<html><body>"]

    for para in paragraphs:
        style = para.style.name if para.style else ""
        if style.startswith("Heading"):
            level = style.replace("Heading ", "") or "1"
            try:
                level = int(level)
            except ValueError:
                level = 1
            html_parts.append(f"<h{level}>{para.text}</h{level}>")
        else:
            html_parts.append(f"<p>{para.text}</p>")

    html_parts.append("</body></html>")

    return {
        "format": "html",
        "content": "\n".join(html_parts),
    }


@router.get(
    "/markdown",
    summary="Export to Markdown",
    description="Export document to Markdown format.",
)
async def export_to_markdown(document_id: str) -> dict[str, Any]:
    """Export to Markdown.

    Args:
        document_id: Document UUID.

    Returns:
        Markdown content.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)

    # Simple Markdown conversion
    paragraphs = handler.document.paragraphs
    md_parts = []

    for para in paragraphs:
        style = para.style.name if para.style else ""
        if style.startswith("Heading"):
            level = style.replace("Heading ", "") or "1"
            try:
                level = int(level)
            except ValueError:
                level = 1
            md_parts.append("#" * level + " " + para.text)
        elif "List Bullet" in style:
            md_parts.append(f"- {para.text}")
        elif "List Number" in style:
            md_parts.append(f"1. {para.text}")
        else:
            md_parts.append(para.text)
        md_parts.append("")

    return {
        "format": "markdown",
        "content": "\n".join(md_parts),
    }


@router.get(
    "/text",
    summary="Export to Text",
    description="Export document to plain text.",
)
async def export_to_text(document_id: str) -> dict[str, Any]:
    """Export to plain text.

    Args:
        document_id: Document UUID.

    Returns:
        Text content.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler = DocumentHandler()
    handler.open_document(file_path)

    return {
        "format": "text",
        "content": handler.get_all_text(),
    }


@router.get(
    "/status/{task_id}",
    summary="Get Export Status",
    description="Get the status of an export task.",
)
async def get_export_status(
    document_id: str,
    task_id: str,
) -> ExportResponse:
    """Get export task status.

    Args:
        document_id: Document UUID.
        task_id: Export task ID.

    Returns:
        Export status.
    """
    # Placeholder - would check Celery task status
    return ExportResponse(
        task_id=task_id,
        status="completed",
        download_url=f"/api/v1/documents/{document_id}/export/download/{task_id}",
    )
