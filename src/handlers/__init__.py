"""Handlers package for document processing."""

from src.handlers.document_handler import DocumentHandler
from src.handlers.text_handler import TextHandler
from src.handlers.table_handler import TableHandler
from src.handlers.list_handler import ListHandler
from src.handlers.media_handler import MediaHandler
from src.handlers.style_handler import StyleHandler
from src.handlers.layout_handler import LayoutHandler
from src.handlers.toc_handler import TocHandler
from src.handlers.comment_handler import CommentHandler
from src.handlers.revision_handler import RevisionHandler

__all__ = [
    "DocumentHandler",
    "TextHandler",
    "TableHandler",
    "ListHandler",
    "MediaHandler",
    "StyleHandler",
    "LayoutHandler",
    "TocHandler",
    "CommentHandler",
    "RevisionHandler",
]
