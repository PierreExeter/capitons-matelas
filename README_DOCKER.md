# Docker Deployment Guide

## Overview

This guide explains how to containerize and deploy the mattress button point calculator using Docker.

## Files Created

- **Dockerfile**: Multi-stage production-ready container
- **docker-compose.yml**: Development and production configurations
- **.dockerignore**: Excludes unnecessary files from build context

## Quick Start

### Development Environment

```bash
# Clone and navigate to the project
cd matelas-calc

# Start development container with hot reload
docker compose up matelas-calc-dev

# Or run in detached mode
docker compose up -d matelas-calc-dev
```

Access the application at: http://localhost:5000

### Production Environment

```bash
# Start production container
docker compose --profile prod up matelas-calc-prod

# Or run in detached mode
docker compose --profile prod up -d matelas-calc-prod
```

Access the application at: http://localhost:5001

## Manual Docker Build

### Build the Image

```bash
# Build the Docker image
docker build -t matelas-calc:latest .

# Build with custom tag
docker build -t matelas-calc:v1.0 .
```

### Run the Container

```bash
# Basic run
docker run -p 5000:5000 --name matelas-calc matelas-calc:latest

# Run with environment variables
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  --name matelas-calc matelas-calc:latest

# Run in detached mode
docker run -d -p 5000:5000 --name matelas-calc matelas-calc:latest
```

## Container Features

### Security
- Non-root user execution (`appuser`)
- Minimal attack surface
- Environment variable configuration

### Performance
- Multi-stage build for smaller image size
- Optimized layer caching
- Health checks for monitoring

### Development
- Hot reload support
- Volume mounting for live code changes
- Debug mode configuration

## Environment Variables

| Variable | Default | Description |
|-----------|----------|-------------|
| `FLASK_APP` | `app.py` | Flask application file |
| `FLASK_ENV` | `production` | Environment mode |
| `FLASK_DEBUG` | `0` | Debug mode |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |

## Health Checks

The container includes built-in health checks:

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"

# View health logs
docker inspect --format='{{json .State.Health}}' matelas-calc
```

## Production Deployment

### Docker Hub

```bash
# Tag for Docker Hub
docker tag matelas-calc:latest yourusername/matelas-calc:latest

# Push to Docker Hub
docker push yourusername/matelas-calc:latest
```

### Cloud Services

#### AWS ECS/EKS
```bash
# Push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker tag matelas-calc:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/matelas-calc:latest
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/matelas-calc:latest
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/matelas-calc
gcloud run deploy --image gcr.io/PROJECT-ID/matelas-calc --platform managed
```

#### Azure Container Instances
```bash
# Deploy to Azure
az container create \
  --resource-group matelas-calc-rg \
  --name matelas-calc \
  --image yourregistry/matelas-calc:latest \
  --cpu 1 --memory 1 \
  --ports 5000
```

## Monitoring and Logs

### View Logs
```bash
# Docker logs
docker logs matelas-calc

# Follow logs
docker logs -f matelas-calc

# Docker Compose logs
docker compose logs matelas-calc-dev
docker compose logs -f matelas-calc-dev
```

### Resource Monitoring
```bash
# Container stats
docker stats matelas-calc

# Inspect container
docker inspect matelas-calc
```

## Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :5000
   # Use different port
   docker run -p 5001:5000 matelas-calc
   ```

2. **Permission issues**
   ```bash
   # Check container user
   docker exec matelas-calc whoami
   ```

3. **Health check failures**
   ```bash
   # Manual health check
   docker exec matelas-calc curl -f http://localhost:5000/
   ```

### Debug Mode

For development debugging:

```bash
# Enable debug environment
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e FLASK_DEBUG=1 \
  --name matelas-calc-debug \
  matelas-calc:latest
```

## Volume Mounting

For persistent data or development:

```bash
# Mount current directory
docker run -p 5000:5000 \
  -v $(pwd):/app \
  matelas-calc:latest

# Mount specific directory
docker run -p 5000:5000 \
  -v ./logs:/app/logs \
  matelas-calc:latest
```

## Network Configuration

### Custom Network
```bash
# Create network
docker network create matelas-network

# Run with network
docker run -p 5000:5000 \
  --network matelas-network \
  --name matelas-calc \
  matelas-calc:latest
```

## Cleanup

```bash
# Stop and remove container
docker stop matelas-calc && docker rm matelas-calc

# Remove image
docker rmi matelas-calc:latest

# Clean up with Docker Compose
docker compose down
docker compose --profile prod down

# Remove volumes
docker compose down -v
```

## Production Best Practices

1. **Use specific image tags** instead of `latest`
2. **Resource limits** for production deployments
3. **Health checks** for automated recovery
4. **Logging configuration** for monitoring
5. **Secrets management** for sensitive data
6. **Regular updates** for security patches

## Support

For issues related to:
- Docker: Check [Docker Documentation](https://docs.docker.com/)
- Docker Compose: Check [Docker Compose Documentation](https://docs.docker.com/compose/)
- Application: Check the main README.md file
