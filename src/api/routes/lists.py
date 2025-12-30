"""List routes.

This module provides endpoints for list operations.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.enums import ListType, NumberingFormat
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.list_handler import ListHandler
from src.models.schemas import ListCreate, ListItemCreate

router = APIRouter(prefix="/documents/{document_id}/lists")


def get_list_handler(document_id: str) -> tuple[DocumentHandler, ListHandler]:
    """Get list handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, ListHandler(doc_handler.document)


@router.post(
    "/bullet",
    summary="Create Bullet List",
    description="Create a bullet list.",
)
async def create_bullet_list(
    document_id: str,
    items: list[str],
) -> dict[str, Any]:
    """Create a bullet list.

    Args:
        document_id: Document UUID.
        items: List items.

    Returns:
        Created list information.
    """
    doc_handler, handler = get_list_handler(document_id)
    start_index = handler.create_bullet_list(items)
    doc_handler.save_document()

    return {
        "type": "bullet",
        "start_index": start_index,
        "items": items,
    }


@router.post(
    "/numbered",
    summary="Create Numbered List",
    description="Create a numbered list.",
)
async def create_numbered_list(
    document_id: str,
    items: list[str],
    numbering_format: str = "decimal",
) -> dict[str, Any]:
    """Create a numbered list.

    Args:
        document_id: Document UUID.
        items: List items.
        numbering_format: Numbering format.

    Returns:
        Created list information.
    """
    doc_handler, handler = get_list_handler(document_id)

    fmt = NumberingFormat.DECIMAL
    try:
        fmt = NumberingFormat(numbering_format)
    except ValueError:
        pass

    start_index = handler.create_numbered_list(items, fmt)
    doc_handler.save_document()

    return {
        "type": "numbered",
        "start_index": start_index,
        "numbering_format": numbering_format,
        "items": items,
    }


@router.post(
    "/multilevel",
    summary="Create Multi-level List",
    description="Create a multi-level list.",
)
async def create_multilevel_list(
    document_id: str,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create a multi-level list.

    Args:
        document_id: Document UUID.
        items: List items with levels.

    Returns:
        Created list information.
    """
    doc_handler, handler = get_list_handler(document_id)

    # Convert to tuples
    item_tuples = [(item["text"], item.get("level", 0)) for item in items]
    start_index = handler.create_multilevel_list(item_tuples)
    doc_handler.save_document()

    return {
        "type": "multilevel",
        "start_index": start_index,
        "items": items,
    }


@router.post(
    "/item",
    summary="Add List Item",
    description="Add a single list item.",
)
async def add_list_item(
    document_id: str,
    text: str,
    list_type: str = "bullet",
    level: int = 0,
) -> dict[str, Any]:
    """Add a list item.

    Args:
        document_id: Document UUID.
        text: Item text.
        list_type: Type of list.
        level: Indentation level.

    Returns:
        Created item information.
    """
    doc_handler, handler = get_list_handler(document_id)

    lt = ListType.BULLET if list_type == "bullet" else ListType.NUMBERED
    index = handler.add_list_item(text, lt, level)
    doc_handler.save_document()

    return {
        "index": index,
        "text": text,
        "list_type": list_type,
        "level": level,
    }


@router.put(
    "/paragraphs/{paragraph_index}/convert",
    summary="Convert to List",
    description="Convert a paragraph to a list item.",
)
async def convert_to_list(
    document_id: str,
    paragraph_index: int,
    list_type: str = "bullet",
) -> dict[str, Any]:
    """Convert a paragraph to a list item.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.
        list_type: Type of list.

    Returns:
        Conversion confirmation.
    """
    doc_handler, handler = get_list_handler(document_id)

    lt = ListType.BULLET if list_type == "bullet" else ListType.NUMBERED
    handler.convert_to_list(paragraph_index, lt)
    doc_handler.save_document()

    return {
        "converted": True,
        "paragraph_index": paragraph_index,
        "list_type": list_type,
    }


@router.delete(
    "/paragraphs/{paragraph_index}/formatting",
    summary="Remove List Formatting",
    description="Remove list formatting from a paragraph.",
)
async def remove_list_formatting(
    document_id: str,
    paragraph_index: int,
) -> dict[str, Any]:
    """Remove list formatting.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.

    Returns:
        Removal confirmation.
    """
    doc_handler, handler = get_list_handler(document_id)
    handler.remove_list_formatting(paragraph_index)
    doc_handler.save_document()

    return {
        "removed": True,
        "paragraph_index": paragraph_index,
    }


@router.post(
    "/paragraphs/{paragraph_index}/indent",
    summary="Indent List Item",
    description="Increase the indentation of a list item.",
)
async def indent_item(
    document_id: str,
    paragraph_index: int,
) -> dict[str, Any]:
    """Indent a list item.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.

    Returns:
        Indentation confirmation.
    """
    doc_handler, handler = get_list_handler(document_id)
    handler.indent_list_item(paragraph_index)
    doc_handler.save_document()

    return {"indented": True, "paragraph_index": paragraph_index}


@router.post(
    "/paragraphs/{paragraph_index}/outdent",
    summary="Outdent List Item",
    description="Decrease the indentation of a list item.",
)
async def outdent_item(
    document_id: str,
    paragraph_index: int,
) -> dict[str, Any]:
    """Outdent a list item.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.

    Returns:
        Outdentation confirmation.
    """
    doc_handler, handler = get_list_handler(document_id)
    handler.outdent_list_item(paragraph_index)
    doc_handler.save_document()

    return {"outdented": True, "paragraph_index": paragraph_index}
