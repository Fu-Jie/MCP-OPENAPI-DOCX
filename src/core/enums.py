"""Enumeration types for the application.

This module contains all enum classes used throughout the application.
"""

from enum import Enum


class DocumentStatus(str, Enum):
    """Document lifecycle status.

    Attributes:
        DRAFT: Document is in draft state.
        PENDING_REVIEW: Document is pending review.
        APPROVED: Document has been approved.
        PUBLISHED: Document is published.
        ARCHIVED: Document is archived.
        DELETED: Document is soft-deleted.
    """

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


class DocumentFormat(str, Enum):
    """Supported document formats.

    Attributes:
        DOCX: Microsoft Word 2007+ format.
        DOC: Legacy Microsoft Word format.
        PDF: Portable Document Format.
        HTML: HyperText Markup Language.
        MARKDOWN: Markdown format.
        RTF: Rich Text Format.
        TXT: Plain text.
    """

    DOCX = "docx"
    DOC = "doc"
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    RTF = "rtf"
    TXT = "txt"


class ExportFormat(str, Enum):
    """Supported export formats.

    Attributes:
        PDF: Export to PDF format.
        HTML: Export to HTML format.
        MARKDOWN: Export to Markdown format.
        TXT: Export to plain text.
        RTF: Export to Rich Text Format.
    """

    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    TXT = "txt"
    RTF = "rtf"


class UserRole(str, Enum):
    """User role types.

    Attributes:
        ADMIN: Administrator with full access.
        EDITOR: Can edit documents.
        REVIEWER: Can review and comment.
        VIEWER: Read-only access.
        GUEST: Limited guest access.
    """

    ADMIN = "admin"
    EDITOR = "editor"
    REVIEWER = "reviewer"
    VIEWER = "viewer"
    GUEST = "guest"


class RevisionAction(str, Enum):
    """Types of revision actions.

    Attributes:
        INSERT: Text or content was inserted.
        DELETE: Text or content was deleted.
        FORMAT: Formatting was changed.
        MOVE: Content was moved.
        REPLACE: Content was replaced.
    """

    INSERT = "insert"
    DELETE = "delete"
    FORMAT = "format"
    MOVE = "move"
    REPLACE = "replace"


class CommentStatus(str, Enum):
    """Comment status types.

    Attributes:
        OPEN: Comment is open and active.
        RESOLVED: Comment has been resolved.
        DELETED: Comment is deleted.
    """

    OPEN = "open"
    RESOLVED = "resolved"
    DELETED = "deleted"


class ListType(str, Enum):
    """Types of lists.

    Attributes:
        BULLET: Bullet list.
        NUMBERED: Numbered list.
        MULTILEVEL: Multi-level list.
        CHECKLIST: Checklist.
    """

    BULLET = "bullet"
    NUMBERED = "numbered"
    MULTILEVEL = "multilevel"
    CHECKLIST = "checklist"


class NumberingFormat(str, Enum):
    """Numbering format types.

    Attributes:
        DECIMAL: Decimal numbers (1, 2, 3).
        LOWER_ALPHA: Lowercase letters (a, b, c).
        UPPER_ALPHA: Uppercase letters (A, B, C).
        LOWER_ROMAN: Lowercase Roman numerals (i, ii, iii).
        UPPER_ROMAN: Uppercase Roman numerals (I, II, III).
    """

    DECIMAL = "decimal"
    LOWER_ALPHA = "lowerLetter"
    UPPER_ALPHA = "upperLetter"
    LOWER_ROMAN = "lowerRoman"
    UPPER_ROMAN = "upperRoman"


class TextAlignment(str, Enum):
    """Text alignment options.

    Attributes:
        LEFT: Left-aligned text.
        CENTER: Center-aligned text.
        RIGHT: Right-aligned text.
        JUSTIFY: Justified text.
        DISTRIBUTE: Distributed text.
    """

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    DISTRIBUTE = "distribute"


class VerticalAlignment(str, Enum):
    """Vertical alignment options.

    Attributes:
        TOP: Top-aligned.
        CENTER: Center-aligned.
        BOTTOM: Bottom-aligned.
    """

    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class PageOrientation(str, Enum):
    """Page orientation options.

    Attributes:
        PORTRAIT: Portrait orientation.
        LANDSCAPE: Landscape orientation.
    """

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class PageSize(str, Enum):
    """Standard page sizes.

    Attributes:
        LETTER: US Letter (8.5 x 11 inches).
        A4: ISO A4 (210 x 297 mm).
        LEGAL: US Legal (8.5 x 14 inches).
        A3: ISO A3 (297 x 420 mm).
        CUSTOM: Custom page size.
    """

    LETTER = "letter"
    A4 = "a4"
    LEGAL = "legal"
    A3 = "a3"
    CUSTOM = "custom"


class HeaderFooterType(str, Enum):
    """Header/footer types.

    Attributes:
        DEFAULT: Default header/footer.
        FIRST: First page header/footer.
        EVEN: Even page header/footer.
        ODD: Odd page header/footer.
    """

    DEFAULT = "default"
    FIRST = "first"
    EVEN = "even"
    ODD = "odd"


class ImagePosition(str, Enum):
    """Image positioning options.

    Attributes:
        INLINE: Inline with text.
        FLOATING_LEFT: Floating left.
        FLOATING_RIGHT: Floating right.
        CENTERED: Centered.
        BEHIND_TEXT: Behind text.
        IN_FRONT: In front of text.
    """

    INLINE = "inline"
    FLOATING_LEFT = "floating_left"
    FLOATING_RIGHT = "floating_right"
    CENTERED = "centered"
    BEHIND_TEXT = "behind_text"
    IN_FRONT = "in_front"


class TableBorderStyle(str, Enum):
    """Table border styles.

    Attributes:
        NONE: No border.
        SINGLE: Single line border.
        THICK: Thick line border.
        DOUBLE: Double line border.
        DOTTED: Dotted border.
        DASHED: Dashed border.
    """

    NONE = "none"
    SINGLE = "single"
    THICK = "thick"
    DOUBLE = "double"
    DOTTED = "dotted"
    DASHED = "dashed"


class TaskStatus(str, Enum):
    """Async task status.

    Attributes:
        PENDING: Task is pending.
        RUNNING: Task is running.
        COMPLETED: Task completed successfully.
        FAILED: Task failed.
        CANCELLED: Task was cancelled.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AuditAction(str, Enum):
    """Audit log action types.

    Attributes:
        CREATE: Resource created.
        READ: Resource read.
        UPDATE: Resource updated.
        DELETE: Resource deleted.
        EXPORT: Resource exported.
        IMPORT: Resource imported.
        SHARE: Resource shared.
        LOGIN: User logged in.
        LOGOUT: User logged out.
    """

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    SHARE = "share"
    LOGIN = "login"
    LOGOUT = "logout"


class NotificationType(str, Enum):
    """Notification types.

    Attributes:
        DOCUMENT_SHARED: Document was shared.
        COMMENT_ADDED: Comment was added.
        DOCUMENT_UPDATED: Document was updated.
        TASK_COMPLETED: Task completed.
        MENTION: User was mentioned.
    """

    DOCUMENT_SHARED = "document_shared"
    COMMENT_ADDED = "comment_added"
    DOCUMENT_UPDATED = "document_updated"
    TASK_COMPLETED = "task_completed"
    MENTION = "mention"


class StyleType(str, Enum):
    """Style types in DOCX.

    Attributes:
        PARAGRAPH: Paragraph style.
        CHARACTER: Character style.
        TABLE: Table style.
        NUMBERING: Numbering/list style.
    """

    PARAGRAPH = "paragraph"
    CHARACTER = "character"
    TABLE = "table"
    NUMBERING = "numbering"


class BreakType(str, Enum):
    """Break types in documents.

    Attributes:
        PAGE: Page break.
        SECTION: Section break.
        COLUMN: Column break.
        LINE: Line break.
    """

    PAGE = "page"
    SECTION = "section"
    COLUMN = "column"
    LINE = "line"


class SectionStart(str, Enum):
    """Section start types.

    Attributes:
        CONTINUOUS: Continuous section.
        NEW_PAGE: New page section.
        EVEN_PAGE: Even page section.
        ODD_PAGE: Odd page section.
        NEW_COLUMN: New column section.
    """

    CONTINUOUS = "continuous"
    NEW_PAGE = "newPage"
    EVEN_PAGE = "evenPage"
    ODD_PAGE = "oddPage"
    NEW_COLUMN = "newColumn"
