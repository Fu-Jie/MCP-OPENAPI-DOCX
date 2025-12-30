# API Documentation

Complete reference for the MCP-OPENAPI-DOCX REST API.

## Overview

- **Base URL**: `/api/v1`
- **Content Type**: `application/json`
- **Authentication**: Bearer token (optional in development)

## Interactive Documentation

Access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Endpoints Reference

### Health Check

#### GET /api/v1/health

Check API health status.

**Response**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Documents

#### GET /api/v1/documents

List all documents.

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Number of records to skip (default: 0) |
| limit | int | Maximum records to return (default: 20, max: 100) |
| search | string | Search query for document names |

**Response**

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "My Document",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 20
}
```

#### POST /api/v1/documents

Create a new document.

**Request Body**

```json
{
  "name": "My Document",
  "template_id": "optional-template-id",
  "metadata": {
    "author": "John Doe"
  }
}
```

**Response** (201 Created)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Document",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET /api/v1/documents/{document_id}

Get document details.

**Response**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Document",
  "current_version": 1,
  "metadata": {},
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /api/v1/documents/{document_id}

Update document metadata.

**Request Body**

```json
{
  "name": "Updated Name",
  "metadata": {
    "author": "Jane Doe"
  }
}
```

#### DELETE /api/v1/documents/{document_id}

Delete a document.

**Response** (204 No Content)

### Text Operations

#### GET /api/v1/text/{document_id}/paragraphs

Get all paragraphs.

**Response**

```json
[
  {
    "index": 0,
    "text": "First paragraph",
    "style": "Normal"
  },
  {
    "index": 1,
    "text": "Second paragraph",
    "style": "Normal"
  }
]
```

#### POST /api/v1/text/{document_id}/paragraphs

Add a paragraph.

**Request Body**

```json
{
  "text": "New paragraph text",
  "style": "Heading 1",
  "position": 0
}
```

#### PUT /api/v1/text/{document_id}/paragraphs/{index}

Update a paragraph.

**Request Body**

```json
{
  "text": "Updated text",
  "style": "Normal"
}
```

#### DELETE /api/v1/text/{document_id}/paragraphs/{index}

Delete a paragraph.

#### POST /api/v1/text/{document_id}/format

Apply formatting.

**Request Body**

```json
{
  "paragraph_index": 0,
  "run_index": 0,
  "bold": true,
  "italic": false,
  "underline": false,
  "font_name": "Arial",
  "font_size": 12,
  "color": "#000000"
}
```

### Tables

#### GET /api/v1/tables/{document_id}

List all tables.

**Response**

```json
[
  {
    "index": 0,
    "rows": 3,
    "cols": 4
  }
]
```

#### POST /api/v1/tables/{document_id}

Create a table.

**Request Body**

```json
{
  "rows": 3,
  "cols": 4,
  "data": [
    ["A1", "B1", "C1", "D1"],
    ["A2", "B2", "C2", "D2"],
    ["A3", "B3", "C3", "D3"]
  ],
  "style": "Table Grid"
}
```

#### GET /api/v1/tables/{document_id}/{table_index}

Get table data.

**Response**

```json
{
  "index": 0,
  "rows": 3,
  "cols": 4,
  "data": [
    ["A1", "B1", "C1", "D1"],
    ["A2", "B2", "C2", "D2"],
    ["A3", "B3", "C3", "D3"]
  ]
}
```

#### PUT /api/v1/tables/{document_id}/{table_index}/cell

Update a cell.

**Request Body**

```json
{
  "row": 0,
  "col": 0,
  "value": "New Value"
}
```

#### POST /api/v1/tables/{document_id}/{table_index}/row

Add a row.

**Request Body**

```json
{
  "values": ["A", "B", "C", "D"],
  "position": 2
}
```

#### POST /api/v1/tables/{document_id}/{table_index}/column

Add a column.

**Request Body**

```json
{
  "values": ["Header", "Value1", "Value2"],
  "position": 0
}
```

### Lists

#### POST /api/v1/lists/{document_id}/bulleted

Create a bulleted list.

**Request Body**

```json
{
  "items": ["Item 1", "Item 2", "Item 3"]
}
```

#### POST /api/v1/lists/{document_id}/numbered

Create a numbered list.

**Request Body**

```json
{
  "items": ["Step 1", "Step 2", "Step 3"],
  "start": 1
}
```

### Media

#### POST /api/v1/media/{document_id}/images

Upload and insert an image.

**Request** (multipart/form-data)

| Field | Type | Description |
|-------|------|-------------|
| file | file | Image file |
| width | float | Width in inches |
| height | float | Height in inches |

#### GET /api/v1/media/{document_id}/images

List all images.

### Styles

#### GET /api/v1/styles/{document_id}

List available styles.

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by type (paragraph, character, table) |

#### POST /api/v1/styles/{document_id}

Create a custom style.

**Request Body**

```json
{
  "name": "Custom Style",
  "type": "paragraph",
  "base_style": "Normal",
  "font_name": "Arial",
  "font_size": 12,
  "bold": false,
  "italic": false,
  "color": "#000000"
}
```

### Layout

#### GET /api/v1/layout/{document_id}/settings

Get page settings.

#### PUT /api/v1/layout/{document_id}/settings

Update page settings.

**Request Body**

```json
{
  "page_width": 8.5,
  "page_height": 11,
  "margin_top": 1,
  "margin_bottom": 1,
  "margin_left": 1,
  "margin_right": 1,
  "orientation": "portrait"
}
```

#### POST /api/v1/layout/{document_id}/header

Set header.

**Request Body**

```json
{
  "text": "Document Header"
}
```

#### POST /api/v1/layout/{document_id}/footer

Set footer.

**Request Body**

```json
{
  "text": "Page number: "
}
```

### Search

#### GET /api/v1/search/{document_id}

Search text in document.

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| query | string | Search text |
| case_sensitive | bool | Case-sensitive search |
| whole_word | bool | Match whole words |

#### POST /api/v1/search/{document_id}/replace

Replace text.

**Request Body**

```json
{
  "search": "old text",
  "replace": "new text",
  "case_sensitive": false,
  "replace_all": true
}
```

### Export

#### POST /api/v1/export/{document_id}/{format}

Export document.

**Path Parameters**

| Parameter | Values |
|-----------|--------|
| format | pdf, html, markdown, text |

### Templates

#### GET /api/v1/templates

List templates.

#### POST /api/v1/templates

Create a template.

#### POST /api/v1/templates/{template_id}/create

Create document from template.

### Comments

#### GET /api/v1/comments/{document_id}

List comments.

#### POST /api/v1/comments/{document_id}

Add a comment.

**Request Body**

```json
{
  "text": "Comment text",
  "author": "John Doe",
  "paragraph_index": 5
}
```

### Revisions

#### GET /api/v1/revisions/{document_id}

List revisions.

#### POST /api/v1/revisions/{document_id}/enable

Enable revision tracking.

#### POST /api/v1/revisions/{document_id}/accept/{revision_id}

Accept a revision.

#### POST /api/v1/revisions/{document_id}/reject/{revision_id}

Reject a revision.

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 422 | Request validation failed |
| DOCUMENT_NOT_FOUND | 404 | Document does not exist |
| TEMPLATE_NOT_FOUND | 404 | Template does not exist |
| UNAUTHORIZED | 401 | Authentication required |
| FORBIDDEN | 403 | Permission denied |
| PROCESSING_ERROR | 500 | Document processing failed |
| INTERNAL_ERROR | 500 | Unexpected server error |

## Rate Limiting

Default rate limits:

- 100 requests per minute per IP
- 1000 requests per hour per API key

Headers in response:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## Pagination

List endpoints support pagination:

```
GET /api/v1/documents?skip=0&limit=20
```

Response includes:

```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 20
}
```

## Filtering and Sorting

Many endpoints support filtering:

```
GET /api/v1/documents?search=report&sort=created_at&order=desc
```
