"""
Enumerations for type safety and consistency.
"""

from enum import Enum, auto


class ArticleType(str, Enum):
    """Article source types."""
    YOUTUBE = "youtube"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class WorkflowStage(str, Enum):
    """LangGraph workflow stages."""
    INITIALIZED = "initialized"
    SCRAPING = "scraping"
    SCRAPED = "scraped"
    SCRAPING_FAILED = "scraping_failed"
    SCRAPING_SKIPPED = "scraping_skipped"
    PROCESSING = "processing"
    PROCESSED = "processed"
    PROCESSING_FAILED = "processing_failed"
    DIGESTING = "digesting"
    DIGESTED = "digested"
    DIGEST_FAILED = "digest_failed"
    RAG_INDEXING = "rag_indexing"
    RAG_INDEXED = "rag_indexed"
    RAG_INDEXING_FAILED = "rag_indexing_failed"
    RANKING = "ranking"
    RANKED = "ranked"
    RANKING_FAILED = "ranking_failed"
    EMAIL_SENDING = "email_sending"
    EMAIL_SENT = "email_sent"
    EMAIL_FAILED = "email_failed"
    EMAIL_SKIPPED = "email_skipped"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EmbeddingModel(str, Enum):
    """Supported embedding models."""
    MINILM_L6_V2 = "all-MiniLM-L6-v2"
    MPNET_BASE_V2 = "all-mpnet-base-v2"
    DISTILBERT = "distilbert-base-nli-mean-tokens"


class GeminiModel(str, Enum):
    """Supported Gemini models."""
    FLASH_2_5 = "gemini-2.5-flash"
    FLASH_2_0_EXP = "gemini-2.0-flash-exp"
    PRO_2_0 = "gemini-2.0-pro"


class DatabaseTable(str, Enum):
    """Database table names."""
    YOUTUBE_VIDEOS = "youtube_videos"
    OPENAI_ARTICLES = "openai_articles"
    ANTHROPIC_ARTICLES = "anthropic_articles"
    DIGESTS = "digests"
