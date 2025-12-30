"""MCP Resources definitions.

This module defines MCP resources for document access.
"""

from mcp.types import Resource


def register_resources() -> list[Resource]:
    """Register all MCP resources.

    Returns:
        List of Resource definitions.
    """
    resources = []

    # Document resource
    resources.append(
        Resource(
            uri="docx://current/document",
            name="Current Document",
            description="The currently open DOCX document",
            mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    )

    # Document content resource
    resources.append(
        Resource(
            uri="docx://current/content",
            name="Document Content",
            description="Full text content of the current document",
            mimeType="text/plain",
        )
    )

    # Document structure resource
    resources.append(
        Resource(
            uri="docx://current/structure",
            name="Document Structure",
            description="Structure information of the current document",
            mimeType="application/json",
        )
    )

    # Document metadata resource
    resources.append(
        Resource(
            uri="docx://current/metadata",
            name="Document Metadata",
            description="Metadata of the current document",
            mimeType="application/json",
        )
    )

    # Paragraphs resource
    resources.append(
        Resource(
            uri="docx://current/paragraphs",
            name="Document Paragraphs",
            description="All paragraphs in the current document",
            mimeType="application/json",
        )
    )

    # Tables resource
    resources.append(
        Resource(
            uri="docx://current/tables",
            name="Document Tables",
            description="All tables in the current document",
            mimeType="application/json",
        )
    )

    # Styles resource
    resources.append(
        Resource(
            uri="docx://current/styles",
            name="Document Styles",
            description="All styles in the current document",
            mimeType="application/json",
        )
    )

    # Headings resource
    resources.append(
        Resource(
            uri="docx://current/headings",
            name="Document Headings",
            description="All headings in the current document",
            mimeType="application/json",
        )
    )

    # Comments resource
    resources.append(
        Resource(
            uri="docx://current/comments",
            name="Document Comments",
            description="All comments in the current document",
            mimeType="application/json",
        )
    )

    # Bookmarks resource
    resources.append(
        Resource(
            uri="docx://current/bookmarks",
            name="Document Bookmarks",
            description="All bookmarks in the current document",
            mimeType="application/json",
        )
    )

    return resources
