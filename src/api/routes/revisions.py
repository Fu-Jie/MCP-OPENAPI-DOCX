"""Revision routes.

This module provides endpoints for revision tracking operations.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.enums import RevisionAction
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.revision_handler import RevisionHandler
from src.models.schemas import RevisionCreate, RevisionAccept

router = APIRouter(prefix="/documents/{document_id}/revisions")

# Store handlers per document session (simplified)
_revision_handlers: dict[str, RevisionHandler] = {}


def get_revision_handler(document_id: str) -> tuple[DocumentHandler, RevisionHandler]:
    """Get revision handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)

    if document_id not in _revision_handlers:
        _revision_handlers[document_id] = RevisionHandler(doc_handler.document)

    return doc_handler, _revision_handlers[document_id]


@router.get(
    "",
    summary="Get All Revisions",
    description="Get all revisions in the document.",
)
async def get_revisions(document_id: str) -> dict[str, Any]:
    """Get all revisions.

    Args:
        document_id: Document UUID.

    Returns:
        List of revisions.
    """
    _, handler = get_revision_handler(document_id)
    revisions = handler.get_all_revisions()

    return {
        "document_id": document_id,
        "count": len(revisions),
        "revisions": handler.export_revisions(),
    }


@router.get(
    "/stats",
    summary="Get Revision Statistics",
    description="Get revision count statistics.",
)
async def get_revision_stats(document_id: str) -> dict[str, Any]:
    """Get revision statistics.

    Args:
        document_id: Document UUID.

    Returns:
        Revision statistics.
    """
    _, handler = get_revision_handler(document_id)
    return handler.get_revision_count()


@router.get(
    "/pending",
    summary="Get Pending Revisions",
    description="Get all pending revisions.",
)
async def get_pending_revisions(document_id: str) -> dict[str, Any]:
    """Get pending revisions.

    Args:
        document_id: Document UUID.

    Returns:
        List of pending revisions.
    """
    _, handler = get_revision_handler(document_id)
    revisions = handler.get_pending_revisions()

    return {
        "document_id": document_id,
        "count": len(revisions),
        "revisions": revisions,
    }


@router.get(
    "/{revision_id}",
    summary="Get Revision",
    description="Get a specific revision by ID.",
)
async def get_revision(
    document_id: str,
    revision_id: int,
) -> dict[str, Any]:
    """Get a revision.

    Args:
        document_id: Document UUID.
        revision_id: Revision ID.

    Returns:
        Revision information.
    """
    _, handler = get_revision_handler(document_id)
    return handler.get_revision(revision_id)


@router.post(
    "",
    summary="Add Revision",
    description="Record a revision.",
)
async def add_revision(
    document_id: str,
    data: RevisionCreate,
    author: str = "User",
) -> dict[str, Any]:
    """Add a revision.

    Args:
        document_id: Document UUID.
        data: Revision creation data.
        author: Author name.

    Returns:
        Created revision information.
    """
    doc_handler, handler = get_revision_handler(document_id)
    revision = handler.add_revision(
        action=data.action,
        author=author,
        paragraph_index=data.paragraph_index or 0,
        original_content=data.original_content,
        new_content=data.new_content,
    )
    doc_handler.save_document()

    return revision


@router.post(
    "/{revision_id}/accept",
    summary="Accept Revision",
    description="Accept a revision.",
)
async def accept_revision(
    document_id: str,
    revision_id: int,
    accepted_by: str = "User",
) -> dict[str, Any]:
    """Accept a revision.

    Args:
        document_id: Document UUID.
        revision_id: Revision ID.
        accepted_by: User accepting the revision.

    Returns:
        Updated revision information.
    """
    doc_handler, handler = get_revision_handler(document_id)
    revision = handler.accept_revision(revision_id, accepted_by)
    doc_handler.save_document()

    return revision


@router.post(
    "/{revision_id}/reject",
    summary="Reject Revision",
    description="Reject a revision.",
)
async def reject_revision(
    document_id: str,
    revision_id: int,
    rejected_by: str = "User",
) -> dict[str, Any]:
    """Reject a revision.

    Args:
        document_id: Document UUID.
        revision_id: Revision ID.
        rejected_by: User rejecting the revision.

    Returns:
        Updated revision information.
    """
    doc_handler, handler = get_revision_handler(document_id)
    revision = handler.reject_revision(revision_id, rejected_by)
    doc_handler.save_document()

    return revision


@router.post(
    "/accept-all",
    summary="Accept All Revisions",
    description="Accept all pending revisions.",
)
async def accept_all_revisions(
    document_id: str,
    accepted_by: str = "User",
) -> dict[str, Any]:
    """Accept all revisions.

    Args:
        document_id: Document UUID.
        accepted_by: User accepting the revisions.

    Returns:
        Number of accepted revisions.
    """
    doc_handler, handler = get_revision_handler(document_id)
    count = handler.accept_all_revisions(accepted_by)
    doc_handler.save_document()

    return {"accepted": count}


@router.post(
    "/reject-all",
    summary="Reject All Revisions",
    description="Reject all pending revisions.",
)
async def reject_all_revisions(
    document_id: str,
    rejected_by: str = "User",
) -> dict[str, Any]:
    """Reject all revisions.

    Args:
        document_id: Document UUID.
        rejected_by: User rejecting the revisions.

    Returns:
        Number of rejected revisions.
    """
    doc_handler, handler = get_revision_handler(document_id)
    count = handler.reject_all_revisions(rejected_by)
    doc_handler.save_document()

    return {"rejected": count}


@router.post(
    "/tracking/enable",
    summary="Enable Tracking",
    description="Enable revision tracking.",
)
async def enable_tracking(document_id: str) -> dict[str, Any]:
    """Enable revision tracking.

    Args:
        document_id: Document UUID.

    Returns:
        Confirmation.
    """
    _, handler = get_revision_handler(document_id)
    handler.enable_tracking()

    return {"tracking": True}


@router.post(
    "/tracking/disable",
    summary="Disable Tracking",
    description="Disable revision tracking.",
)
async def disable_tracking(document_id: str) -> dict[str, Any]:
    """Disable revision tracking.

    Args:
        document_id: Document UUID.

    Returns:
        Confirmation.
    """
    _, handler = get_revision_handler(document_id)
    handler.disable_tracking()

    return {"tracking": False}


@router.get(
    "/tracking/status",
    summary="Get Tracking Status",
    description="Get revision tracking status.",
)
async def get_tracking_status(document_id: str) -> dict[str, Any]:
    """Get tracking status.

    Args:
        document_id: Document UUID.

    Returns:
        Tracking status.
    """
    _, handler = get_revision_handler(document_id)

    return {"tracking": handler.tracking_enabled}
