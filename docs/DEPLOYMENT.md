# Deployment Guide

## Docker Deployment

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Kubernetes Deployment

```bash
# Apply namespace and configs
kubectl apply -f kubernetes/configmap.yaml

# Apply storage
kubectl apply -f kubernetes/persistent-volume.yaml

# Deploy application
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Check status
kubectl get pods -n docx
```

## Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Use PostgreSQL database
- [ ] Enable HTTPS
- [ ] Configure rate limiting
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review CORS settings

## Environment Variables

Required for production:

```env
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
ENVIRONMENT=production
DEBUG=false
```

## Scaling

- Horizontal: Add more API pods
- Database: Use read replicas
- Cache: Redis cluster
- Storage: Object storage (S3)
