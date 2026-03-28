# Docker Build & Run Guide

## Build Docker Image

```bash
docker build -t ai-meeting-intelligence .
```

## Run Container

### Basic Run
```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_api_key_here \
  ai-meeting-intelligence
```

### With Persistent Data
```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_api_key_here \
  -v $(pwd)/data:/app/data \
  ai-meeting-intelligence
```

### With Docker Compose

1. Create `.env.docker` file:
```
GROQ_API_KEY=your_api_key_here
```

2. Run:
```bash
docker-compose up -d
```

3. Access at `http://localhost:8501`

4. Stop:
```bash
docker-compose down
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| GROQ_API_KEY | Groq API key (required) | gsk_... |
| STREAMLIT_SERVER_PORT | Server port | 8501 |
| STREAMLIT_SERVER_HEADLESS | Run headless | true |

## Logs

```bash
# View container logs
docker logs container_name

# Follow logs
docker logs -f container_name
```

## Cleanup

```bash
# Remove container
docker rm container_id

# Remove image
docker rmi ai-meeting-intelligence

# Clean all
docker system prune -a
```

## Deployment

### AWS
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin your-registry
docker tag ai-meeting-intelligence:latest your-registry/ai-meeting-intelligence:latest
docker push your-registry/ai-meeting-intelligence:latest
```

### Google Cloud
```bash
gcloud builds submit --tag gcr.io/your-project/ai-meeting-intelligence
gcloud run deploy ai-meeting-intelligence \
  --image gcr.io/your-project/ai-meeting-intelligence \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key
```

### Azure
```bash
az acr build --registry your-registry -t ai-meeting-intelligence:latest .
```

---

See [README.md](README.md) for more details.
