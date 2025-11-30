# FastAPI Integration - Quick Start Guide

## Starting the API Server

### Development Mode (with auto-reload)
```bash
# Activate virtual environment
venv\Scripts\activate

# Start server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Available Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Scraping
```bash
POST http://localhost:8000/api/v1/scrape
Content-Type: application/json

{
  "hours": 24
}
```

### Run Complete Workflow
```bash
POST http://localhost:8000/api/v1/workflow/run
Content-Type: application/json

{
  "hours": 24,
  "top_n": 10,
  "skip_email": false
}
```

### Get Digests
```bash
GET http://localhost:8000/api/v1/digests?hours=24&page=1&page_size=20
```

### Semantic Search
```bash
POST http://localhost:8000/api/v1/search
Content-Type: application/json

{
  "query": "RAG systems and vector databases",
  "n_results": 5,
  "article_type": null
}
```

### System Statistics
```bash
GET http://localhost:8000/api/v1/stats
```

### Get Articles
```bash
GET http://localhost:8000/api/v1/articles?source_type=youtube&limit=50
GET http://localhost:8000/api/v1/articles?source_type=web&limit=50
```

## Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Trigger scraping
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"hours": 24}'

# Get statistics
curl http://localhost:8000/api/v1/stats

# Search
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "LangGraph workflows", "n_results": 5}'
```

## Features

✅ **7 REST Endpoints**
✅ **Background Task Support** for long-running operations
✅ **CORS Enabled** for cross-origin requests
✅ **Swagger UI Documentation** at `/docs`
✅ **Pydantic Validation** for all requests/responses
✅ **Structured Logging** with context
✅ **Pagination Support** for digests and articles

## Architecture

- **main.py** - FastAPI application entry point
- **src/api/routes.py** - All API endpoints
- **src/api/schemas.py** - Pydantic models for validation
- **src/api/dependencies.py** - Dependency injection
- **src/api/background.py** - Background task handlers
