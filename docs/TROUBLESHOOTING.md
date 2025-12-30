# Troubleshooting Guide

## Common Issues

### Server Won't Start

**Port in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

### Database Errors

**Connection refused:**
- Check DATABASE_URL
- Verify database is running
- Check credentials

**Migration errors:**
```bash
alembic upgrade head
```

### Redis Errors

**Connection failed:**
```bash
redis-cli ping
# Should return PONG
```

### Document Processing

**File not found:**
- Check UPLOAD_DIR exists
- Verify file permissions

**Invalid DOCX:**
- Ensure file is valid DOCX format
- Check file is not corrupted

### Memory Issues

- Reduce WORKERS count
- Limit MAX_UPLOAD_SIZE
- Process large documents async

## Logs

```bash
# Docker
docker-compose logs -f api

# Systemd
journalctl -u docx-api -f
```

## Getting Help

1. Check logs for errors
2. Search GitHub issues
3. Open new issue with details
