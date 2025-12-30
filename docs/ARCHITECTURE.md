# Architecture Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Load Balancer                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
         ┌──────────┐    ┌──────────┐    ┌──────────┐
         │ API Pod  │    │ API Pod  │    │ API Pod  │
         │ (FastAPI)│    │ (FastAPI)│    │ (FastAPI)│
         └──────────┘    └──────────┘    └──────────┘
                │               │               │
                └───────────────┼───────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
         ┌──────────┐    ┌──────────┐    ┌──────────┐
         │PostgreSQL│    │  Redis   │    │  Celery  │
         │    DB    │    │  Cache   │    │ Workers  │
         └──────────┘    └──────────┘    └──────────┘
```

## Component Overview

### API Layer (FastAPI)
- RESTful endpoints for document operations
- OpenAPI/Swagger documentation
- Request validation with Pydantic
- Async/await for high performance

### MCP Server
- Model Context Protocol implementation
- 80+ tools for AI integrations
- stdio transport for CLI tools

### Service Layer
- Business logic encapsulation
- Database interactions
- Handler coordination

### Handler Layer
- Low-level DOCX operations
- python-docx integration
- File format handling

### Database
- PostgreSQL for production
- SQLite for development
- SQLAlchemy ORM with async support

### Background Tasks
- Celery for long-running operations
- Redis as message broker
- Scheduled jobs with Celery Beat

## Data Flow

1. Request → API Route
2. Route → Service (business logic)
3. Service → Handler (DOCX operations)
4. Handler → Document file
5. Service → Database (metadata)
6. Response ← API Route

## Security

- JWT authentication
- Password hashing (bcrypt)
- API key support
- Rate limiting
- Input validation
