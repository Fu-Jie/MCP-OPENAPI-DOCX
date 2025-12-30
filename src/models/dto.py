"""Data Transfer Objects for internal data conversion.

This module defines DTOs used for internal data transformations
and service layer communication.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.core.enums import (
    CommentStatus,
    DocumentStatus,
    ExportFormat,
    ListType,
    RevisionAction,
    TextAlignment,
    UserRole,
)


@dataclass
class UserDTO:
    """Data transfer object for user data.

    Attributes:
        id: User ID.
        uuid: User UUID.
        email: User email.
        username: Username.
        role: User role.
        is_active: Whether user is active.
        is_verified: Whether email is verified.
        created_at: Creation timestamp.
    """

    id: int
    uuid: str
    email: str
    username: str
    role: UserRole
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime | None = None


@dataclass
class DocumentDTO:
    """Data transfer object for document data.

    Attributes:
        id: Document ID.
        uuid: Document UUID.
        title: Document title.
        description: Document description.
        file_path: Path to the file.
        file_size: File size in bytes.
        mime_type: File MIME type.
        status: Document status.
        version: Current version number.
        metadata: Document metadata.
        owner_id: Owner user ID.
        created_at: Creation timestamp.
        updated_at: Update timestamp.
    """

    id: int
    uuid: str
    title: str
    file_path: str
    file_size: int
    mime_type: str
    status: DocumentStatus
    version: int
    owner_id: int
    description: str | None = None
    metadata: dict[str, Any] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class ParagraphDTO:
    """Data transfer object for paragraph data.

    Attributes:
        index: Paragraph index in document.
        text: Paragraph text content.
        style: Paragraph style name.
        alignment: Text alignment.
        runs: List of text runs in paragraph.
    """

    index: int
    text: str
    style: str | None = None
    alignment: TextAlignment | None = None
    runs: list["RunDTO"] = field(default_factory=list)


@dataclass
class RunDTO:
    """Data transfer object for text run data.

    Attributes:
        text: Run text content.
        bold: Whether text is bold.
        italic: Whether text is italic.
        underline: Whether text is underlined.
        font_name: Font name.
        font_size: Font size in points.
        color: Text color (hex).
    """

    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_name: str | None = None
    font_size: int | None = None
    color: str | None = None


@dataclass
class TableDTO:
    """Data transfer object for table data.

    Attributes:
        index: Table index in document.
        rows: Number of rows.
        cols: Number of columns.
        cells: Table cell data.
        style: Table style name.
    """

    index: int
    rows: int
    cols: int
    cells: list[list["CellDTO"]] = field(default_factory=list)
    style: str | None = None


@dataclass
class CellDTO:
    """Data transfer object for table cell data.

    Attributes:
        row: Row index.
        col: Column index.
        text: Cell text content.
        colspan: Column span.
        rowspan: Row span.
    """

    row: int
    col: int
    text: str = ""
    colspan: int = 1
    rowspan: int = 1


@dataclass
class ImageDTO:
    """Data transfer object for image data.

    Attributes:
        index: Image index in document.
        paragraph_index: Paragraph containing the image.
        filename: Original filename.
        width: Image width in inches.
        height: Image height in inches.
        alt_text: Alternative text.
        content_type: Image content type.
    """

    index: int
    paragraph_index: int
    filename: str
    width: float | None = None
    height: float | None = None
    alt_text: str | None = None
    content_type: str | None = None


@dataclass
class StyleDTO:
    """Data transfer object for style data.

    Attributes:
        name: Style name.
        style_type: Style type (paragraph, character, etc.).
        base_style: Base style name.
        font_name: Font name.
        font_size: Font size in points.
        bold: Whether text is bold.
        italic: Whether text is italic.
        color: Text color (hex).
        alignment: Text alignment.
    """

    name: str
    style_type: str
    base_style: str | None = None
    font_name: str | None = None
    font_size: int | None = None
    bold: bool | None = None
    italic: bool | None = None
    color: str | None = None
    alignment: TextAlignment | None = None


@dataclass
class SectionDTO:
    """Data transfer object for section data.

    Attributes:
        index: Section index.
        start_type: Section start type.
        page_width: Page width in inches.
        page_height: Page height in inches.
        margin_top: Top margin in inches.
        margin_bottom: Bottom margin in inches.
        margin_left: Left margin in inches.
        margin_right: Right margin in inches.
        orientation: Page orientation.
    """

    index: int
    start_type: str | None = None
    page_width: float | None = None
    page_height: float | None = None
    margin_top: float | None = None
    margin_bottom: float | None = None
    margin_left: float | None = None
    margin_right: float | None = None
    orientation: str | None = None


@dataclass
class CommentDTO:
    """Data transfer object for comment data.

    Attributes:
        id: Comment ID.
        uuid: Comment UUID.
        document_id: Document ID.
        author_id: Author user ID.
        content: Comment content.
        status: Comment status.
        paragraph_index: Paragraph index.
        start_offset: Start character offset.
        end_offset: End character offset.
        parent_id: Parent comment ID for replies.
        created_at: Creation timestamp.
    """

    id: int
    uuid: str
    document_id: int
    author_id: int
    content: str
    status: CommentStatus
    paragraph_index: int | None = None
    start_offset: int | None = None
    end_offset: int | None = None
    parent_id: int | None = None
    created_at: datetime | None = None


@dataclass
class RevisionDTO:
    """Data transfer object for revision data.

    Attributes:
        id: Revision ID.
        uuid: Revision UUID.
        document_id: Document ID.
        author_id: Author user ID.
        action: Revision action type.
        paragraph_index: Paragraph index.
        original_content: Original content.
        new_content: New content.
        is_accepted: Whether revision is accepted.
        created_at: Creation timestamp.
    """

    id: int
    uuid: str
    document_id: int
    author_id: int
    action: RevisionAction
    paragraph_index: int | None = None
    original_content: str | None = None
    new_content: str | None = None
    is_accepted: bool = False
    created_at: datetime | None = None


@dataclass
class SearchResultDTO:
    """Data transfer object for search results.

    Attributes:
        paragraph_index: Paragraph index where match was found.
        text: Matched text.
        start_offset: Start character offset.
        end_offset: End character offset.
        context: Surrounding context text.
    """

    paragraph_index: int
    text: str
    start_offset: int
    end_offset: int
    context: str = ""


@dataclass
class ExportTaskDTO:
    """Data transfer object for export task.

    Attributes:
        task_id: Task ID.
        document_id: Document ID.
        format: Export format.
        status: Task status.
        output_path: Output file path.
        error: Error message if failed.
        created_at: Task creation timestamp.
        completed_at: Task completion timestamp.
    """

    task_id: str
    document_id: int
    format: ExportFormat
    status: str
    output_path: str | None = None
    error: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class DocumentMetadataDTO:
    """Data transfer object for document metadata.

    Attributes:
        author: Document author.
        title: Document title.
        subject: Document subject.
        keywords: Document keywords.
        comments: Document comments/description.
        category: Document category.
        created: Creation timestamp.
        modified: Modification timestamp.
        last_modified_by: Last modifier.
        revision: Revision number.
    """

    author: str | None = None
    title: str | None = None
    subject: str | None = None
    keywords: str | None = None
    comments: str | None = None
    category: str | None = None
    created: datetime | None = None
    modified: datetime | None = None
    last_modified_by: str | None = None
    revision: int | None = None


@dataclass
class ListItemDTO:
    """Data transfer object for list item.

    Attributes:
        index: Item index in list.
        text: Item text.
        level: Indentation level.
    """

    index: int
    text: str
    level: int = 0


@dataclass
class ListDTO:
    """Data transfer object for list.

    Attributes:
        paragraph_index: Starting paragraph index.
        list_type: Type of list.
        items: List items.
    """

    paragraph_index: int
    list_type: ListType
    items: list[ListItemDTO] = field(default_factory=list)


@dataclass
class BookmarkDTO:
    """Data transfer object for bookmark.

    Attributes:
        name: Bookmark name.
        paragraph_index: Paragraph index.
    """

    name: str
    paragraph_index: int


@dataclass
class HyperlinkDTO:
    """Data transfer object for hyperlink.

    Attributes:
        text: Link text.
        url: Link URL.
        paragraph_index: Paragraph index.
        start_offset: Start character offset.
        end_offset: End character offset.
    """

    text: str
    url: str
    paragraph_index: int
    start_offset: int | None = None
    end_offset: int | None = None
