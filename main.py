"""
FastAPI Application - AI News Aggregator REST API

Production-ready REST API for the AI News Aggregator with:
- 7 REST endpoints
- Background task support
- CORS middleware
- Swagger UI documentation
- Structured logging
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from src.config.settings import get_settings
from src.core.logging import configure_logging
from src.api.routes import router

# Configure logging
settings = get_settings()
configure_logging(settings)

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    log.info("Starting AI News Aggregator API",
             version=settings.app_version,
             environment=settings.environment)

    yield

    # Shutdown
    log.info("Shutting down AI News Aggregator API")


# Create FastAPI app
app = FastAPI(
    title="AI News Aggregator API",
    description="""
    Intelligent news aggregation system with LangGraph, RAG, and Gemini AI.

    ## Features
    - **23 Sources**: 3 YouTube channels + 20 web sources
    - **6-Stage Workflow**: Scraping → Processing → Digest → RAG → Ranking → Email
    - **Multi-Agent System**: Digest, Curator, Email agents
    - **RAG Search**: Semantic search with ChromaDB vector store
    - **Personalized Curation**: AI-powered ranking based on user profiles

    ## Endpoints
    - `/health` - Health check
    - `/api/v1/scrape` - Trigger scraping
    - `/api/v1/workflow/run` - Run complete workflow
    - `/api/v1/digests` - Get recent digests
    - `/api/v1/search` - Semantic search
    - `/api/v1/stats` - System statistics
    - `/api/v1/articles` - Get articles by source
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    
    log.info("Starting FastAPI server",
             host=settings.api_host,
             port=settings.api_port)
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.is_development(),
        workers=settings.api_workers if settings.is_production() else 1,
        log_level=settings.log_level.lower()
    )
