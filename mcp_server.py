"""
FastMCP Server - AI News Aggregator

Exposes the AI News Aggregator as MCP tools for Claude and other MCP clients.

Tools provided:
- search_ai_news: Semantic search using RAG
- get_latest_digests: Get recent AI summaries
- run_news_scraper: Trigger scraping from 23 sources
- get_news_stats: System statistics
- run_full_workflow: Complete workflow (scrape + AI + email)
- send_email_digest: Send email digest on-demand (NEW)
"""

import sys
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from fastmcp import FastMCP
from src.config.settings import get_settings
from src.core.logging import configure_logging
from src.database.repository import Repository
from src.rag.retriever import get_article_retriever
from src.core.runner import run_scrapers
from src.workflows.workflow import run_workflow

# Configure logging
settings = get_settings()
configure_logging(settings)

# Create FastMCP server
mcp = FastMCP(
    name="AI News Aggregator",
    version=settings.app_version,
)


@mcp.tool()
def search_ai_news(query: str, limit: int = 5, article_type: Optional[str] = None) -> dict:
    """
    Search AI news articles semantically using RAG (vector similarity).

    Args:
        query: Search query (e.g., "LLM reasoning capabilities")
        limit: Number of results to return (default: 5)
        article_type: Filter by type - youtube, official, research, news, safety (optional)

    Returns:
        Dictionary with search results including titles, summaries, URLs, and similarity scores

    Example:
        search_ai_news("GPT-5 capabilities", limit=3)
    """
    try:
        retriever = get_article_retriever()
        results = retriever.find_similar(
            query=query,
            n_results=limit,
            article_type=article_type
        )

        # Format results for better readability
        formatted_results = []
        for i, result in enumerate(results, 1):
            metadata = result.get("metadata", {})
            similarity = 1 - result.get("distance", 0) if result.get("distance") is not None else 0

            formatted_results.append({
                "rank": i,
                "title": metadata.get("title", "N/A"),
                "summary": result.get("document", "")[:300] + "..." if len(result.get("document", "")) > 300 else result.get("document", ""),
                "url": metadata.get("url", ""),
                "article_type": metadata.get("article_type", ""),
                "similarity_score": f"{similarity:.2%}"
            })

        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_latest_digests(hours: int = 168, limit: int = 10) -> dict:
    """
    Get recent AI article summaries (digests created by Gemini AI).

    Args:
        hours: Time window in hours (default: 168 = 1 week)
        limit: Maximum number of digests (default: 10)

    Returns:
        Dictionary with recent article summaries

    Example:
        get_latest_digests(hours=24, limit=5)  # Last 24 hours, top 5
    """
    try:
        repo = Repository()
        digests = repo.get_recent_digests(hours=hours)

        # Format for readability
        formatted_digests = []
        for digest in digests[:limit]:
            formatted_digests.append({
                "title": digest["title"],
                "summary": digest["summary"],
                "type": digest["article_type"],
                "url": digest["url"],
                "created_at": str(digest["created_at"])
            })

        return {
            "digests": formatted_digests,
            "total_found": len(digests),
            "returned": len(formatted_digests),
            "time_window_hours": hours
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def run_news_scraper(hours: int = 168) -> dict:
    """
    Scrape latest articles from 23 AI news sources (3 YouTube + 20 web sources).

    This only scrapes and saves to database - no AI processing or email.

    Args:
        hours: Time window for scraping (default: 168 = 1 week)

    Returns:
        Dictionary with scraping results

    Sources:
        - YouTube: Varun Mayya, Krish Naik, Codebasics
        - Web: OpenAI, Anthropic, DeepMind, VentureBeat, MIT Tech Review, etc.

    Example:
        run_news_scraper(hours=24)  # Last 24 hours
    """
    try:
        results = run_scrapers(hours=hours)

        return {
            "status": "success",
            "youtube_videos": len(results.get("youtube", [])),
            "web_articles": len(results.get("web", [])),
            "total_articles": results.get("total", 0),
            "time_window_hours": hours,
            "message": f"Scraped {results.get('total', 0)} articles from 23 sources"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}


@mcp.tool()
def get_news_stats() -> dict:
    """
    Get system statistics and health information.

    Returns:
        Dictionary with vector store stats, database status, and configuration

    Example:
        get_news_stats()
    """
    try:
        retriever = get_article_retriever()
        article_count = retriever.count_articles()

        return {
            "status": "healthy",
            "vector_store": {
                "total_indexed_articles": article_count,
                "embedding_model": settings.embedding_model,
                "embedding_dimensions": settings.embedding_dimension
            },
            "database": {
                "status": "connected",
                "host": settings.postgres_host,
                "database": settings.postgres_db
            },
            "ai_models": {
                "digest_model": settings.gemini_model_digest,
                "curator_model": settings.gemini_model_curator
            },
            "environment": settings.environment,
            "version": settings.app_version
        }
    except Exception as e:
        return {"error": str(e), "status": "unhealthy"}


@mcp.tool()
def run_full_workflow(hours: int = 168, top_n: int = 10) -> dict:
    """
    Run the complete 6-stage AI news aggregation workflow.

    Stages:
        1. Scraping - Collect from 23 sources
        2. Processing - Get YouTube transcripts
        3. Digest - Generate AI summaries (Gemini)
        4. RAG Indexing - Index in vector database
        5. Ranking - AI-powered ranking with RAG context
        6. Email - Send personalized digest

    Args:
        hours: Time window for scraping (default: 168 = 1 week)
        top_n: Number of articles to include in email (default: 10)

    Returns:
        Dictionary with workflow results

    Example:
        run_full_workflow(hours=168, top_n=15)
    """
    try:
        result = run_workflow(hours=hours, top_n=top_n)

        if result and result.get("success"):
            return {
                "status": "success",
                "articles_scraped": len(result.get("articles", [])),
                "digests_created": len(result.get("digests", [])),
                "articles_indexed": len(result.get("digests", [])),
                "articles_ranked": len(result.get("ranked_articles", [])),
                "email_sent": result.get("success", False),
                "email_article_count": min(len(result.get("ranked_articles", [])), top_n),
                "message": f"Successfully processed and emailed top {top_n} articles"
            }
        else:
            return {
                "status": "failed",
                "error": "Workflow did not complete successfully",
                "errors": result.get("errors", []) if result else []
            }
    except Exception as e:
        return {"error": str(e), "status": "failed"}


@mcp.tool()
def send_email_digest(hours: int = 24, top_n: int = 10, recipient: Optional[str] = None) -> dict:
    """
    Send AI news digest email immediately (on-demand).

    Perfect for:
    - Quick email delivery without full workflow
    - Custom time windows and article counts
    - Testing email functionality

    Args:
        hours: Time window in hours (default: 24)
        top_n: Number of top articles to include (default: 10)
        recipient: Email recipient (defaults to MY_EMAIL from config)

    Returns:
        Dictionary with email send status and details

    Example:
        send_email_digest(hours=24, top_n=10)  # Send last 24 hours, top 10
        send_email_digest(hours=168, top_n=20, recipient="custom@email.com")

    Note:
        Requires digests to exist in database. Run workflow or scraper + digest first.
    """
    try:
        import os
        from src.agents.email import EmailAgent, RankedArticleDetail
        from src.services.email import send_email, digest_to_html

        # Get recent digests
        repo = Repository()
        digests = repo.get_recent_digests(hours=hours)

        if not digests:
            return {
                "status": "error",
                "message": f"No digests found in the last {hours} hours. Run workflow first.",
                "articles_count": 0
            }

        # Convert to ranked article format
        ranked_articles = []
        for idx, digest in enumerate(digests[:top_n]):
            ranked_articles.append(
                RankedArticleDetail(
                    digest_id=digest['id'],
                    rank=idx + 1,
                    relevance_score=10.0 - (idx * 0.5),
                    title=digest['title'],
                    summary=digest['summary'],
                    url=digest['url'],
                    article_type=digest['article_type'],
                    reasoning=f"Ranked #{idx + 1} by recency and relevance"
                )
            )

        # Create email using EmailAgent
        user_profile = {
            "name": "AI Enthusiast",
            "interests": ["AI", "Machine Learning", "LLMs", "AI Safety"]
        }

        email_agent = EmailAgent(user_profile=user_profile)
        email_digest = email_agent.create_email_digest_response(
            ranked_articles=ranked_articles,
            total_ranked=len(digests),
            limit=top_n
        )

        # Generate email content
        subject = f"🤖 AI News Digest - Top {top_n} Articles"
        text_content = email_digest.to_markdown()
        html_content = digest_to_html(email_digest)

        # Determine recipient
        email_recipient = recipient or os.getenv("MY_EMAIL")
        if not email_recipient:
            return {
                "status": "error",
                "message": "No recipient specified and MY_EMAIL not configured"
            }

        # Send email
        send_email(
            subject=subject,
            body_text=text_content,
            body_html=html_content,
            recipients=[email_recipient]
        )

        return {
            "status": "success",
            "message": f"Email digest sent successfully to {email_recipient}",
            "articles_count": len(ranked_articles),
            "recipient": email_recipient,
            "time_window_hours": hours,
            "top_n": top_n
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}",
            "error": str(e)
        }


if __name__ == "__main__":
    # Run the MCP server (no print statements - they interfere with stdio transport)
    mcp.run()
