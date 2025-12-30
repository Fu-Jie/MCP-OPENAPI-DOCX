"""Pydantic schemas for API request/response validation.

This module defines all Pydantic models used for data validation
and serialization in the API.
"""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.core.enums import (
    CommentStatus,
    DocumentStatus,
    ExportFormat,
    ListType,
    NumberingFormat,
    PageOrientation,
    PageSize,
    RevisionAction,
    TextAlignment,
    UserRole,
)

# =============================================================================
# Base Schemas
# =============================================================================


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema.

    Attributes:
        items: List of items in the current page.
        total: Total number of items.
        page: Current page number.
        size: Number of items per page.
        pages: Total number of pages.
    """

    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseModel):
    """Standard success response schema."""

    success: bool = True
    message: str = "Operation completed successfully"
    data: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    success: bool = False
    error: dict[str, Any]


# =============================================================================
# User Schemas
# =============================================================================


class UserBase(BaseSchema):
    """Base user schema with common fields."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = Field(default=UserRole.VIEWER)


class UserUpdate(BaseSchema):
    """Schema for updating a user."""

    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=100)
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    uuid: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# =============================================================================
# Document Schemas
# =============================================================================


class DocumentBase(BaseSchema):
    """Base document schema with common fields."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)


class DocumentCreate(DocumentBase):
    """Schema for creating a new document."""

    metadata: dict[str, Any] | None = None


class DocumentUpdate(BaseSchema):
    """Schema for updating a document."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: DocumentStatus | None = None
    metadata: dict[str, Any] | None = None


class DocumentResponse(DocumentBase):
    """Schema for document response."""

    uuid: str
    file_size: int
    mime_type: str
    status: DocumentStatus
    version: int
    metadata: dict[str, Any] | None
    owner_id: int
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseSchema):
    """Schema for document list item."""

    uuid: str
    title: str
    status: DocumentStatus
    version: int
    file_size: int
    created_at: datetime
    updated_at: datetime


# =============================================================================
# Document Version Schemas
# =============================================================================


class DocumentVersionResponse(BaseSchema):
    """Schema for document version response."""

    id: int
    version_number: int
    file_size: int
    change_summary: str | None
    created_at: datetime


# =============================================================================
# Comment Schemas
# =============================================================================


class CommentBase(BaseSchema):
    """Base comment schema."""

    content: str = Field(..., min_length=1, max_length=5000)


class CommentCreate(CommentBase):
    """Schema for creating a comment."""

    paragraph_index: int | None = None
    start_offset: int | None = None
    end_offset: int | None = None
    parent_id: int | None = None


class CommentUpdate(BaseSchema):
    """Schema for updating a comment."""

    content: str | None = Field(default=None, min_length=1, max_length=5000)
    status: CommentStatus | None = None


class CommentResponse(CommentBase):
    """Schema for comment response."""

    uuid: str
    author_id: int
    status: CommentStatus
    paragraph_index: int | None
    start_offset: int | None
    end_offset: int | None
    parent_id: int | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None


# =============================================================================
# Revision Schemas
# =============================================================================


class RevisionCreate(BaseSchema):
    """Schema for creating a revision."""

    action: RevisionAction
    paragraph_index: int | None = None
    original_content: str | None = None
    new_content: str | None = None


class RevisionResponse(BaseSchema):
    """Schema for revision response."""

    uuid: str
    author_id: int
    action: RevisionAction
    paragraph_index: int | None
    original_content: str | None
    new_content: str | None
    is_accepted: bool
    created_at: datetime
    accepted_at: datetime | None


class RevisionAccept(BaseSchema):
    """Schema for accepting/rejecting a revision."""

    accept: bool


# =============================================================================
# Template Schemas
# =============================================================================


class TemplateBase(BaseSchema):
    """Base template schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, max_length=100)


class TemplateCreate(TemplateBase):
    """Schema for creating a template."""

    is_public: bool = True
    metadata: dict[str, Any] | None = None


class TemplateUpdate(BaseSchema):
    """Schema for updating a template."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, max_length=100)
    is_public: bool | None = None


class TemplateResponse(TemplateBase):
    """Schema for template response."""

    uuid: str
    is_public: bool
    metadata: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime


# =============================================================================
# Text Editing Schemas
# =============================================================================


class ParagraphCreate(BaseSchema):
    """Schema for creating a paragraph."""

    text: str
    style: str | None = Field(default=None, description="Paragraph style name")
    alignment: TextAlignment | None = None


class ParagraphUpdate(BaseSchema):
    """Schema for updating a paragraph."""

    text: str | None = None
    style: str | None = None
    alignment: TextAlignment | None = None


class TextFormat(BaseSchema):
    """Schema for text formatting options."""

    bold: bool | None = None
    italic: bool | None = None
    underline: bool | None = None
    strike: bool | None = None
    font_name: str | None = None
    font_size: int | None = Field(default=None, ge=6, le=144)
    color: str | None = Field(default=None, pattern=r"^[0-9A-Fa-f]{6}$")
    highlight_color: str | None = None
    superscript: bool | None = None
    subscript: bool | None = None


class TextInsert(BaseSchema):
    """Schema for inserting text."""

    text: str
    paragraph_index: int = Field(..., ge=0)
    offset: int | None = Field(default=None, ge=0)
    format: TextFormat | None = None


class TextReplace(BaseSchema):
    """Schema for replacing text."""

    find: str = Field(..., min_length=1)
    replace: str
    case_sensitive: bool = True
    whole_word: bool = False
    use_regex: bool = False


# =============================================================================
# Table Schemas
# =============================================================================


class TableCell(BaseSchema):
    """Schema for a table cell."""

    text: str = ""
    colspan: int = Field(default=1, ge=1)
    rowspan: int = Field(default=1, ge=1)


class TableRow(BaseSchema):
    """Schema for a table row."""

    cells: list[TableCell]


class TableCreate(BaseSchema):
    """Schema for creating a table."""

    rows: int = Field(..., ge=1, le=100)
    cols: int = Field(..., ge=1, le=63)
    data: list[TableRow] | None = None
    style: str | None = None
    paragraph_index: int | None = Field(default=None, ge=0)


class TableUpdate(BaseSchema):
    """Schema for updating a table."""

    data: list[TableRow] | None = None
    style: str | None = None


class TableCellUpdate(BaseSchema):
    """Schema for updating a table cell."""

    table_index: int = Field(..., ge=0)
    row: int = Field(..., ge=0)
    col: int = Field(..., ge=0)
    text: str | None = None
    merge_right: int | None = Field(default=None, ge=0)
    merge_down: int | None = Field(default=None, ge=0)


# =============================================================================
# List Schemas
# =============================================================================


class ListItemCreate(BaseSchema):
    """Schema for creating a list item."""

    text: str
    level: int = Field(default=0, ge=0, le=8)


class ListCreate(BaseSchema):
    """Schema for creating a list."""

    list_type: ListType
    items: list[ListItemCreate]
    numbering_format: NumberingFormat | None = None
    paragraph_index: int | None = Field(default=None, ge=0)


# =============================================================================
# Media Schemas
# =============================================================================


class ImageInsert(BaseSchema):
    """Schema for inserting an image."""

    paragraph_index: int = Field(..., ge=0)
    width: float | None = Field(default=None, ge=0.1, le=20)
    height: float | None = Field(default=None, ge=0.1, le=20)
    alt_text: str | None = None


class ImageUpdate(BaseSchema):
    """Schema for updating an image."""

    width: float | None = Field(default=None, ge=0.1, le=20)
    height: float | None = Field(default=None, ge=0.1, le=20)
    alt_text: str | None = None


# =============================================================================
# Style Schemas
# =============================================================================


class StyleCreate(BaseSchema):
    """Schema for creating a style."""

    name: str = Field(..., min_length=1, max_length=100)
    base_style: str | None = None
    font_name: str | None = None
    font_size: int | None = Field(default=None, ge=6, le=144)
    bold: bool | None = None
    italic: bool | None = None
    color: str | None = Field(default=None, pattern=r"^[0-9A-Fa-f]{6}$")
    alignment: TextAlignment | None = None
    line_spacing: float | None = Field(default=None, ge=0.5, le=10)
    space_before: float | None = Field(default=None, ge=0)
    space_after: float | None = Field(default=None, ge=0)


class StyleResponse(BaseSchema):
    """Schema for style response."""

    name: str
    style_type: str
    base_style: str | None
    font_name: str | None
    font_size: int | None
    bold: bool | None
    italic: bool | None


# =============================================================================
# Layout Schemas
# =============================================================================


class PageLayout(BaseSchema):
    """Schema for page layout settings."""

    page_size: PageSize | None = None
    orientation: PageOrientation | None = None
    margin_top: float | None = Field(default=None, ge=0, le=10)
    margin_bottom: float | None = Field(default=None, ge=0, le=10)
    margin_left: float | None = Field(default=None, ge=0, le=10)
    margin_right: float | None = Field(default=None, ge=0, le=10)
    width: float | None = Field(default=None, ge=1, le=50)
    height: float | None = Field(default=None, ge=1, le=50)


class HeaderFooterContent(BaseSchema):
    """Schema for header/footer content."""

    text: str
    alignment: TextAlignment = TextAlignment.CENTER
    font_size: int | None = Field(default=None, ge=6, le=72)


# =============================================================================
# TOC and Navigation Schemas
# =============================================================================


class TocCreate(BaseSchema):
    """Schema for creating a table of contents."""

    title: str = "Table of Contents"
    max_level: int = Field(default=3, ge=1, le=9)
    paragraph_index: int | None = Field(default=None, ge=0)


class BookmarkCreate(BaseSchema):
    """Schema for creating a bookmark."""

    name: str = Field(..., min_length=1, max_length=100)
    paragraph_index: int = Field(..., ge=0)


class HyperlinkCreate(BaseSchema):
    """Schema for creating a hyperlink."""

    text: str
    url: str
    paragraph_index: int = Field(..., ge=0)
    offset: int | None = Field(default=None, ge=0)


# =============================================================================
# Search Schemas
# =============================================================================


class SearchQuery(BaseSchema):
    """Schema for search queries."""

    query: str = Field(..., min_length=1)
    case_sensitive: bool = False
    whole_word: bool = False
    use_regex: bool = False


class SearchResult(BaseSchema):
    """Schema for search results."""

    paragraph_index: int
    text: str
    start_offset: int
    end_offset: int
    context: str


# =============================================================================
# Export Schemas
# =============================================================================


class ExportRequest(BaseSchema):
    """Schema for export requests."""

    format: ExportFormat
    include_comments: bool = False
    include_revisions: bool = False


class ExportResponse(BaseSchema):
    """Schema for export response."""

    task_id: str
    status: str
    download_url: str | None = None


# =============================================================================
# Batch Operation Schemas
# =============================================================================


class BatchOperation(BaseSchema):
    """Schema for a single batch operation."""

    operation: str
    params: dict[str, Any]


class BatchRequest(BaseSchema):
    """Schema for batch operation requests."""

    operations: list[BatchOperation]
    stop_on_error: bool = False


class BatchResult(BaseSchema):
    """Schema for batch operation results."""

    success: bool
    results: list[dict[str, Any]]
    errors: list[dict[str, Any]]


# =============================================================================
# Filter and Query Schemas
# =============================================================================


class DocumentFilter(BaseSchema):
    """Schema for document filtering."""

    status: DocumentStatus | None = None
    owner_id: int | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    search: str | None = None


class PaginationParams(BaseSchema):
    """Schema for pagination parameters."""

    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    sort_by: str | None = None
    sort_order: str = Field(default="desc", pattern=r"^(asc|desc)$")


# =============================================================================
# Health Check Schemas
# =============================================================================


class HealthStatus(BaseSchema):
    """Schema for health check response."""

    status: str
    version: str
    database: str
    redis: str
    uptime: float
