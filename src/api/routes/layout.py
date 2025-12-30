"""Layout routes.

This module provides endpoints for page layout operations.
"""

import contextlib
import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.enums import HeaderFooterType, SectionStart
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.layout_handler import LayoutHandler
from src.models.schemas import PageLayout

router = APIRouter(prefix="/documents/{document_id}/layout")


def get_layout_handler(document_id: str) -> tuple[DocumentHandler, LayoutHandler]:
    """Get layout handler for a document."""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, LayoutHandler(doc_handler.document)


@router.get(
    "/sections",
    summary="Get All Sections",
    description="Get all sections in the document.",
)
async def get_sections(document_id: str) -> dict[str, Any]:
    """Get all sections.

    Args:
        document_id: Document UUID.

    Returns:
        List of sections.
    """
    _, handler = get_layout_handler(document_id)
    sections = handler.get_all_sections()

    return {
        "document_id": document_id,
        "count": len(sections),
        "sections": [
            {
                "index": s.index,
                "page_width": s.page_width,
                "page_height": s.page_height,
                "margin_top": s.margin_top,
                "margin_bottom": s.margin_bottom,
                "margin_left": s.margin_left,
                "margin_right": s.margin_right,
                "orientation": s.orientation,
            }
            for s in sections
        ],
    }


@router.get(
    "/sections/{index}",
    summary="Get Section",
    description="Get a specific section by index.",
)
async def get_section(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Get a section.

    Args:
        document_id: Document UUID.
        index: Section index.

    Returns:
        Section information.
    """
    _, handler = get_layout_handler(document_id)
    section = handler.get_section(index)

    return {
        "index": section.index,
        "page_width": section.page_width,
        "page_height": section.page_height,
        "margin_top": section.margin_top,
        "margin_bottom": section.margin_bottom,
        "margin_left": section.margin_left,
        "margin_right": section.margin_right,
        "orientation": section.orientation,
    }


@router.put(
    "/sections/{index}",
    summary="Update Section Layout",
    description="Update page layout for a section.",
)
async def update_section(
    document_id: str,
    index: int,
    layout: PageLayout,
) -> dict[str, Any]:
    """Update section layout.

    Args:
        document_id: Document UUID.
        index: Section index.
        layout: Layout settings.

    Returns:
        Updated section information.
    """
    doc_handler, handler = get_layout_handler(document_id)
    section = handler.set_page_layout(index, layout)
    doc_handler.save_document()

    return {
        "index": section.index,
        "updated": True,
    }


@router.post(
    "/sections",
    summary="Add Section",
    description="Add a new section to the document.",
)
async def add_section(
    document_id: str,
    start_type: str = "new_page",
) -> dict[str, Any]:
    """Add a section.

    Args:
        document_id: Document UUID.
        start_type: Section start type.

    Returns:
        Created section information.
    """
    doc_handler, handler = get_layout_handler(document_id)

    st = SectionStart.NEW_PAGE
    with contextlib.suppress(ValueError):
        st = SectionStart(start_type)

    index = handler.add_section(st)
    doc_handler.save_document()

    return {"index": index, "start_type": start_type}


@router.put(
    "/sections/{index}/margins",
    summary="Set Margins",
    description="Set page margins for a section.",
)
async def set_margins(
    document_id: str,
    index: int,
    top: float | None = None,
    bottom: float | None = None,
    left: float | None = None,
    right: float | None = None,
) -> dict[str, Any]:
    """Set page margins.

    Args:
        document_id: Document UUID.
        index: Section index.
        top: Top margin in inches.
        bottom: Bottom margin in inches.
        left: Left margin in inches.
        right: Right margin in inches.

    Returns:
        Updated section information.
    """
    doc_handler, handler = get_layout_handler(document_id)
    section = handler.set_margins(index, top, bottom, left, right)
    doc_handler.save_document()

    return {
        "index": section.index,
        "margin_top": section.margin_top,
        "margin_bottom": section.margin_bottom,
        "margin_left": section.margin_left,
        "margin_right": section.margin_right,
    }


@router.get(
    "/sections/{index}/header",
    summary="Get Header",
    description="Get header content for a section.",
)
async def get_header(
    document_id: str,
    index: int,
    header_type: str = "default",
) -> dict[str, Any]:
    """Get header content.

    Args:
        document_id: Document UUID.
        index: Section index.
        header_type: Header type.

    Returns:
        Header content.
    """
    _, handler = get_layout_handler(document_id)

    ht = HeaderFooterType.DEFAULT
    with contextlib.suppress(ValueError):
        ht = HeaderFooterType(header_type)

    content = handler.get_header(index, ht)

    return {
        "section_index": index,
        "header_type": header_type,
        "content": content,
    }


@router.put(
    "/sections/{index}/header",
    summary="Set Header",
    description="Set header content for a section.",
)
async def set_header(
    document_id: str,
    index: int,
    text: str,
    header_type: str = "default",
) -> dict[str, Any]:
    """Set header content.

    Args:
        document_id: Document UUID.
        index: Section index.
        text: Header text.
        header_type: Header type.

    Returns:
        Confirmation.
    """
    doc_handler, handler = get_layout_handler(document_id)

    ht = HeaderFooterType.DEFAULT
    with contextlib.suppress(ValueError):
        ht = HeaderFooterType(header_type)

    handler.set_header(text, index, ht)
    doc_handler.save_document()

    return {
        "section_index": index,
        "header_type": header_type,
        "updated": True,
    }


@router.get(
    "/sections/{index}/footer",
    summary="Get Footer",
    description="Get footer content for a section.",
)
async def get_footer(
    document_id: str,
    index: int,
    footer_type: str = "default",
) -> dict[str, Any]:
    """Get footer content.

    Args:
        document_id: Document UUID.
        index: Section index.
        footer_type: Footer type.

    Returns:
        Footer content.
    """
    _, handler = get_layout_handler(document_id)

    ft = HeaderFooterType.DEFAULT
    with contextlib.suppress(ValueError):
        ft = HeaderFooterType(footer_type)

    content = handler.get_footer(index, ft)

    return {
        "section_index": index,
        "footer_type": footer_type,
        "content": content,
    }


@router.put(
    "/sections/{index}/footer",
    summary="Set Footer",
    description="Set footer content for a section.",
)
async def set_footer(
    document_id: str,
    index: int,
    text: str,
    footer_type: str = "default",
) -> dict[str, Any]:
    """Set footer content.

    Args:
        document_id: Document UUID.
        index: Section index.
        text: Footer text.
        footer_type: Footer type.

    Returns:
        Confirmation.
    """
    doc_handler, handler = get_layout_handler(document_id)

    ft = HeaderFooterType.DEFAULT
    with contextlib.suppress(ValueError):
        ft = HeaderFooterType(footer_type)

    handler.set_footer(text, index, ft)
    doc_handler.save_document()

    return {
        "section_index": index,
        "footer_type": footer_type,
        "updated": True,
    }


@router.post(
    "/page-break",
    summary="Add Page Break",
    description="Add a page break to the document.",
)
async def add_page_break(document_id: str) -> dict[str, Any]:
    """Add a page break.

    Args:
        document_id: Document UUID.

    Returns:
        Confirmation.
    """
    doc_handler, handler = get_layout_handler(document_id)
    handler.add_page_break()
    doc_handler.save_document()

    return {"added": True, "type": "page_break"}
