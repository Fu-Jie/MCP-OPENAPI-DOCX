"""MCP Handlers for tool execution and resource reading.

This module implements the actual logic for MCP tool calls
and resource reading operations.
"""

import json
import os
from typing import Any

from src.core.config import get_settings
from src.handlers.document_handler import DocumentHandler
from src.handlers.text_handler import TextHandler
from src.handlers.table_handler import TableHandler
from src.handlers.list_handler import ListHandler
from src.handlers.media_handler import MediaHandler
from src.handlers.style_handler import StyleHandler
from src.handlers.layout_handler import LayoutHandler
from src.handlers.toc_handler import TocHandler
from src.handlers.comment_handler import CommentHandler


class MCPHandler:
    """Handler for MCP operations.

    This class manages the current document state and executes
    tool calls and resource reads.
    """

    def __init__(self) -> None:
        """Initialize the MCP handler."""
        self._doc_handler: DocumentHandler | None = None
        self._text_handler: TextHandler | None = None
        self._table_handler: TableHandler | None = None
        self._list_handler: ListHandler | None = None
        self._media_handler: MediaHandler | None = None
        self._style_handler: StyleHandler | None = None
        self._layout_handler: LayoutHandler | None = None
        self._toc_handler: TocHandler | None = None
        self._comment_handler: CommentHandler | None = None

    @property
    def doc_handler(self) -> DocumentHandler:
        """Get or create document handler."""
        if self._doc_handler is None:
            self._doc_handler = DocumentHandler()
        return self._doc_handler

    def _init_handlers(self) -> None:
        """Initialize all handlers with current document."""
        if self._doc_handler is None:
            return

        doc = self._doc_handler.document
        self._text_handler = TextHandler(doc)
        self._table_handler = TableHandler(doc)
        self._list_handler = ListHandler(doc)
        self._media_handler = MediaHandler(doc)
        self._style_handler = StyleHandler(doc)
        self._layout_handler = LayoutHandler(doc)
        self._toc_handler = TocHandler(doc)
        self._comment_handler = CommentHandler(doc)

    async def execute_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute an MCP tool.

        Args:
            name: Tool name.
            arguments: Tool arguments.

        Returns:
            Tool execution result.
        """
        # Document Management Tools
        if name == "create_document":
            self._doc_handler = DocumentHandler()
            self._doc_handler.create_document()
            if arguments.get("title"):
                self._doc_handler.set_metadata(title=arguments["title"])
            if arguments.get("author"):
                self._doc_handler.set_metadata(author=arguments["author"])
            self._init_handlers()
            return {"status": "created", "title": arguments.get("title")}

        elif name == "open_document":
            self._doc_handler = DocumentHandler()
            self._doc_handler.open_document(arguments["file_path"])
            self._init_handlers()
            return {"status": "opened", "path": arguments["file_path"]}

        elif name == "save_document":
            path = arguments.get("file_path")
            saved_path = self.doc_handler.save_document(path)
            return {"status": "saved", "path": saved_path}

        elif name == "close_document":
            if self._doc_handler:
                self._doc_handler.close()
                self._doc_handler = None
            return {"status": "closed"}

        elif name == "get_document_info":
            return {
                "paragraphs": self.doc_handler.get_paragraph_count(),
                "tables": self.doc_handler.get_table_count(),
                "sections": self.doc_handler.get_section_count(),
                "word_count": self.doc_handler.get_word_count(),
            }

        elif name == "get_document_structure":
            return self.doc_handler.get_document_structure()

        elif name == "get_document_metadata":
            meta = self.doc_handler.get_metadata()
            return {
                "author": meta.author,
                "title": meta.title,
                "subject": meta.subject,
                "keywords": meta.keywords,
            }

        elif name == "set_document_metadata":
            self.doc_handler.set_metadata(
                author=arguments.get("author"),
                title=arguments.get("title"),
                subject=arguments.get("subject"),
                keywords=arguments.get("keywords"),
            )
            return {"status": "updated"}

        elif name == "get_word_count":
            return {"word_count": self.doc_handler.get_word_count()}

        elif name == "get_character_count":
            include_spaces = arguments.get("include_spaces", True)
            return {"character_count": self.doc_handler.get_character_count(include_spaces)}

        # Paragraph Tools
        elif name == "get_paragraph":
            if self._text_handler is None:
                self._init_handlers()
            para = self._text_handler.get_paragraph(arguments["index"])
            return {"index": para.index, "text": para.text, "style": para.style}

        elif name == "get_all_paragraphs":
            if self._text_handler is None:
                self._init_handlers()
            paras = self._text_handler.get_all_paragraphs()
            return {"paragraphs": [{"index": p.index, "text": p.text} for p in paras]}

        elif name == "add_paragraph":
            if self._text_handler is None:
                self._init_handlers()
            index = self._text_handler.add_paragraph(
                text=arguments["text"],
                style=arguments.get("style"),
            )
            return {"index": index}

        elif name == "insert_paragraph":
            if self._text_handler is None:
                self._init_handlers()
            index = self._text_handler.insert_paragraph(
                index=arguments["index"],
                text=arguments["text"],
                style=arguments.get("style"),
            )
            return {"index": index}

        elif name == "update_paragraph":
            if self._text_handler is None:
                self._init_handlers()
            para = self._text_handler.update_paragraph(
                index=arguments["index"],
                text=arguments.get("text"),
                style=arguments.get("style"),
            )
            return {"index": para.index, "updated": True}

        elif name == "delete_paragraph":
            if self._text_handler is None:
                self._init_handlers()
            self._text_handler.delete_paragraph(arguments["index"])
            return {"deleted": True}

        elif name == "add_heading":
            if self._toc_handler is None:
                self._init_handlers()
            index = self._toc_handler.add_heading(
                text=arguments["text"],
                level=arguments.get("level", 1),
            )
            return {"index": index}

        elif name == "get_all_text":
            return {"text": self.doc_handler.get_all_text()}

        elif name == "find_text":
            if self._text_handler is None:
                self._init_handlers()
            results = self._text_handler.find_text(
                search_text=arguments["search_text"],
                case_sensitive=arguments.get("case_sensitive", False),
                whole_word=arguments.get("whole_word", False),
            )
            return {"results": results}

        elif name == "replace_text":
            if self._text_handler is None:
                self._init_handlers()
            count = self._text_handler.replace_text(
                find=arguments["find"],
                replace=arguments["replace"],
                case_sensitive=arguments.get("case_sensitive", False),
            )
            return {"replaced": count}

        # Table Tools
        elif name == "get_table":
            if self._table_handler is None:
                self._init_handlers()
            table = self._table_handler.get_table(arguments["index"])
            return {"index": table.index, "rows": table.rows, "cols": table.cols}

        elif name == "get_all_tables":
            if self._table_handler is None:
                self._init_handlers()
            tables = self._table_handler.get_all_tables()
            return {"tables": [{"index": t.index, "rows": t.rows, "cols": t.cols} for t in tables]}

        elif name == "add_table":
            if self._table_handler is None:
                self._init_handlers()
            index = self._table_handler.add_table(
                rows=arguments["rows"],
                cols=arguments["cols"],
                style=arguments.get("style"),
            )
            return {"index": index}

        elif name == "delete_table":
            if self._table_handler is None:
                self._init_handlers()
            self._table_handler.delete_table(arguments["index"])
            return {"deleted": True}

        elif name == "get_table_cell":
            if self._table_handler is None:
                self._init_handlers()
            cell = self._table_handler.get_cell(
                arguments["table_index"],
                arguments["row"],
                arguments["col"],
            )
            return {"text": cell.text}

        elif name == "set_table_cell":
            if self._table_handler is None:
                self._init_handlers()
            self._table_handler.set_cell(
                arguments["table_index"],
                arguments["row"],
                arguments["col"],
                arguments["text"],
            )
            return {"updated": True}

        elif name == "add_table_row":
            if self._table_handler is None:
                self._init_handlers()
            row_index = self._table_handler.add_row(arguments["table_index"])
            return {"row_index": row_index}

        elif name == "add_table_column":
            if self._table_handler is None:
                self._init_handlers()
            col_index = self._table_handler.add_column(arguments["table_index"])
            return {"col_index": col_index}

        elif name == "delete_table_row":
            if self._table_handler is None:
                self._init_handlers()
            self._table_handler.delete_row(
                arguments["table_index"],
                arguments["row_index"],
            )
            return {"deleted": True}

        elif name == "merge_table_cells":
            if self._table_handler is None:
                self._init_handlers()
            self._table_handler.merge_cells(
                arguments["table_index"],
                arguments["start_row"],
                arguments["start_col"],
                arguments["end_row"],
                arguments["end_col"],
            )
            return {"merged": True}

        elif name == "get_table_as_list":
            if self._table_handler is None:
                self._init_handlers()
            data = self._table_handler.get_table_as_list(arguments["table_index"])
            return {"data": data}

        # List Tools
        elif name == "create_bullet_list":
            if self._list_handler is None:
                self._init_handlers()
            index = self._list_handler.create_bullet_list(arguments["items"])
            return {"start_index": index}

        elif name == "create_numbered_list":
            if self._list_handler is None:
                self._init_handlers()
            index = self._list_handler.create_numbered_list(arguments["items"])
            return {"start_index": index}

        elif name == "add_list_item":
            if self._list_handler is None:
                self._init_handlers()
            from src.core.enums import ListType
            lt = ListType.BULLET if arguments.get("list_type") == "bullet" else ListType.NUMBERED
            index = self._list_handler.add_list_item(
                arguments["text"],
                lt,
                arguments.get("level", 0),
            )
            return {"index": index}

        # Layout Tools
        elif name == "get_section":
            if self._layout_handler is None:
                self._init_handlers()
            section = self._layout_handler.get_section(arguments.get("index", 0))
            return {
                "page_width": section.page_width,
                "page_height": section.page_height,
                "margins": {
                    "top": section.margin_top,
                    "bottom": section.margin_bottom,
                    "left": section.margin_left,
                    "right": section.margin_right,
                },
            }

        elif name == "set_page_margins":
            if self._layout_handler is None:
                self._init_handlers()
            self._layout_handler.set_margins(
                section_index=arguments.get("section_index", 0),
                top=arguments.get("top"),
                bottom=arguments.get("bottom"),
                left=arguments.get("left"),
                right=arguments.get("right"),
            )
            return {"updated": True}

        elif name == "set_header":
            if self._layout_handler is None:
                self._init_handlers()
            self._layout_handler.set_header(
                arguments["text"],
                arguments.get("section_index", 0),
            )
            return {"updated": True}

        elif name == "set_footer":
            if self._layout_handler is None:
                self._init_handlers()
            self._layout_handler.set_footer(
                arguments["text"],
                arguments.get("section_index", 0),
            )
            return {"updated": True}

        elif name == "add_page_break":
            if self._layout_handler is None:
                self._init_handlers()
            self._layout_handler.add_page_break()
            return {"added": True}

        # TOC and Navigation Tools
        elif name == "add_table_of_contents":
            if self._toc_handler is None:
                self._init_handlers()
            index = self._toc_handler.add_table_of_contents(
                title=arguments.get("title", "Table of Contents"),
                max_level=arguments.get("max_level", 3),
            )
            return {"index": index}

        elif name == "get_headings":
            if self._toc_handler is None:
                self._init_handlers()
            headings = self._toc_handler.get_headings()
            return {"headings": headings}

        elif name == "add_bookmark":
            if self._toc_handler is None:
                self._init_handlers()
            bookmark = self._toc_handler.add_bookmark(
                arguments["name"],
                arguments["paragraph_index"],
            )
            return {"name": bookmark.name}

        elif name == "get_bookmarks":
            if self._toc_handler is None:
                self._init_handlers()
            bookmarks = self._toc_handler.get_bookmarks()
            return {"bookmarks": [{"name": b.name, "paragraph_index": b.paragraph_index} for b in bookmarks]}

        elif name == "add_hyperlink":
            if self._toc_handler is None:
                self._init_handlers()
            hyperlink = self._toc_handler.add_hyperlink(
                arguments["text"],
                arguments["url"],
                arguments["paragraph_index"],
            )
            return {"text": hyperlink.text, "url": hyperlink.url}

        elif name == "get_hyperlinks":
            if self._toc_handler is None:
                self._init_handlers()
            hyperlinks = self._toc_handler.get_hyperlinks()
            return {"hyperlinks": [{"text": h.text, "url": h.url} for h in hyperlinks]}

        # Comment Tools
        elif name == "add_comment":
            if self._comment_handler is None:
                self._init_handlers()
            comment = self._comment_handler.add_comment(
                text=arguments["text"],
                author=arguments.get("author", "User"),
                paragraph_index=arguments["paragraph_index"],
            )
            return {"id": comment["id"]}

        elif name == "get_comments":
            if self._comment_handler is None:
                self._init_handlers()
            comments = self._comment_handler.get_all_comments()
            return {"comments": self._comment_handler.export_comments()}

        elif name == "resolve_comment":
            if self._comment_handler is None:
                self._init_handlers()
            self._comment_handler.resolve_comment(arguments["comment_id"])
            return {"resolved": True}

        elif name == "delete_comment":
            if self._comment_handler is None:
                self._init_handlers()
            self._comment_handler.delete_comment(arguments["comment_id"])
            return {"deleted": True}

        # Export Tools
        elif name == "export_to_html":
            paragraphs = self.doc_handler.document.paragraphs
            html_parts = ["<html><body>"]
            for para in paragraphs:
                html_parts.append(f"<p>{para.text}</p>")
            html_parts.append("</body></html>")
            return {"html": "\n".join(html_parts)}

        elif name == "export_to_markdown":
            paragraphs = self.doc_handler.document.paragraphs
            md_parts = []
            for para in paragraphs:
                md_parts.append(para.text)
                md_parts.append("")
            return {"markdown": "\n".join(md_parts)}

        elif name == "export_to_text":
            return {"text": self.doc_handler.get_all_text()}

        else:
            return {"error": f"Unknown tool: {name}"}

    async def read_resource(self, uri: str) -> str:
        """Read an MCP resource.

        Args:
            uri: Resource URI.

        Returns:
            Resource content as string.
        """
        if uri == "docx://current/content":
            return self.doc_handler.get_all_text()

        elif uri == "docx://current/structure":
            return json.dumps(self.doc_handler.get_document_structure())

        elif uri == "docx://current/metadata":
            meta = self.doc_handler.get_metadata()
            return json.dumps({
                "author": meta.author,
                "title": meta.title,
                "subject": meta.subject,
                "keywords": meta.keywords,
            })

        elif uri == "docx://current/paragraphs":
            if self._text_handler is None:
                self._init_handlers()
            paras = self._text_handler.get_all_paragraphs()
            return json.dumps([{"index": p.index, "text": p.text} for p in paras])

        elif uri == "docx://current/tables":
            if self._table_handler is None:
                self._init_handlers()
            tables = self._table_handler.get_all_tables()
            return json.dumps([{"index": t.index, "rows": t.rows, "cols": t.cols} for t in tables])

        elif uri == "docx://current/styles":
            if self._style_handler is None:
                self._init_handlers()
            styles = self._style_handler.get_all_styles()
            return json.dumps([{"name": s.name, "type": s.style_type} for s in styles])

        elif uri == "docx://current/headings":
            if self._toc_handler is None:
                self._init_handlers()
            headings = self._toc_handler.get_headings()
            return json.dumps(headings)

        elif uri == "docx://current/comments":
            if self._comment_handler is None:
                self._init_handlers()
            return json.dumps(self._comment_handler.export_comments())

        elif uri == "docx://current/bookmarks":
            if self._toc_handler is None:
                self._init_handlers()
            bookmarks = self._toc_handler.get_bookmarks()
            return json.dumps([{"name": b.name, "paragraph_index": b.paragraph_index} for b in bookmarks])

        else:
            return f"Unknown resource: {uri}"
