"""Style routes.

This module provides endpoints for style operations.
"""

import contextlib
import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.enums import StyleType
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.style_handler import StyleHandler
from src.models.schemas import StyleCreate

router = APIRouter(prefix="/documents/{document_id}/styles")


def get_style_handler(document_id: str) -> tuple[DocumentHandler, StyleHandler]:
    """Get style handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, StyleHandler(doc_handler.document)


@router.get(
    "",
    summary="Get All Styles",
    description="Get all styles in the document.",
)
async def get_styles(
    document_id: str,
    style_type: str | None = None,
) -> dict[str, Any]:
    """Get all styles.

    Args:
        document_id: Document UUID.
        style_type: Optional filter by style type.

    Returns:
        List of styles.
    """
    _, handler = get_style_handler(document_id)

    st = None
    if style_type:
        with contextlib.suppress(ValueError):
            st = StyleType(style_type)

    styles = handler.get_all_styles(st)

    return {
        "document_id": document_id,
        "count": len(styles),
        "styles": [
            {
                "name": s.name,
                "style_type": s.style_type,
                "base_style": s.base_style,
                "font_name": s.font_name,
                "font_size": s.font_size,
                "bold": s.bold,
                "italic": s.italic,
            }
            for s in styles
        ],
    }


@router.get(
    "/builtin",
    summary="Get Built-in Styles",
    description="Get all built-in style names.",
)
async def get_builtin_styles(document_id: str) -> dict[str, Any]:
    """Get built-in styles.

    Args:
        document_id: Document UUID.

    Returns:
        List of built-in style names.
    """
    _, handler = get_style_handler(document_id)
    styles = handler.get_built_in_styles()

    return {
        "document_id": document_id,
        "count": len(styles),
        "styles": styles,
    }


@router.get(
    "/custom",
    summary="Get Custom Styles",
    description="Get all custom style names.",
)
async def get_custom_styles(document_id: str) -> dict[str, Any]:
    """Get custom styles.

    Args:
        document_id: Document UUID.

    Returns:
        List of custom style names.
    """
    _, handler = get_style_handler(document_id)
    styles = handler.get_custom_styles()

    return {
        "document_id": document_id,
        "count": len(styles),
        "styles": styles,
    }


@router.get(
    "/{name}",
    summary="Get Style",
    description="Get a specific style by name.",
)
async def get_style(
    document_id: str,
    name: str,
) -> dict[str, Any]:
    """Get a style.

    Args:
        document_id: Document UUID.
        name: Style name.

    Returns:
        Style information.
    """
    _, handler = get_style_handler(document_id)
    style = handler.get_style(name)

    return {
        "name": style.name,
        "style_type": style.style_type,
        "base_style": style.base_style,
        "font_name": style.font_name,
        "font_size": style.font_size,
        "bold": style.bold,
        "italic": style.italic,
        "color": style.color,
    }


@router.post(
    "",
    summary="Create Style",
    description="Create a new custom style.",
)
async def create_style(
    document_id: str,
    data: StyleCreate,
) -> dict[str, Any]:
    """Create a style.

    Args:
        document_id: Document UUID.
        data: Style creation data.

    Returns:
        Created style information.
    """
    doc_handler, handler = get_style_handler(document_id)
    style = handler.create_style(data)
    doc_handler.save_document()

    return {
        "name": style.name,
        "style_type": style.style_type,
        "created": True,
    }


@router.put(
    "/{name}",
    summary="Update Style",
    description="Update a style.",
)
async def update_style(
    document_id: str,
    name: str,
    updates: dict[str, Any],
) -> dict[str, Any]:
    """Update a style.

    Args:
        document_id: Document UUID.
        name: Style name.
        updates: Style updates.

    Returns:
        Updated style information.
    """
    doc_handler, handler = get_style_handler(document_id)
    style = handler.update_style(name, updates)
    doc_handler.save_document()

    return {
        "name": style.name,
        "updated": True,
    }


@router.delete(
    "/{name}",
    summary="Delete Style",
    description="Delete a custom style.",
)
async def delete_style(
    document_id: str,
    name: str,
) -> dict[str, Any]:
    """Delete a style.

    Args:
        document_id: Document UUID.
        name: Style name.

    Returns:
        Deletion confirmation.
    """
    doc_handler, handler = get_style_handler(document_id)
    handler.delete_style(name)
    doc_handler.save_document()

    return {"deleted": True, "name": name}


@router.post(
    "/apply",
    summary="Apply Style",
    description="Apply a style to a paragraph.",
)
async def apply_style(
    document_id: str,
    paragraph_index: int,
    style_name: str,
) -> dict[str, Any]:
    """Apply a style to a paragraph.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.
        style_name: Style name.

    Returns:
        Application confirmation.
    """
    doc_handler, handler = get_style_handler(document_id)
    handler.apply_style_to_paragraph(paragraph_index, style_name)
    doc_handler.save_document()

    return {
        "applied": True,
        "paragraph_index": paragraph_index,
        "style_name": style_name,
    }


@router.post(
    "/{source_name}/copy",
    summary="Copy Style",
    description="Copy a style with a new name.",
)
async def copy_style(
    document_id: str,
    source_name: str,
    new_name: str,
) -> dict[str, Any]:
    """Copy a style.

    Args:
        document_id: Document UUID.
        source_name: Source style name.
        new_name: New style name.

    Returns:
        Created style information.
    """
    doc_handler, handler = get_style_handler(document_id)
    style = handler.copy_style(source_name, new_name)
    doc_handler.save_document()

    return {
        "name": style.name,
        "source": source_name,
        "copied": True,
    }
