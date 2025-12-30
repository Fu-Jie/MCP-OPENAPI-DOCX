# MCP-OPENAPI-DOCX

Enterprise-grade document editing and management server supporting MCP (Model Context Protocol) and OpenAPI protocols for DOCX documents.

[![CI/CD Pipeline](https://github.com/Fu-Jie/MCP-OPENAPI-DOCX/actions/workflows/ci.yml/badge.svg)](https://github.com/Fu-Jie/MCP-OPENAPI-DOCX/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Features

- **Complete DOCX Support**: Full support for reading, writing, and editing Microsoft Word documents
- **MCP Protocol**: Implements the Model Context Protocol for AI-powered document operations
- **RESTful API**: Comprehensive OpenAPI-compliant REST API with Swagger documentation
- **Async Architecture**: Built with FastAPI and async/await for high performance
- **Document Processing**: Paragraphs, tables, lists, images, styles, and more
- **Version Control**: Track document versions and compare changes
- **Template Management**: Create and manage document templates
- **Export Options**: Export to PDF, HTML, Markdown, and plain text
- **Comments & Revisions**: Add comments and track changes
- **Security**: Document encryption, password protection, and permissions
- **Background Tasks**: Celery integration for long-running operations
- **Containerized**: Docker and Kubernetes ready

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [MCP Protocol](#mcp-protocol)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (optional)
- PostgreSQL (optional, SQLite available for development)
- Redis (for Celery tasks)

### Using Poetry

```bash
# Clone the repository
git clone https://github.com/Fu-Jie/MCP-OPENAPI-DOCX.git
cd MCP-OPENAPI-DOCX

# Install dependencies
pip install poetry
poetry install

# Run the application
poetry run docx-server
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/Fu-Jie/MCP-OPENAPI-DOCX.git
cd MCP-OPENAPI-DOCX

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn src.api.main:app --reload
```

### Using Docker

```bash
# Clone the repository
git clone https://github.com/Fu-Jie/MCP-OPENAPI-DOCX.git
cd MCP-OPENAPI-DOCX

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

## 🏃 Quick Start

### Start the API Server

```bash
# Development mode
python -m uvicorn src.api.main:app --reload --port 8000

# Production mode
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Start the MCP Server

```bash
# Run MCP server (for AI integrations)
poetry run mcp-server
```

## 📖 API Documentation

The API provides comprehensive endpoints for document management:

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/documents` | GET | List all documents |
| `/api/v1/documents` | POST | Create a new document |
| `/api/v1/documents/{id}` | GET | Get document details |
| `/api/v1/documents/{id}` | PUT | Update document |
| `/api/v1/documents/{id}` | DELETE | Delete document |

### Text Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/text/{doc_id}/paragraphs` | GET | List paragraphs |
| `/api/v1/text/{doc_id}/paragraphs` | POST | Add paragraph |
| `/api/v1/text/{doc_id}/paragraphs/{idx}` | PUT | Update paragraph |
| `/api/v1/text/{doc_id}/format` | POST | Apply formatting |

### Table Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/tables/{doc_id}` | GET | List tables |
| `/api/v1/tables/{doc_id}` | POST | Create table |
| `/api/v1/tables/{doc_id}/{idx}/cell` | PUT | Update cell |
| `/api/v1/tables/{doc_id}/{idx}/row` | POST | Add row |

See the full [API Documentation](docs/API_DOCUMENTATION.md) for complete details.

## 🔌 MCP Protocol

This server implements the Model Context Protocol for AI integrations:

### Available Tools

- `create_document` - Create a new DOCX document
- `open_document` - Open an existing document
- `add_paragraph` - Add a paragraph to a document
- `add_table` - Add a table to a document
- `format_text` - Apply text formatting
- `search_replace` - Search and replace text
- `export_document` - Export to various formats
- And 80+ more tools...

### Example Usage

```python
# Using MCP client
async with MCPClient("http://localhost:8000/mcp") as client:
    result = await client.call_tool(
        "create_document",
        {"name": "My Document"}
    )
```

See the [MCP Protocol Guide](docs/MCP_PROTOCOL.md) for detailed usage.

## ⚙️ Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### Key Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `sqlite+aiosqlite:///./docx_db.sqlite` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT secret key | (required in production) |
| `DEBUG` | Enable debug mode | `false` |
| `ENVIRONMENT` | Environment name | `development` |
| `UPLOAD_DIR` | Upload directory | `./uploads` |
| `MAX_UPLOAD_SIZE` | Max upload size (bytes) | `104857600` |

See `.env.example` for all available options.

## 🛠️ Development

### Project Structure

```
mcp-openapi-docx/
├── src/
│   ├── api/            # FastAPI application
│   │   ├── routes/     # API endpoints
│   │   └── dependencies.py
│   ├── core/           # Core configuration
│   ├── database/       # Database setup
│   ├── handlers/       # DOCX file handlers
│   ├── mcp/            # MCP server
│   ├── middleware/     # HTTP middleware
│   ├── models/         # Data models
│   ├── services/       # Business logic
│   ├── tasks/          # Celery tasks
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── docs/               # Documentation
├── alembic/            # Database migrations
├── kubernetes/         # K8s configurations
└── scripts/            # Utility scripts
```

### Running Locally

```bash
# Install dev dependencies
poetry install --with dev

# Run linting
poetry run ruff check src/
poetry run black --check src/
poetry run isort --check-only src/

# Run type checking
poetry run mypy src/

# Start development server
poetry run uvicorn src.api.main:app --reload
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/handlers/test_document_handler.py

# Run integration tests
pytest tests/integration/ -v
```

## 🚢 Deployment

### Docker Compose (Recommended for Development)

```bash
docker-compose up -d
```

### Kubernetes

```bash
# Apply configurations
kubectl apply -f kubernetes/

# Check status
kubectl get pods -n docx
```

### Manual Deployment

```bash
# Build the image
docker build -t mcp-openapi-docx:latest .

# Run the container
docker run -p 8000:8000 mcp-openapi-docx:latest
```

See the [Deployment Guide](docs/DEPLOYMENT.md) for production recommendations.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/Fu-Jie/MCP-OPENAPI-DOCX/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Fu-Jie/MCP-OPENAPI-DOCX/discussions)

---

Made with ❤️ for the document automation community
