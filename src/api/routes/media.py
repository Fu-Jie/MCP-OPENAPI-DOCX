"""Media routes.

This module provides endpoints for image and media operations.
"""

import os
from typing import Any

from fastapi import APIRouter, File, UploadFile

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.media_handler import MediaHandler
from src.models.schemas import ImageUpdate

router = APIRouter(prefix="/documents/{document_id}/media")


def get_media_handler(document_id: str) -> tuple[DocumentHandler, MediaHandler]:
    """Get media handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, MediaHandler(doc_handler.document)


@router.get(
    "/images",
    summary="Get All Images",
    description="Get all images in the document.",
)
async def get_images(document_id: str) -> dict[str, Any]:
    """Get all images.

    Args:
        document_id: Document UUID.

    Returns:
        List of images.
    """
    _, handler = get_media_handler(document_id)
    count = handler.get_image_count()

    images = []
    for i in range(count):
        img = handler.get_image_info(i)
        images.append(
            {
                "index": img.index,
                "width": img.width,
                "height": img.height,
            }
        )

    return {
        "document_id": document_id,
        "count": count,
        "images": images,
    }


@router.post(
    "/images",
    summary="Insert Image",
    description="Insert an image into the document.",
)
async def insert_image(
    document_id: str,
    file: UploadFile = File(...),
    paragraph_index: int | None = None,
    width: float | None = None,
    height: float | None = None,
) -> dict[str, Any]:
    """Insert an image.

    Args:
        document_id: Document UUID.
        file: Image file.
        paragraph_index: Optional paragraph index.
        width: Optional width in inches.
        height: Optional height in inches.

    Returns:
        Inserted image information.
    """
    doc_handler, handler = get_media_handler(document_id)

    # Read image data
    content = await file.read()

    index = handler.insert_image_from_bytes(
        image_data=content,
        filename=file.filename or "image.png",
        paragraph_index=paragraph_index,
        width=width,
        height=height,
    )

    doc_handler.save_document()

    return {
        "index": index,
        "filename": file.filename,
        "width": width,
        "height": height,
    }


@router.get(
    "/images/{index}",
    summary="Get Image",
    description="Get image information by index.",
)
async def get_image(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Get image information.

    Args:
        document_id: Document UUID.
        index: Image index.

    Returns:
        Image information.
    """
    _, handler = get_media_handler(document_id)
    img = handler.get_image_info(index)

    return {
        "index": img.index,
        "width": img.width,
        "height": img.height,
    }


@router.put(
    "/images/{index}",
    summary="Update Image",
    description="Update image properties.",
)
async def update_image(
    document_id: str,
    index: int,
    data: ImageUpdate,
) -> dict[str, Any]:
    """Update an image.

    Args:
        document_id: Document UUID.
        index: Image index.
        data: Update data.

    Returns:
        Updated image information.
    """
    doc_handler, handler = get_media_handler(document_id)

    handler.resize_image(index, data.width, data.height)
    doc_handler.save_document()

    return {
        "index": index,
        "width": data.width,
        "height": data.height,
        "updated": True,
    }


@router.delete(
    "/images/{index}",
    summary="Delete Image",
    description="Delete an image from the document.",
)
async def delete_image(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Delete an image.

    Args:
        document_id: Document UUID.
        index: Image index.

    Returns:
        Deletion confirmation.
    """
    doc_handler, handler = get_media_handler(document_id)
    handler.delete_image(index)
    doc_handler.save_document()

    return {"deleted": True, "index": index}
