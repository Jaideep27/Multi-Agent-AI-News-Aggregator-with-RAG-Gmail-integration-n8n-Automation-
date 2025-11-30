"""
LangGraph State Definition

Defines the state that flows through the workflow graph.
"""

from typing import List, Dict, Any, Optional, TypedDict, Annotated
from datetime import datetime
import operator


class Article(TypedDict):
    """Raw scraped article data"""
    id: str
    title: str
    description: str
    url: str
    article_type: str  # youtube, openai, anthropic
    published_at: datetime
    content: Optional[str]


class Digest(TypedDict):
    """AI-generated digest"""
    id: str
    article_id: str
    article_type: str
    title: str
    summary: str
    url: str
    published_at: datetime


class RankedArticle(TypedDict):
    """Ranked article with score"""
    digest_id: str
    rank: int
    relevance_score: float
    reasoning: str
    title: str
    summary: str
    url: str


class ErrorInfo(TypedDict):
    """Error tracking"""
    stage: str
    error_type: str
    message: str
    timestamp: datetime


class WorkflowState(TypedDict):
    """
    State that flows through the LangGraph workflow.

    This state is passed between nodes and can be modified by each node.
    LangGraph automatically manages state transitions and persistence.
    """

    # Configuration
    hours: int  # Time window for scraping (default: 24)
    top_n: int  # Number of articles to send (default: 10)

    # Data at each stage
    articles: Annotated[List[Article], operator.add]  # Raw scraped articles
    digests: Annotated[List[Digest], operator.add]  # AI-generated digests
    ranked_articles: List[RankedArticle]  # Ranked and filtered articles
    email_content: Optional[str]  # Final email HTML

    # RAG context
    vector_indexed: bool  # Whether articles are indexed in vector DB
    similar_articles: List[Dict[str, Any]]  # Historical context for ranking

    # Execution metadata
    errors: Annotated[List[ErrorInfo], operator.add]  # Error tracking
    retry_count: int  # Number of retries
    current_stage: str  # Current workflow stage
    start_time: datetime  # Workflow start time
    end_time: Optional[datetime]  # Workflow end time

    # Flags
    skip_scraping: bool  # Whether to skip scraping (use existing data)
    skip_email: bool  # Whether to skip email sending
    success: bool  # Overall workflow success


def create_initial_state(hours: int = 24, top_n: int = 10) -> WorkflowState:
    """
    Create initial workflow state.

    Args:
        hours: Time window for scraping
        top_n: Number of articles to include

    Returns:
        Initial workflow state
    """
    return WorkflowState(
        hours=hours,
        top_n=top_n,
        articles=[],
        digests=[],
        ranked_articles=[],
        email_content=None,
        vector_indexed=False,
        similar_articles=[],
        errors=[],
        retry_count=0,
        current_stage="initialized",
        start_time=datetime.now(),
        end_time=None,
        skip_scraping=False,
        skip_email=False,
        success=False
    )
