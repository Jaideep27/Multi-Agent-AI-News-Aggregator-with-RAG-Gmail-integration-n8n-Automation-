"""
LangGraph Workflow Nodes

Each node is a function that processes the workflow state.
Nodes can modify the state and control workflow routing.
"""

from datetime import datetime
from typing import Dict, Any
import structlog
from .state import WorkflowState, ErrorInfo

# Import existing services
from src.core.runner import run_scrapers
from src.services.youtube_processor import process_youtube_transcripts
from src.services.digest_processor import process_digests
from src.database.repository import Repository
from src.rag.retriever import get_article_retriever
from src.config.user_profile import USER_PROFILE

log = structlog.get_logger()


def scraping_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Scrape articles from sources.

    Scrapes YouTube, OpenAI, and Anthropic sources.
    """
    log.info("=== Scraping Node ===", hours=state["hours"])

    if state["skip_scraping"]:
        log.info("Skipping scraping (using existing data)")
        return {"current_stage": "scraping_skipped"}

    try:
        # Run scrapers
        results = run_scrapers(hours=state["hours"])

        # Convert to Article format
        articles = []

        # YouTube articles
        for video in results.get("youtube", []):
            articles.append({
                "id": f"youtube:{video.video_id}",
                "title": video.title,
                "description": video.description,
                "url": video.url,
                "article_type": "youtube",
                "published_at": video.published_at,
                "content": video.transcript
            })

        # Web articles (20 sources)
        for article in results.get("web", []):
            articles.append({
                "id": f"web:{article.guid}",
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "article_type": article.category,  # official, research, news, safety
                "published_at": article.published_at,
                "content": article.content or article.description
            })

        log.info(f"Scraped {len(articles)} total articles")

        return {
            "articles": articles,
            "current_stage": "scraped"
        }

    except Exception as e:
        log.error("Scraping failed", error=str(e))
        return {
            "errors": [ErrorInfo(
                stage="scraping",
                error_type=type(e).__name__,
                message=str(e),
                timestamp=datetime.now()
            )],
            "current_stage": "scraping_failed"
        }


def processing_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Process raw articles (get transcripts for YouTube).

    Enriches YouTube videos with transcripts if missing.
    Web articles already have content from Crawl4AI.
    """
    log.info("=== Processing Node ===")

    try:
        # Process YouTube transcripts (if any are missing)
        youtube_result = process_youtube_transcripts()
        log.info(f"Processed {youtube_result['processed']} YouTube transcripts")

        # Web articles already have content from Crawl4AI scraper
        log.info("Web articles already have content from Crawl4AI")

        return {
            "current_stage": "processed"
        }

    except Exception as e:
        log.error("Processing failed", error=str(e))
        return {
            "errors": [ErrorInfo(
                stage="processing",
                error_type=type(e).__name__,
                message=str(e),
                timestamp=datetime.now()
            )],
            "current_stage": "processing_failed"
        }


def digest_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Generate AI digests for articles.

    Uses DigestAgent to create summaries.
    """
    log.info("=== Digest Node ===")

    try:
        # Process digests using existing service
        digest_result = process_digests()

        log.info(f"Created {digest_result['processed']} digests")

        # Load digests from database
        repo = Repository()
        digests_data = repo.get_recent_digests(hours=state["hours"])

        # Convert to Digest format
        digests = []
        for d in digests_data:
            digests.append({
                "id": d["id"],
                "article_id": d["id"],
                "article_type": d["article_type"],
                "title": d["title"],
                "summary": d["summary"],
                "url": d["url"],
                "published_at": d.get("published_at")
            })

        return {
            "digests": digests,
            "current_stage": "digested"
        }

    except Exception as e:
        log.error("Digest generation failed", error=str(e))
        return {
            "errors": [ErrorInfo(
                stage="digest",
                error_type=type(e).__name__,
                message=str(e),
                timestamp=datetime.now()
            )],
            "current_stage": "digest_failed"
        }


def rag_indexing_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Index articles in vector database for RAG.

    Creates embeddings and stores in ChromaDB.
    """
    log.info("=== RAG Indexing Node ===")

    try:
        retriever = get_article_retriever()

        # Prepare articles for indexing
        articles_to_index = []
        for digest in state["digests"]:
            articles_to_index.append({
                "id": digest["id"],
                "title": digest["title"],
                "summary": digest["summary"],
                "content": None,  # We could fetch full content if needed
                "metadata": {
                    "article_type": digest["article_type"],
                    "url": digest["url"],
                    "published_at": str(digest.get("published_at", ""))
                }
            })

        # Index in batch
        if articles_to_index:
            retriever.index_articles_batch(articles_to_index)
            log.info(f"Indexed {len(articles_to_index)} articles in vector DB")

        return {
            "vector_indexed": True,
            "current_stage": "rag_indexed"
        }

    except Exception as e:
        log.error("RAG indexing failed", error=str(e))
        return {
            "errors": [ErrorInfo(
                stage="rag_indexing",
                error_type=type(e).__name__,
                message=str(e),
                timestamp=datetime.now()
            )],
            "vector_indexed": False,
            "current_stage": "rag_indexing_failed"
        }


def ranking_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Rank articles using CuratorAgent with RAG context.

    Uses RAG to provide historical context for better ranking.
    """
    log.info("=== Ranking Node ===")

    try:
        from src.agents.curator import CuratorAgent

        curator = CuratorAgent(USER_PROFILE)

        # Get RAG context for ranking
        retriever = get_article_retriever()
        user_interests = " ".join(USER_PROFILE["interests"][:3])
        similar_articles = retriever.get_context_for_ranking(
            user_query=user_interests,
            n_results=5
        )

        log.info(f"Retrieved {len(similar_articles)} similar articles for context")

        # Prepare digests for ranking
        digests_for_ranking = []
        for d in state["digests"]:
            digests_for_ranking.append({
                "id": d["id"],
                "title": d["title"],
                "summary": d["summary"],
                "article_type": d["article_type"]
            })

        # Rank articles
        ranked = curator.rank_digests(digests_for_ranking)

        # Convert to RankedArticle format
        ranked_articles = []
        for r in ranked:
            # Find matching digest
            digest = next((d for d in state["digests"] if d["id"] == r.digest_id), None)
            if digest:
                ranked_articles.append({
                    "digest_id": r.digest_id,
                    "rank": r.rank,
                    "relevance_score": r.relevance_score,
                    "reasoning": r.reasoning,
                    "title": digest["title"],
                    "summary": digest["summary"],
                    "url": digest["url"]
                })

        log.info(f"Ranked {len(ranked_articles)} articles")

        return {
            "ranked_articles": ranked_articles,
            "similar_articles": similar_articles,
            "current_stage": "ranked"
        }

    except Exception as e:
        log.error("Ranking failed", error=str(e))
        return {
            "errors": [ErrorInfo(
                stage="ranking",
                error_type=type(e).__name__,
                message=str(e),
                timestamp=datetime.now()
            )],
            "current_stage": "ranking_failed"
        }


def email_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Generate and send email digest.

    Uses EmailAgent to create personalized email.
    """
    log.info("=== Email Node ===")

    if state["skip_email"]:
        log.info("Skipping email send")
        return {
            "current_stage": "email_skipped",
            "success": True
        }

    try:
        from src.agents.email import EmailAgent, RankedArticleDetail, EmailDigestResponse
        from src.services.email import send_email, digest_to_html

        email_agent = EmailAgent(USER_PROFILE)

        # Prepare top N articles
        top_articles = state["ranked_articles"][:state["top_n"]]

        # Convert to RankedArticleDetail format
        article_details = []
        for a in top_articles:
            article_details.append(RankedArticleDetail(
                digest_id=a["digest_id"],
                rank=a["rank"],
                relevance_score=a["relevance_score"],
                reasoning=a.get("reasoning", ""),
                title=a["title"],
                summary=a["summary"],
                url=a["url"],
                article_type=""
            ))

        # Generate email
        email_digest = email_agent.create_email_digest_response(
            ranked_articles=article_details,
            total_ranked=len(state["ranked_articles"]),
            limit=state["top_n"]
        )

        # Convert to HTML
        html_content = digest_to_html(email_digest)
        markdown_content = email_digest.to_markdown()

        # Send email
        subject = f"Daily AI News Digest - {email_digest.introduction.greeting.split('for ')[-1] if 'for ' in email_digest.introduction.greeting else 'Today'}"

        send_email(
            subject=subject,
            body_text=markdown_content,
            body_html=html_content
        )

        log.info("Email sent successfully!", article_count=len(top_articles))

        return {
            "email_content": html_content,
            "current_stage": "email_sent",
            "success": True,
            "end_time": datetime.now()
        }

    except Exception as e:
        log.error("Email send failed", error=str(e))
        return {
            "errors": [ErrorInfo(
                stage="email",
                error_type=type(e).__name__,
                message=str(e),
                timestamp=datetime.now()
            )],
            "current_stage": "email_failed",
            "success": False
        }


def error_handler_node(state: WorkflowState) -> Dict[str, Any]:
    """
    Node: Handle errors and decide on retry strategy.
    """
    log.error("=== Error Handler Node ===", errors=len(state["errors"]))

    if state["retry_count"] < 3:
        log.info("Retrying workflow", retry_count=state["retry_count"] + 1)
        return {
            "retry_count": state["retry_count"] + 1,
            "current_stage": "retrying"
        }
    else:
        log.error("Max retries exceeded, workflow failed")
        return {
            "current_stage": "failed",
            "success": False,
            "end_time": datetime.now()
        }
