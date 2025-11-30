# FastAPI Server - Start Guide

## ✅ Issue Fixed

The dependency injection error has been resolved by fixing the `get_repository()` function in `src/api/dependencies.py`.

## 🚀 Starting the Server

### Method 1: Using main.py
```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
python main.py
```

### Method 2: Using uvicorn directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Production mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📡 Access the API

Once the server is running:
- **Swagger UI (Interactive Docs)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Quick Test

Open a new terminal and test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-28T...",
  "version": "2.0.0"
}
```

## 📝 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/scrape` | Trigger scraping (23 sources) |
| POST | `/api/v1/workflow/run` | Run complete 6-stage workflow |
| GET | `/api/v1/digests` | Get recent digests (paginated) |
| POST | `/api/v1/search` | Semantic search with RAG |
| GET | `/api/v1/stats` | System statistics |
| GET | `/api/v1/articles` | Get articles by source type |

## 🔧 What Was Fixed

**Problem**: FastAPI dependency injection error with `get_repository()` function

**Solution**: Removed the problematic default parameter `db: Session = None` from the dependency function

**Changed in**: `src/api/dependencies.py`

```python
# Before (caused error)
def get_repository(db: Session = None) -> Repository:
    return Repository(session=db)

# After (fixed)
def get_repository() -> Repository:
    return Repository()
```

## ✅ Next Steps

1. Start the server using one of the methods above
2. Open http://localhost:8000/docs in your browser
3. Test the endpoints using the interactive Swagger UI
4. Try the example cURL commands from API_GUIDE.md

## 📊 Updated Resume Description

```latex
{\textbf{AI News Aggregator with RAG \& Multi-Agent Curation}}{\textbf{[Backend + AI/ML]}}
        \resumeItemListStart
            \resumeItem{Built an AI-powered news curation platform using \textbf{Google Gemini 2.5 Flash}, \textbf{LangGraph}, and \textbf{RAG architecture}, aggregating content from \textbf{23 sources} to deliver \textbf{top 10 personalized articles} via \textbf{Gmail}. Implemented \textbf{6-stage pipeline} with \textbf{ChromaDB} (\textbf{384-dimensional embeddings}), \textbf{PostgreSQL}, and \textbf{3 AI agents}. Developed \textbf{FastAPI REST API} with \textbf{7 endpoints}, \textbf{background task processing}, and \textbf{Swagger documentation}, alongside \textbf{Click CLI} for workflow automation.}
        \resumeItemListEnd
```

---

**The FastAPI integration is now complete and ready to use!** 🎉
