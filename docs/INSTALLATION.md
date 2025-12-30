# Installation Guide

This guide provides detailed instructions for installing and setting up the MCP-OPENAPI-DOCX server.

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 10 GB
- **OS**: Linux, macOS, or Windows (with WSL2)

### Recommended Requirements

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 50+ GB SSD
- **OS**: Ubuntu 20.04 LTS or newer

### Software Requirements

- Python 3.10 or higher
- Docker 20.10+ and Docker Compose 2.0+ (optional)
- PostgreSQL 13+ (optional, SQLite available)
- Redis 6+ (for background tasks)

## Installation Methods

### Method 1: Using Poetry (Recommended for Development)

```bash
# 1. Clone the repository
git clone https://github.com/Fu-Jie/MCP-OPENAPI-DOCX.git
cd MCP-OPENAPI-DOCX

# 2. Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# 3. Install dependencies
poetry install

# 4. Copy environment configuration
cp .env.example .env

# 5. Initialize the database
poetry run python scripts/init_db.py --seed

# 6. Start the server
poetry run docx-server
```

### Method 2: Using pip

```bash
# 1. Clone the repository
git clone https://github.com/Fu-Jie/MCP-OPENAPI-DOCX.git
cd MCP-OPENAPI-DOCX

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment configuration
cp .env.example .env

# 5. Initialize the database
python scripts/init_db.py --seed

# 6. Start the server
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Method 3: Using Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/Fu-Jie/MCP-OPENAPI-DOCX.git
cd MCP-OPENAPI-DOCX

# 2. Copy environment configuration
cp .env.example .env

# 3. Start all services
docker-compose up -d

# 4. View logs
docker-compose logs -f api

# 5. Stop services
docker-compose down
```

### Method 4: Using Docker

```bash
# 1. Build the image
docker build -t mcp-openapi-docx:latest .

# 2. Run the container
docker run -d \
  --name docx-api \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/exports:/app/exports \
  -e DATABASE_URL=sqlite+aiosqlite:///./docx_db.sqlite \
  -e SECRET_KEY=your-secret-key \
  mcp-openapi-docx:latest
```

## Environment Configuration

### Required Variables

```env
# Security (REQUIRED in production)
SECRET_KEY=your-super-secret-key-change-in-production

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/docx_db

# Redis (for background tasks)
REDIS_URL=redis://localhost:6379/0
```

### Optional Variables

```env
# Application
APP_NAME=MCP-OPENAPI-DOCX
DEBUG=false
ENVIRONMENT=production

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Storage
UPLOAD_DIR=./uploads
EXPORT_DIR=./exports
MAX_UPLOAD_SIZE=104857600

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

See `.env.example` for all available options.

## Database Setup

### SQLite (Development)

No additional setup required. SQLite database is created automatically.

### PostgreSQL (Production)

```bash
# 1. Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# 2. Create database and user
sudo -u postgres psql
CREATE DATABASE docx_db;
CREATE USER docx WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE docx_db TO docx;
\q

# 3. Update DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://docx:your_password@localhost:5432/docx_db

# 4. Run migrations
alembic upgrade head
```

## Redis Setup

### Using Docker

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### System Installation

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server

# macOS
brew install redis
brew services start redis
```

## Verification

### Check API Health

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Access Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test MCP Server

```bash
poetry run mcp-server
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find the process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

#### Database Connection Error

- Verify DATABASE_URL is correct
- Check that the database server is running
- Ensure the database exists and user has access

#### Permission Denied for Uploads

```bash
# Fix directory permissions
chmod -R 755 uploads exports temp
```

#### Redis Connection Error

- Verify Redis is running: `redis-cli ping`
- Check REDIS_URL configuration

## Next Steps

- Read the [Usage Guide](USAGE_GUIDE.md) to learn how to use the API
- Explore the [API Documentation](API_DOCUMENTATION.md) for endpoint details
- Check the [MCP Protocol Guide](MCP_PROTOCOL.md) for AI integration

## Support

If you encounter any issues during installation, please:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/Fu-Jie/MCP-OPENAPI-DOCX/issues)
3. Open a new issue with detailed information about your environment
