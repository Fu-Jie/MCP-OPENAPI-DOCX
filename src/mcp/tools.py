"""MCP Tools definitions.

This module defines all MCP tools for document operations.
Following MCP protocol specifications.
"""

from mcp.types import Tool


def register_tools() -> list[Tool]:
    """Register all MCP tools.

    Returns:
        List of Tool definitions for the MCP server.
    """
    tools = []

    # ==========================================================================
    # Document Management Tools (1-10)
    # ==========================================================================
    tools.append(
        Tool(
            name="create_document",
            description="Create a new empty DOCX document",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Document title"},
                    "author": {"type": "string", "description": "Document author"},
                },
                "required": ["title"],
            },
        )
    )

    tools.append(
        Tool(
            name="open_document",
            description="Open an existing DOCX document",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the DOCX file",
                    },
                },
                "required": ["file_path"],
            },
        )
    )

    tools.append(
        Tool(
            name="save_document",
            description="Save the current document",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to save the document",
                    },
                },
            },
        )
    )

    tools.append(
        Tool(
            name="close_document",
            description="Close the current document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="get_document_info",
            description="Get information about the current document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="get_document_structure",
            description="Get the structure of the document (paragraphs, tables, etc.)",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="get_document_metadata",
            description="Get document metadata (author, title, etc.)",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="set_document_metadata",
            description="Set document metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "author": {"type": "string", "description": "Document author"},
                    "title": {"type": "string", "description": "Document title"},
                    "subject": {"type": "string", "description": "Document subject"},
                    "keywords": {"type": "string", "description": "Document keywords"},
                },
            },
        )
    )

    tools.append(
        Tool(
            name="get_word_count",
            description="Get the word count of the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="get_character_count",
            description="Get the character count of the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_spaces": {"type": "boolean", "default": True},
                },
            },
        )
    )

    # ==========================================================================
    # Paragraph Tools (11-25)
    # ==========================================================================
    tools.append(
        Tool(
            name="get_paragraph",
            description="Get a paragraph by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Paragraph index"},
                },
                "required": ["index"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_all_paragraphs",
            description="Get all paragraphs in the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="add_paragraph",
            description="Add a new paragraph to the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Paragraph text"},
                    "style": {"type": "string", "description": "Paragraph style"},
                },
                "required": ["text"],
            },
        )
    )

    tools.append(
        Tool(
            name="insert_paragraph",
            description="Insert a paragraph at a specific index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Index to insert at"},
                    "text": {"type": "string", "description": "Paragraph text"},
                    "style": {"type": "string", "description": "Paragraph style"},
                },
                "required": ["index", "text"],
            },
        )
    )

    tools.append(
        Tool(
            name="update_paragraph",
            description="Update an existing paragraph",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Paragraph index"},
                    "text": {"type": "string", "description": "New text"},
                    "style": {"type": "string", "description": "New style"},
                },
                "required": ["index"],
            },
        )
    )

    tools.append(
        Tool(
            name="delete_paragraph",
            description="Delete a paragraph by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Paragraph index"},
                },
                "required": ["index"],
            },
        )
    )

    tools.append(
        Tool(
            name="add_heading",
            description="Add a heading to the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Heading text"},
                    "level": {
                        "type": "integer",
                        "description": "Heading level (1-9)",
                        "default": 1,
                    },
                },
                "required": ["text"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_all_text",
            description="Get all text content from the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="find_text",
            description="Find text in the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_text": {
                        "type": "string",
                        "description": "Text to search for",
                    },
                    "case_sensitive": {"type": "boolean", "default": False},
                    "whole_word": {"type": "boolean", "default": False},
                },
                "required": ["search_text"],
            },
        )
    )

    tools.append(
        Tool(
            name="replace_text",
            description="Find and replace text in the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "find": {"type": "string", "description": "Text to find"},
                    "replace": {"type": "string", "description": "Replacement text"},
                    "case_sensitive": {"type": "boolean", "default": False},
                },
                "required": ["find", "replace"],
            },
        )
    )

    tools.append(
        Tool(
            name="insert_text",
            description="Insert text at a specific position",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "offset": {"type": "integer"},
                    "text": {"type": "string"},
                },
                "required": ["paragraph_index", "text"],
            },
        )
    )

    # ==========================================================================
    # Formatting Tools (26-40)
    # ==========================================================================
    tools.append(
        Tool(
            name="format_text_bold",
            description="Apply bold formatting to text",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "run_index": {"type": "integer"},
                    "bold": {"type": "boolean", "default": True},
                },
                "required": ["paragraph_index", "run_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="format_text_italic",
            description="Apply italic formatting to text",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "run_index": {"type": "integer"},
                    "italic": {"type": "boolean", "default": True},
                },
                "required": ["paragraph_index", "run_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="format_text_underline",
            description="Apply underline formatting to text",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "run_index": {"type": "integer"},
                    "underline": {"type": "boolean", "default": True},
                },
                "required": ["paragraph_index", "run_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="set_font",
            description="Set font properties for text",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "run_index": {"type": "integer"},
                    "font_name": {"type": "string"},
                    "font_size": {"type": "integer"},
                },
                "required": ["paragraph_index", "run_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="set_text_color",
            description="Set text color",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "run_index": {"type": "integer"},
                    "color": {
                        "type": "string",
                        "description": "Hex color code (e.g., 'FF0000')",
                    },
                },
                "required": ["paragraph_index", "run_index", "color"],
            },
        )
    )

    tools.append(
        Tool(
            name="set_paragraph_alignment",
            description="Set paragraph alignment",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "alignment": {
                        "type": "string",
                        "enum": ["left", "center", "right", "justify"],
                    },
                },
                "required": ["paragraph_index", "alignment"],
            },
        )
    )

    tools.append(
        Tool(
            name="apply_style",
            description="Apply a style to a paragraph",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                    "style_name": {"type": "string"},
                },
                "required": ["paragraph_index", "style_name"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_styles",
            description="Get all available styles in the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="create_style",
            description="Create a new custom style",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "font_name": {"type": "string"},
                    "font_size": {"type": "integer"},
                    "bold": {"type": "boolean"},
                    "italic": {"type": "boolean"},
                },
                "required": ["name"],
            },
        )
    )

    # ==========================================================================
    # Table Tools (41-55)
    # ==========================================================================
    tools.append(
        Tool(
            name="get_table",
            description="Get a table by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                },
                "required": ["index"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_all_tables",
            description="Get all tables in the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="add_table",
            description="Add a new table to the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "rows": {"type": "integer", "description": "Number of rows"},
                    "cols": {"type": "integer", "description": "Number of columns"},
                    "style": {"type": "string", "description": "Table style"},
                },
                "required": ["rows", "cols"],
            },
        )
    )

    tools.append(
        Tool(
            name="delete_table",
            description="Delete a table by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                },
                "required": ["index"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_table_cell",
            description="Get content of a table cell",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                    "row": {"type": "integer"},
                    "col": {"type": "integer"},
                },
                "required": ["table_index", "row", "col"],
            },
        )
    )

    tools.append(
        Tool(
            name="set_table_cell",
            description="Set content of a table cell",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                    "row": {"type": "integer"},
                    "col": {"type": "integer"},
                    "text": {"type": "string"},
                },
                "required": ["table_index", "row", "col", "text"],
            },
        )
    )

    tools.append(
        Tool(
            name="add_table_row",
            description="Add a row to a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                },
                "required": ["table_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="add_table_column",
            description="Add a column to a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                },
                "required": ["table_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="delete_table_row",
            description="Delete a row from a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                    "row_index": {"type": "integer"},
                },
                "required": ["table_index", "row_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="merge_table_cells",
            description="Merge table cells",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                    "start_row": {"type": "integer"},
                    "start_col": {"type": "integer"},
                    "end_row": {"type": "integer"},
                    "end_col": {"type": "integer"},
                },
                "required": [
                    "table_index",
                    "start_row",
                    "start_col",
                    "end_row",
                    "end_col",
                ],
            },
        )
    )

    tools.append(
        Tool(
            name="set_table_style",
            description="Set table style",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                    "style": {"type": "string"},
                },
                "required": ["table_index", "style"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_table_as_list",
            description="Get table content as a 2D list",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_index": {"type": "integer"},
                },
                "required": ["table_index"],
            },
        )
    )

    # ==========================================================================
    # List Tools (56-62)
    # ==========================================================================
    tools.append(
        Tool(
            name="create_bullet_list",
            description="Create a bullet list",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["items"],
            },
        )
    )

    tools.append(
        Tool(
            name="create_numbered_list",
            description="Create a numbered list",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["items"],
            },
        )
    )

    tools.append(
        Tool(
            name="add_list_item",
            description="Add an item to a list",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "list_type": {"type": "string", "enum": ["bullet", "numbered"]},
                    "level": {"type": "integer", "default": 0},
                },
                "required": ["text"],
            },
        )
    )

    tools.append(
        Tool(
            name="indent_list_item",
            description="Increase indentation of a list item",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                },
                "required": ["paragraph_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="outdent_list_item",
            description="Decrease indentation of a list item",
            inputSchema={
                "type": "object",
                "properties": {
                    "paragraph_index": {"type": "integer"},
                },
                "required": ["paragraph_index"],
            },
        )
    )

    # ==========================================================================
    # Image Tools (63-70)
    # ==========================================================================
    tools.append(
        Tool(
            name="insert_image",
            description="Insert an image into the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string"},
                    "width": {"type": "number", "description": "Width in inches"},
                    "height": {"type": "number", "description": "Height in inches"},
                },
                "required": ["image_path"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_image_count",
            description="Get the number of images in the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="resize_image",
            description="Resize an image",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                    "width": {"type": "number"},
                    "height": {"type": "number"},
                },
                "required": ["index"],
            },
        )
    )

    tools.append(
        Tool(
            name="delete_image",
            description="Delete an image",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                },
                "required": ["index"],
            },
        )
    )

    # ==========================================================================
    # Layout Tools (71-78)
    # ==========================================================================
    tools.append(
        Tool(
            name="get_section",
            description="Get section layout information",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "default": 0},
                },
            },
        )
    )

    tools.append(
        Tool(
            name="set_page_margins",
            description="Set page margins",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_index": {"type": "integer", "default": 0},
                    "top": {"type": "number"},
                    "bottom": {"type": "number"},
                    "left": {"type": "number"},
                    "right": {"type": "number"},
                },
            },
        )
    )

    tools.append(
        Tool(
            name="set_page_orientation",
            description="Set page orientation",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_index": {"type": "integer", "default": 0},
                    "orientation": {
                        "type": "string",
                        "enum": ["portrait", "landscape"],
                    },
                },
                "required": ["orientation"],
            },
        )
    )

    tools.append(
        Tool(
            name="set_header",
            description="Set header content",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "section_index": {"type": "integer", "default": 0},
                },
                "required": ["text"],
            },
        )
    )

    tools.append(
        Tool(
            name="set_footer",
            description="Set footer content",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "section_index": {"type": "integer", "default": 0},
                },
                "required": ["text"],
            },
        )
    )

    tools.append(
        Tool(
            name="add_page_break",
            description="Add a page break",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="add_section",
            description="Add a new section",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_type": {
                        "type": "string",
                        "enum": ["continuous", "new_page"],
                    },
                },
            },
        )
    )

    # ==========================================================================
    # TOC and Navigation Tools (79-85)
    # ==========================================================================
    tools.append(
        Tool(
            name="add_table_of_contents",
            description="Add a table of contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "default": "Table of Contents"},
                    "max_level": {"type": "integer", "default": 3},
                },
            },
        )
    )

    tools.append(
        Tool(
            name="get_headings",
            description="Get all headings in the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="add_bookmark",
            description="Add a bookmark",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "paragraph_index": {"type": "integer"},
                },
                "required": ["name", "paragraph_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_bookmarks",
            description="Get all bookmarks",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="add_hyperlink",
            description="Add a hyperlink",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "url": {"type": "string"},
                    "paragraph_index": {"type": "integer"},
                },
                "required": ["text", "url", "paragraph_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_hyperlinks",
            description="Get all hyperlinks in the document",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    # ==========================================================================
    # Comment Tools (86-90)
    # ==========================================================================
    tools.append(
        Tool(
            name="add_comment",
            description="Add a comment to the document",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "author": {"type": "string"},
                    "paragraph_index": {"type": "integer"},
                },
                "required": ["text", "paragraph_index"],
            },
        )
    )

    tools.append(
        Tool(
            name="get_comments",
            description="Get all comments",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="resolve_comment",
            description="Resolve a comment",
            inputSchema={
                "type": "object",
                "properties": {
                    "comment_id": {"type": "integer"},
                },
                "required": ["comment_id"],
            },
        )
    )

    tools.append(
        Tool(
            name="delete_comment",
            description="Delete a comment",
            inputSchema={
                "type": "object",
                "properties": {
                    "comment_id": {"type": "integer"},
                },
                "required": ["comment_id"],
            },
        )
    )

    # ==========================================================================
    # Export Tools (91-95)
    # ==========================================================================
    tools.append(
        Tool(
            name="export_to_html",
            description="Export document to HTML",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="export_to_markdown",
            description="Export document to Markdown",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    tools.append(
        Tool(
            name="export_to_text",
            description="Export document to plain text",
            inputSchema={"type": "object", "properties": {}},
        )
    )

    return tools
