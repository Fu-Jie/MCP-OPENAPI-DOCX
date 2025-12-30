# MCP Protocol Guide

This guide explains how to use the Model Context Protocol (MCP) interface for AI-powered document operations.

## Overview

The MCP server provides a standardized interface for AI models to interact with DOCX documents. It follows the [MCP Specification](https://modelcontextprotocol.io/).

## Starting the MCP Server

```bash
# Using Poetry
poetry run mcp-server

# Using Python directly
python -m src.mcp.server
```

The MCP server uses stdio transport by default.

## Configuration

Configure MCP settings in `.env`:

```env
MCP_SERVER_NAME=docx-mcp-server
MCP_SERVER_VERSION=1.0.0
MCP_TRANSPORT=stdio
```

## Available Tools

### Document Management

#### create_document

Create a new DOCX document.

**Parameters:**
- `name` (string, required): Document name

**Returns:**
```json
{
  "document_id": "...",
  "name": "...",
  "file_path": "..."
}
```

#### open_document

Open an existing document.

**Parameters:**
- `document_id` (string, required): Document ID

#### save_document

Save document changes.

**Parameters:**
- `document_id` (string, required): Document ID

#### get_document_info

Get document metadata.

**Parameters:**
- `document_id` (string, required): Document ID

### Text Operations

#### add_paragraph

Add a paragraph to the document.

**Parameters:**
- `document_id` (string, required): Document ID
- `text` (string, required): Paragraph text
- `style` (string, optional): Paragraph style

#### update_paragraph

Update existing paragraph text.

**Parameters:**
- `document_id` (string, required): Document ID
- `paragraph_index` (integer, required): Paragraph index
- `text` (string, required): New text

#### delete_paragraph

Delete a paragraph.

**Parameters:**
- `document_id` (string, required): Document ID
- `paragraph_index` (integer, required): Paragraph index

#### format_text

Apply formatting to text.

**Parameters:**
- `document_id` (string, required): Document ID
- `paragraph_index` (integer, required): Paragraph index
- `bold` (boolean, optional): Bold formatting
- `italic` (boolean, optional): Italic formatting
- `underline` (boolean, optional): Underline formatting
- `font_name` (string, optional): Font name
- `font_size` (integer, optional): Font size in points
- `color` (string, optional): Text color (hex)

### Table Operations

#### create_table

Create a new table.

**Parameters:**
- `document_id` (string, required): Document ID
- `rows` (integer, required): Number of rows
- `cols` (integer, required): Number of columns
- `data` (array, optional): Initial table data

#### update_cell

Update a table cell.

**Parameters:**
- `document_id` (string, required): Document ID
- `table_index` (integer, required): Table index
- `row` (integer, required): Row index
- `col` (integer, required): Column index
- `value` (string, required): Cell value

#### add_table_row

Add a row to a table.

**Parameters:**
- `document_id` (string, required): Document ID
- `table_index` (integer, required): Table index
- `values` (array, optional): Row values

### List Operations

#### create_bulleted_list

Create a bulleted list.

**Parameters:**
- `document_id` (string, required): Document ID
- `items` (array, required): List items

#### create_numbered_list

Create a numbered list.

**Parameters:**
- `document_id` (string, required): Document ID
- `items` (array, required): List items
- `start` (integer, optional): Starting number (default: 1)

### Image Operations

#### insert_image

Insert an image.

**Parameters:**
- `document_id` (string, required): Document ID
- `image_path` (string, required): Path to image file
- `width` (number, optional): Width in inches
- `height` (number, optional): Height in inches

### Search and Replace

#### search_text

Search for text in document.

**Parameters:**
- `document_id` (string, required): Document ID
- `query` (string, required): Search query
- `case_sensitive` (boolean, optional): Case-sensitive search

#### replace_text

Replace text in document.

**Parameters:**
- `document_id` (string, required): Document ID
- `search` (string, required): Text to find
- `replace` (string, required): Replacement text
- `replace_all` (boolean, optional): Replace all occurrences

### Export Operations

#### export_document

Export document to another format.

**Parameters:**
- `document_id` (string, required): Document ID
- `format` (string, required): Export format (pdf, html, markdown, text)

### Style Operations

#### apply_style

Apply a style to content.

**Parameters:**
- `document_id` (string, required): Document ID
- `style_name` (string, required): Style name
- `paragraph_index` (integer, optional): Paragraph index

#### create_style

Create a custom style.

**Parameters:**
- `document_id` (string, required): Document ID
- `name` (string, required): Style name
- `type` (string, required): Style type (paragraph, character)
- `font_name` (string, optional): Font name
- `font_size` (integer, optional): Font size
- `bold` (boolean, optional): Bold
- `italic` (boolean, optional): Italic
- `color` (string, optional): Color

### Layout Operations

#### set_page_size

Set document page size.

**Parameters:**
- `document_id` (string, required): Document ID
- `width` (number, required): Width in inches
- `height` (number, required): Height in inches

#### set_margins

Set page margins.

**Parameters:**
- `document_id` (string, required): Document ID
- `top` (number, optional): Top margin
- `bottom` (number, optional): Bottom margin
- `left` (number, optional): Left margin
- `right` (number, optional): Right margin

#### set_header

Set document header.

**Parameters:**
- `document_id` (string, required): Document ID
- `text` (string, required): Header text

#### set_footer

Set document footer.

**Parameters:**
- `document_id` (string, required): Document ID
- `text` (string, required): Footer text

### TOC Operations

#### generate_toc

Generate table of contents.

**Parameters:**
- `document_id` (string, required): Document ID
- `title` (string, optional): TOC title
- `levels` (integer, optional): Heading levels to include

#### add_bookmark

Add a bookmark.

**Parameters:**
- `document_id` (string, required): Document ID
- `name` (string, required): Bookmark name
- `paragraph_index` (integer, required): Paragraph index

#### add_hyperlink

Add a hyperlink.

**Parameters:**
- `document_id` (string, required): Document ID
- `url` (string, required): Link URL
- `text` (string, required): Link text

### Comment Operations

#### add_comment

Add a comment.

**Parameters:**
- `document_id` (string, required): Document ID
- `text` (string, required): Comment text
- `author` (string, required): Comment author
- `paragraph_index` (integer, optional): Paragraph to comment on

#### get_comments

Get all comments.

**Parameters:**
- `document_id` (string, required): Document ID

### Version Operations

#### create_version

Create a new version.

**Parameters:**
- `document_id` (string, required): Document ID
- `comment` (string, optional): Version comment

#### get_versions

Get version history.

**Parameters:**
- `document_id` (string, required): Document ID

#### restore_version

Restore a previous version.

**Parameters:**
- `document_id` (string, required): Document ID
- `version_number` (integer, required): Version to restore

## Resources

The MCP server exposes the following resources:

### document://{document_id}

Access document content and metadata.

### template://{template_id}

Access template information.

## Example Usage

### Python Client

```python
import asyncio
from mcp import Client

async def main():
    async with Client() as client:
        # Create a document
        result = await client.call_tool(
            "create_document",
            {"name": "My Report"}
        )
        doc_id = result["document_id"]

        # Add content
        await client.call_tool(
            "add_paragraph",
            {
                "document_id": doc_id,
                "text": "Introduction",
                "style": "Heading 1"
            }
        )

        await client.call_tool(
            "add_paragraph",
            {
                "document_id": doc_id,
                "text": "This is the introduction paragraph."
            }
        )

        # Create a table
        await client.call_tool(
            "create_table",
            {
                "document_id": doc_id,
                "rows": 3,
                "cols": 3,
                "data": [
                    ["Name", "Age", "City"],
                    ["Alice", "30", "NYC"],
                    ["Bob", "25", "LA"]
                ]
            }
        )

        # Export
        await client.call_tool(
            "export_document",
            {
                "document_id": doc_id,
                "format": "pdf"
            }
        )

asyncio.run(main())
```

### Claude Desktop Integration

Add to your Claude desktop config:

```json
{
  "mcpServers": {
    "docx": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/path/to/mcp-openapi-docx"
    }
  }
}
```

## Error Handling

All tool calls return structured errors:

```json
{
  "error": {
    "code": "TOOL_ERROR",
    "message": "Document not found"
  }
}
```

## Best Practices

1. **Always save** after making changes
2. **Use descriptive names** for documents and styles
3. **Handle errors** gracefully in your client
4. **Use versions** for important documents
5. **Export regularly** for backup

## Troubleshooting

### Connection Issues

- Ensure the MCP server is running
- Check that stdio transport is properly configured
- Verify Python path and dependencies

### Tool Errors

- Verify document_id exists
- Check parameter types and values
- Look for detailed error messages in logs

### Performance

- For large documents, use batch operations
- Consider using background tasks for exports
- Monitor memory usage for image operations
