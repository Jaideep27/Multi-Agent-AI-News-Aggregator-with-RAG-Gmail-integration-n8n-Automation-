"""FastAPI routes for AI News Aggregator API."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
import structlog

from .schemas import (
    HealthResponse,
    ScrapeRequest,
    ScrapeResponse,
    WorkflowRequest,
    WorkflowResponse,
    DigestsListResponse,
    DigestResponse,
    SearchRequest,
    SearchResponse,
    SearchResultItem,
    StatsResponse,
    SourceStats,
    ArticlesListResponse,
    ArticleResponse,
    SendEmailRequest,
    SendEmailResponse,
)
from .dependencies import get_repository, get_app_settings, get_retriever
from .background import run_workflow_background, run_scraping_background
from src.database.repository import Repository
from src.config.settings import Settings
from src.database.models import YouTubeVideo, WebArticle

log = structlog.get_logger()
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(settings: Settings = Depends(get_app_settings)):
    """
    Health check endpoint.
    
    Returns:
        Health status with timestamp and version
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version
    )


@router.post("/api/v1/scrape", response_model=ScrapeResponse, tags=["Scraping"])
async def scrape_sources(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    repo: Repository = Depends(get_repository)
):
    """
    Trigger scraping of all 23 sources (3 YouTube + 20 Web).
    
    This runs in the background and returns immediately.
    
    Args:
        request: Scrape request with time window
        background_tasks: FastAPI background tasks
        repo: Database repository
        
    Returns:
        Scraping status and counts
    """
    try:
        log.info("API: Scraping triggered", hours=request.hours)
        
        # Run scraping in background
        background_tasks.add_task(run_scraping_background, request.hours)
        
        return ScrapeResponse(
            success=True,
            youtube_count=0,
            web_count=0,
            total_count=0,
            message=f"Scraping started for last {request.hours} hours. Running in background."
        )
    except Exception as e:
        log.error("API: Scraping failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/workflow/run", response_model=WorkflowResponse, tags=["Workflow"])
async def run_complete_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks
):
    """
    Run the complete AI news aggregator workflow.
    
    Stages:
    1. Scraping (23 sources)
    2. Processing (transcripts/markdown)
    3. Digest generation (AI summaries)
    4. RAG indexing (vector database)
    5. Ranking (personalized curation)
    6. Email delivery (optional)
    
    Args:
        request: Workflow request parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Workflow execution status
    """
    try:
        log.info("API: Workflow triggered", hours=request.hours, top_n=request.top_n)
        
        # Run workflow in background
        background_tasks.add_task(
            run_workflow_background,
            request.hours,
            request.top_n,
            request.skip_email
        )
        
        return WorkflowResponse(
            success=True,
            articles_scraped=0,
            digests_created=0,
            articles_ranked=0,
            email_sent=not request.skip_email,
            message=f"Workflow started. Processing last {request.hours} hours, top {request.top_n} articles.",
            errors=[]
        )
    except Exception as e:
        log.error("API: Workflow failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/email/send", response_model=SendEmailResponse, tags=["Email"])
async def send_email_digest(
    request: SendEmailRequest,
    repo: Repository = Depends(get_repository),
    settings: Settings = Depends(get_app_settings)
):
    """
    Send AI news digest email immediately (on-demand).

    Perfect for:
    - Manual trigger from Streamlit UI
    - n8n scheduled workflows
    - External integrations

    Args:
        request: Email request with time window and top N articles
        repo: Database repository
        settings: Application settings

    Returns:
        Email send status and details
    """
    try:
        from src.database.repository import Repository
        from src.agents.email import EmailAgent, RankedArticleDetail
        from src.services.email import send_email, digest_to_html
        import os

        log.info("API: Email digest requested",
                hours=request.hours,
                top_n=request.top_n,
                recipient=request.recipient)

        # Get recent digests
        digests = repo.get_recent_digests(hours=request.hours)

        if not digests:
            raise HTTPException(
                status_code=404,
                detail=f"No digests found in the last {request.hours} hours. Run the workflow first."
            )

        # Convert to ranked article format (using digest scores or default ranking)
        ranked_articles = []
        for idx, digest in enumerate(digests[:request.top_n]):
            ranked_articles.append(
                RankedArticleDetail(
                    digest_id=digest['id'],
                    rank=idx + 1,
                    relevance_score=10.0 - (idx * 0.5),  # Simple scoring
                    title=digest['title'],
                    summary=digest['summary'],
                    url=digest['url'],
                    article_type=digest['article_type'],
                    reasoning=f"Ranked #{idx + 1} based on recency and relevance"
                )
            )

        # Create email using EmailAgent
        user_profile = {
            "name": settings.user_name if hasattr(settings, 'user_name') else "AI Enthusiast",
            "interests": ["AI", "Machine Learning", "LLMs", "AI Safety"]
        }

        email_agent = EmailAgent(user_profile=user_profile)
        email_digest = email_agent.create_email_digest_response(
            ranked_articles=ranked_articles,
            total_ranked=len(digests),
            limit=request.top_n
        )

        # Generate email content
        subject = request.subject or f"🤖 AI News Digest - Top {request.top_n} Articles"
        text_content = email_digest.to_markdown()
        html_content = digest_to_html(email_digest)

        # Determine recipient
        recipient = request.recipient or os.getenv("MY_EMAIL")
        if not recipient:
            raise HTTPException(
                status_code=400,
                detail="No recipient specified and MY_EMAIL not configured"
            )

        # Send email
        send_email(
            subject=subject,
            body_text=text_content,
            body_html=html_content,
            recipients=[recipient]
        )

        log.info("API: Email sent successfully", recipient=recipient, articles=len(ranked_articles))

        return SendEmailResponse(
            success=True,
            message=f"Email digest sent successfully to {recipient}",
            articles_count=len(ranked_articles),
            recipient=recipient,
            sent_at=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error("API: Email sending failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@router.get("/api/v1/digests", response_model=DigestsListResponse, tags=["Digests"])
async def get_digests(
    hours: int = Query(default=24, ge=1, le=168, description="Time window in hours"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    repo: Repository = Depends(get_repository)
):
    """
    Get recent article digests with pagination.
    
    Args:
        hours: Time window for digests
        page: Page number (1-indexed)
        page_size: Number of items per page
        repo: Database repository
        
    Returns:
        Paginated list of digests
    """
    try:
        log.info("API: Fetching digests", hours=hours, page=page, page_size=page_size)
        
        # Get all digests
        all_digests = repo.get_recent_digests(hours=hours)
        total = len(all_digests)
        
        # Paginate
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_digests = all_digests[start_idx:end_idx]
        
        # Convert to response models
        digest_responses = [
            DigestResponse(
                id=d["id"],
                article_type=d["article_type"],
                article_id=d["article_id"],
                url=d["url"],
                title=d["title"],
                summary=d["summary"],
                created_at=d["created_at"]
            )
            for d in paginated_digests
        ]
        
        return DigestsListResponse(
            digests=digest_responses,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        log.error("API: Failed to fetch digests", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/search", response_model=SearchResponse, tags=["Search"])
async def semantic_search(
    request: SearchRequest,
    retriever = Depends(get_retriever),
    repo: Repository = Depends(get_repository)
):
    """
    Semantic search using RAG (vector similarity).
    
    Find articles similar to your query using embeddings.
    
    Args:
        request: Search request with query and filters
        retriever: RAG retriever instance
        repo: Database repository
        
    Returns:
        Search results with similarity scores
    """
    try:
        log.info("API: Search query", query=request.query, n_results=request.n_results)
        
        # Perform semantic search
        similar = retriever.find_similar(
            query=request.query,
            n_results=request.n_results,
            article_type=request.article_type
        )
        
        # Convert to response format
        results = []
        for item in similar:
            metadata = item.get("metadata", {})
            distance = item.get("distance", 0)
            similarity = 1 - distance if distance is not None else 0
            
            results.append(SearchResultItem(
                title=metadata.get("title", "N/A"),
                url=metadata.get("url", ""),
                article_type=metadata.get("article_type", "unknown"),
                similarity=similarity,
                summary=metadata.get("summary")
            ))
        
        return SearchResponse(
            query=request.query,
            results=results,
            total=len(results)
        )
    except Exception as e:
        log.error("API: Search failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_statistics(
    repo: Repository = Depends(get_repository),
    retriever = Depends(get_retriever),
    settings: Settings = Depends(get_app_settings)
):
    """
    Get system statistics.
    
    Returns:
        System statistics including database and vector store counts
    """
    try:
        log.info("API: Fetching statistics")
        
        # Get counts from database
        youtube_count = repo.session.query(YouTubeVideo).count()
        web_count = repo.session.query(WebArticle).count()
        digest_count = len(repo.get_recent_digests(hours=24*365))  # All time
        
        # Get vector store count
        vector_count = retriever.count_articles()
        
        return StatsResponse(
            sources=SourceStats(
                youtube_videos=youtube_count,
                web_articles=web_count,
                total_digests=digest_count,
                vector_store_count=vector_count
            ),
            database_status="connected",
            vector_store_status="healthy",
            gemini_model=settings.gemini_model_digest,
            embedding_model=settings.embedding_model,
            last_updated=datetime.now()
        )
    except Exception as e:
        log.error("API: Failed to fetch statistics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/articles", response_model=ArticlesListResponse, tags=["Articles"])
async def get_articles(
    source_type: str = Query(default="youtube", description="Source type: youtube, web"),
    limit: int = Query(default=50, ge=1, le=200, description="Number of articles"),
    repo: Repository = Depends(get_repository)
):
    """
    Get recent articles by source type.
    
    Args:
        source_type: Type of source (youtube or web)
        limit: Maximum number of articles
        repo: Database repository
        
    Returns:
        List of articles
    """
    try:
        log.info("API: Fetching articles", source_type=source_type, limit=limit)
        
        articles = []
        
        if source_type.lower() == "youtube":
            videos = repo.session.query(YouTubeVideo).order_by(
                YouTubeVideo.published_at.desc()
            ).limit(limit).all()
            
            articles = [
                ArticleResponse(
                    id=v.video_id,
                    title=v.title,
                    url=v.url,
                    published_at=v.published_at,
                    source="YouTube",
                    description=v.description
                )
                for v in videos
            ]
        elif source_type.lower() == "web":
            web_articles = repo.session.query(WebArticle).order_by(
                WebArticle.published_at.desc()
            ).limit(limit).all()
            
            articles = [
                ArticleResponse(
                    id=a.guid,
                    title=a.title,
                    url=a.url,
                    published_at=a.published_at,
                    source=a.source_name,
                    description=a.description
                )
                for a in web_articles
            ]
        else:
            raise HTTPException(status_code=400, detail="Invalid source_type. Use 'youtube' or 'web'")
        
        return ArticlesListResponse(
            articles=articles,
            total=len(articles),
            source_type=source_type
        )
    except HTTPException:
        raise
    except Exception as e:
        log.error("API: Failed to fetch articles", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
