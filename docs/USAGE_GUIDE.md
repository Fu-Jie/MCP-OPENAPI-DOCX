# Usage Guide

This guide provides detailed instructions on how to use the MCP-OPENAPI-DOCX server for document editing and management.

## Getting Started

### Starting the Server

```bash
# Development mode with auto-reload
python -m uvicorn src.api.main:app --reload

# Production mode
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

All API endpoints are prefixed with `/api/v1/`.

## Working with Documents

### Creating a Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Document"}'
```

### Uploading an Existing Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@path/to/document.docx" \
  -F "name=Uploaded Document"
```

### Getting Document Details

```bash
curl "http://localhost:8000/api/v1/documents/{document_id}"
```

### Listing Documents

```bash
curl "http://localhost:8000/api/v1/documents?skip=0&limit=20"
```

### Downloading a Document

```bash
curl -O "http://localhost:8000/api/v1/documents/{document_id}/download"
```

### Deleting a Document

```bash
curl -X DELETE "http://localhost:8000/api/v1/documents/{document_id}"
```

## Text Operations

### Adding a Paragraph

```bash
curl -X POST "http://localhost:8000/api/v1/text/{document_id}/paragraphs" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a new paragraph.",
    "style": "Normal"
  }'
```

### Adding a Heading

```bash
curl -X POST "http://localhost:8000/api/v1/text/{document_id}/paragraphs" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Chapter 1: Introduction",
    "style": "Heading 1"
  }'
```

### Formatting Text

```bash
curl -X POST "http://localhost:8000/api/v1/text/{document_id}/format" \
  -H "Content-Type: application/json" \
  -d '{
    "paragraph_index": 0,
    "bold": true,
    "font_name": "Arial",
    "font_size": 14
  }'
```

### Searching and Replacing

```bash
curl -X POST "http://localhost:8000/api/v1/search/{document_id}/replace" \
  -H "Content-Type: application/json" \
  -d '{
    "search": "old text",
    "replace": "new text",
    "replace_all": true
  }'
```

## Table Operations

### Creating a Table

```bash
curl -X POST "http://localhost:8000/api/v1/tables/{document_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "rows": 3,
    "cols": 4,
    "data": [
      ["Header 1", "Header 2", "Header 3", "Header 4"],
      ["Row 1", "Data", "Data", "Data"],
      ["Row 2", "Data", "Data", "Data"]
    ]
  }'
```

### Updating a Cell

```bash
curl -X PUT "http://localhost:8000/api/v1/tables/{document_id}/{table_index}/cell" \
  -H "Content-Type: application/json" \
  -d '{
    "row": 1,
    "col": 2,
    "value": "Updated Value"
  }'
```

### Adding a Row

```bash
curl -X POST "http://localhost:8000/api/v1/tables/{document_id}/{table_index}/row" \
  -H "Content-Type: application/json" \
  -d '{
    "values": ["New", "Row", "Data", "Here"]
  }'
```

## List Operations

### Creating a Bulleted List

```bash
curl -X POST "http://localhost:8000/api/v1/lists/{document_id}/bulleted" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      "First item",
      "Second item",
      "Third item"
    ]
  }'
```

### Creating a Numbered List

```bash
curl -X POST "http://localhost:8000/api/v1/lists/{document_id}/numbered" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      "Step one",
      "Step two",
      "Step three"
    ],
    "start": 1
  }'
```

## Image Operations

### Inserting an Image

```bash
curl -X POST "http://localhost:8000/api/v1/media/{document_id}/images" \
  -F "file=@path/to/image.png" \
  -F "width=4.0" \
  -F "height=3.0"
```

### Listing Images

```bash
curl "http://localhost:8000/api/v1/media/{document_id}/images"
```

## Style Operations

### Listing Available Styles

```bash
curl "http://localhost:8000/api/v1/styles/{document_id}"
```

### Creating a Custom Style

```bash
curl -X POST "http://localhost:8000/api/v1/styles/{document_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Heading",
    "type": "paragraph",
    "font_name": "Calibri",
    "font_size": 18,
    "bold": true,
    "color": "#0066CC"
  }'
```

## Export Operations

### Export to PDF

```bash
curl -X POST "http://localhost:8000/api/v1/export/{document_id}/pdf" \
  -o "output.pdf"
```

### Export to HTML

```bash
curl -X POST "http://localhost:8000/api/v1/export/{document_id}/html" \
  -o "output.html"
```

### Export to Markdown

```bash
curl -X POST "http://localhost:8000/api/v1/export/{document_id}/markdown" \
  -o "output.md"
```

## Template Operations

### Listing Templates

```bash
curl "http://localhost:8000/api/v1/templates"
```

### Creating a Document from Template

```bash
curl -X POST "http://localhost:8000/api/v1/templates/{template_id}/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Document from Template"
  }'
```

## Version Control

### Getting Document Versions

```bash
curl "http://localhost:8000/api/v1/documents/{document_id}/versions"
```

### Restoring a Version

```bash
curl -X POST "http://localhost:8000/api/v1/documents/{document_id}/versions/{version}/restore"
```

## Comments and Revisions

### Adding a Comment

```bash
curl -X POST "http://localhost:8000/api/v1/comments/{document_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This needs revision.",
    "author": "John Doe",
    "paragraph_index": 5
  }'
```

### Listing Comments

```bash
curl "http://localhost:8000/api/v1/comments/{document_id}"
```

### Enabling Revision Tracking

```bash
curl -X POST "http://localhost:8000/api/v1/revisions/{document_id}/enable"
```

## Batch Operations

### Batch Processing

```bash
curl -X POST "http://localhost:8000/api/v1/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {
        "action": "add_paragraph",
        "document_id": "doc-123",
        "params": {"text": "First paragraph"}
      },
      {
        "action": "add_paragraph",
        "document_id": "doc-123",
        "params": {"text": "Second paragraph"}
      }
    ]
  }'
```

## Python SDK Usage

```python
import httpx

class DocxClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def create_document(self, name: str):
        response = await self.client.post(
            f"{self.base_url}/api/v1/documents",
            json={"name": name}
        )
        return response.json()

    async def add_paragraph(self, doc_id: str, text: str, style: str = "Normal"):
        response = await self.client.post(
            f"{self.base_url}/api/v1/text/{doc_id}/paragraphs",
            json={"text": text, "style": style}
        )
        return response.json()

# Usage
async def main():
    client = DocxClient()
    doc = await client.create_document("My Document")
    await client.add_paragraph(doc["id"], "Hello, World!")
```

## Best Practices

1. **Use proper authentication** in production environments
2. **Implement rate limiting** for public APIs
3. **Cache document metadata** for frequently accessed documents
4. **Use background tasks** for long-running operations like PDF export
5. **Regularly backup** uploaded documents and database

## Error Handling

All errors return a consistent JSON format:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document with ID 'xyz' was not found"
  }
}
```

Common HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Next Steps

- Explore the [API Documentation](API_DOCUMENTATION.md) for complete endpoint reference
- Learn about [MCP Protocol](MCP_PROTOCOL.md) for AI integration
- Check the [Architecture Guide](ARCHITECTURE.md) for system design details
