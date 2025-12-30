"""Document routes.

This module provides endpoints for document CRUD operations.
"""

import os
import uuid
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.api.dependencies import CurrentUserOptional, DocHandler
from src.core.config import get_settings
from src.core.constants import DOCX_MIME_TYPE
from src.core.exceptions import DocumentNotFoundError, InvalidDocumentError
from src.models.schemas import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
    PaginatedResponse,
    SuccessResponse,
)

router = APIRouter(prefix="/documents")


@router.get(
    "",
    response_model=PaginatedResponse[dict[str, Any]],
    summary="List Documents",
    description="Get a paginated list of documents.",
)
async def list_documents(
    page: int = 1,
    size: int = 20,
    status_filter: str | None = None,
) -> PaginatedResponse[dict[str, Any]]:
    """List all documents with pagination.

    Args:
        page: Page number (1-based).
        size: Number of items per page.
        status_filter: Optional status filter.

    Returns:
        Paginated list of documents.
    """
    # Placeholder implementation
    return PaginatedResponse(
        items=[],
        total=0,
        page=page,
        size=size,
        pages=0,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create Document",
    description="Create a new empty document.",
)
async def create_document(
    data: DocumentCreate,
    handler: DocHandler,
) -> dict[str, Any]:
    """Create a new document.

    Args:
        data: Document creation data.
        handler: Document handler.

    Returns:
        Created document information.
    """
    settings = get_settings()
    doc = handler.create_document()

    # Set metadata
    handler.set_metadata(title=data.title)
    if data.description:
        handler.set_metadata(comments=data.description)

    # Save document
    doc_uuid = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{doc_uuid}.docx")
    handler.save_document(file_path)

    return {
        "uuid": doc_uuid,
        "title": data.title,
        "description": data.description,
        "file_path": file_path,
        "status": "draft",
        "version": 1,
    }


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload Document",
    description="Upload a DOCX file.",
)
async def upload_document(
    file: UploadFile = File(...),
    handler: DocHandler = Depends(),
) -> dict[str, Any]:
    """Upload a DOCX document.

    Args:
        file: Uploaded file.
        handler: Document handler.

    Returns:
        Uploaded document information.
    """
    settings = get_settings()

    # Validate file type
    if not file.filename or not file.filename.endswith(".docx"):
        raise InvalidDocumentError("Only .docx files are supported")

    # Read and validate content
    content = await file.read()
    handler.validate_bytes(content)

    # Save file
    doc_uuid = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{doc_uuid}.docx")

    with open(file_path, "wb") as f:
        f.write(content)

    # Open and get metadata
    handler.open_from_bytes(content)
    metadata = handler.get_metadata()

    return {
        "uuid": doc_uuid,
        "title": metadata.title or file.filename,
        "file_path": file_path,
        "file_size": len(content),
        "status": "draft",
        "version": 1,
    }


@router.get(
    "/{document_id}",
    summary="Get Document",
    description="Get document details by ID.",
)
async def get_document(
    document_id: str,
    handler: DocHandler,
) -> dict[str, Any]:
    """Get a document by ID.

    Args:
        document_id: Document UUID.
        handler: Document handler.

    Returns:
        Document information.

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler.open_document(file_path)
    metadata = handler.get_metadata()
    structure = handler.get_document_structure()

    return {
        "uuid": document_id,
        "title": metadata.title or document_id,
        "author": metadata.author,
        "subject": metadata.subject,
        "keywords": metadata.keywords,
        "created": metadata.created.isoformat() if metadata.created else None,
        "modified": metadata.modified.isoformat() if metadata.modified else None,
        "structure": structure,
        "word_count": handler.get_word_count(),
        "character_count": handler.get_character_count(),
    }


@router.put(
    "/{document_id}",
    summary="Update Document",
    description="Update document metadata.",
)
async def update_document(
    document_id: str,
    data: DocumentUpdate,
    handler: DocHandler,
) -> dict[str, Any]:
    """Update a document.

    Args:
        document_id: Document UUID.
        data: Update data.
        handler: Document handler.

    Returns:
        Updated document information.

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler.open_document(file_path)

    # Update metadata
    if data.title is not None:
        handler.set_metadata(title=data.title)
    if data.description is not None:
        handler.set_metadata(comments=data.description)

    handler.save_document()

    return {
        "uuid": document_id,
        "title": data.title,
        "description": data.description,
        "updated": True,
    }


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document",
    description="Delete a document.",
)
async def delete_document(document_id: str) -> None:
    """Delete a document.

    Args:
        document_id: Document UUID.

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    os.remove(file_path)


@router.get(
    "/{document_id}/download",
    summary="Download Document",
    description="Download the document file.",
)
async def download_document(
    document_id: str,
    handler: DocHandler,
) -> dict[str, Any]:
    """Get download URL for a document.

    Args:
        document_id: Document UUID.
        handler: Document handler.

    Returns:
        Download information.

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    return {
        "uuid": document_id,
        "download_url": f"/api/v1/documents/{document_id}/file",
        "mime_type": DOCX_MIME_TYPE,
    }


@router.get(
    "/{document_id}/content",
    summary="Get Document Content",
    description="Get the full text content of the document.",
)
async def get_document_content(
    document_id: str,
    handler: DocHandler,
) -> dict[str, Any]:
    """Get document text content.

    Args:
        document_id: Document UUID.
        handler: Document handler.

    Returns:
        Document content.

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    handler.open_document(file_path)

    return {
        "uuid": document_id,
        "content": handler.get_all_text(),
        "paragraph_count": handler.get_paragraph_count(),
    }
