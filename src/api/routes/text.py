"""Text editing routes.

This module provides endpoints for text and paragraph operations.
"""

import os
from typing import Any

from fastapi import APIRouter, Depends

from src.api.dependencies import DocHandler
from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.text_handler import TextHandler
from src.models.schemas import (
    ParagraphCreate,
    ParagraphUpdate,
    TextFormat,
    TextInsert,
    TextReplace,
)

router = APIRouter(prefix="/documents/{document_id}/text")


def get_text_handler(document_id: str) -> TextHandler:
    """Get text handler for a document.

    Args:
        document_id: Document UUID.

    Returns:
        TextHandler instance.

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return TextHandler(doc_handler.document)


@router.get(
    "/paragraphs",
    summary="Get All Paragraphs",
    description="Get all paragraphs in the document.",
)
async def get_paragraphs(document_id: str) -> dict[str, Any]:
    """Get all paragraphs.

    Args:
        document_id: Document UUID.

    Returns:
        List of paragraphs.
    """
    handler = get_text_handler(document_id)
    paragraphs = handler.get_all_paragraphs()

    return {
        "document_id": document_id,
        "count": len(paragraphs),
        "paragraphs": [
            {
                "index": p.index,
                "text": p.text,
                "style": p.style,
                "alignment": p.alignment.value if p.alignment else None,
            }
            for p in paragraphs
        ],
    }


@router.get(
    "/paragraphs/{index}",
    summary="Get Paragraph",
    description="Get a specific paragraph by index.",
)
async def get_paragraph(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Get a paragraph by index.

    Args:
        document_id: Document UUID.
        index: Paragraph index.

    Returns:
        Paragraph information.
    """
    handler = get_text_handler(document_id)
    para = handler.get_paragraph(index)

    return {
        "index": para.index,
        "text": para.text,
        "style": para.style,
        "alignment": para.alignment.value if para.alignment else None,
        "runs": [
            {
                "text": r.text,
                "bold": r.bold,
                "italic": r.italic,
                "underline": r.underline,
                "font_name": r.font_name,
                "font_size": r.font_size,
            }
            for r in para.runs
        ],
    }


@router.post(
    "/paragraphs",
    summary="Add Paragraph",
    description="Add a new paragraph to the document.",
)
async def add_paragraph(
    document_id: str,
    data: ParagraphCreate,
) -> dict[str, Any]:
    """Add a new paragraph.

    Args:
        document_id: Document UUID.
        data: Paragraph data.

    Returns:
        Created paragraph information.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    handler = TextHandler(doc_handler.document)

    index = handler.add_paragraph(
        text=data.text,
        style=data.style,
        alignment=data.alignment,
    )

    doc_handler.save_document()

    return {
        "index": index,
        "text": data.text,
        "style": data.style,
    }


@router.put(
    "/paragraphs/{index}",
    summary="Update Paragraph",
    description="Update a paragraph.",
)
async def update_paragraph(
    document_id: str,
    index: int,
    data: ParagraphUpdate,
) -> dict[str, Any]:
    """Update a paragraph.

    Args:
        document_id: Document UUID.
        index: Paragraph index.
        data: Update data.

    Returns:
        Updated paragraph information.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    handler = TextHandler(doc_handler.document)

    para = handler.update_paragraph(
        index=index,
        text=data.text,
        style=data.style,
        alignment=data.alignment,
    )

    doc_handler.save_document()

    return {
        "index": para.index,
        "text": para.text,
        "style": para.style,
        "updated": True,
    }


@router.delete(
    "/paragraphs/{index}",
    summary="Delete Paragraph",
    description="Delete a paragraph.",
)
async def delete_paragraph(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Delete a paragraph.

    Args:
        document_id: Document UUID.
        index: Paragraph index.

    Returns:
        Deletion confirmation.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    handler = TextHandler(doc_handler.document)

    handler.delete_paragraph(index)
    doc_handler.save_document()

    return {"deleted": True, "index": index}


@router.post(
    "/insert",
    summary="Insert Text",
    description="Insert text at a specific position.",
)
async def insert_text(
    document_id: str,
    data: TextInsert,
) -> dict[str, Any]:
    """Insert text at a position.

    Args:
        document_id: Document UUID.
        data: Insert data.

    Returns:
        Insert confirmation.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    handler = TextHandler(doc_handler.document)

    handler.insert_text(
        paragraph_index=data.paragraph_index,
        offset=data.offset or 0,
        text=data.text,
        format_=data.format,
    )

    doc_handler.save_document()

    return {
        "inserted": True,
        "paragraph_index": data.paragraph_index,
        "text": data.text,
    }


@router.post(
    "/replace",
    summary="Find and Replace",
    description="Find and replace text in the document.",
)
async def find_and_replace(
    document_id: str,
    data: TextReplace,
) -> dict[str, Any]:
    """Find and replace text.

    Args:
        document_id: Document UUID.
        data: Replace data.

    Returns:
        Replace result.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    handler = TextHandler(doc_handler.document)

    count = handler.replace_text(
        find=data.find,
        replace=data.replace,
        case_sensitive=data.case_sensitive,
        whole_word=data.whole_word,
    )

    doc_handler.save_document()

    return {
        "replaced": True,
        "count": count,
        "find": data.find,
        "replace": data.replace,
    }


@router.post(
    "/format",
    summary="Format Text",
    description="Apply formatting to text.",
)
async def format_text(
    document_id: str,
    paragraph_index: int,
    run_index: int,
    format_data: TextFormat,
) -> dict[str, Any]:
    """Apply formatting to a text run.

    Args:
        document_id: Document UUID.
        paragraph_index: Paragraph index.
        run_index: Run index within the paragraph.
        format_data: Formatting to apply.

    Returns:
        Format result.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    from src.handlers.document_handler import DocumentHandler
    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    handler = TextHandler(doc_handler.document)

    run = handler.format_run(
        paragraph_index=paragraph_index,
        run_index=run_index,
        format_=format_data,
    )

    doc_handler.save_document()

    return {
        "formatted": True,
        "paragraph_index": paragraph_index,
        "run_index": run_index,
        "run": {
            "text": run.text,
            "bold": run.bold,
            "italic": run.italic,
        },
    }
