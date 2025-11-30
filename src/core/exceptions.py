"""
Custom exception hierarchy for the AI News Aggregator.
"""


class NewsAggregatorError(Exception):
    """Base exception for all news aggregator errors."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ScrapingError(NewsAggregatorError):
    """Raised when scraping fails."""
    pass


class ProcessingError(NewsAggregatorError):
    """Raised when article processing fails."""
    pass


class DigestError(NewsAggregatorError):
    """Raised when digest generation fails."""
    pass


class RankingError(NewsAggregatorError):
    """Raised when article ranking fails."""
    pass


class RAGError(NewsAggregatorError):
    """Raised when RAG operations fail."""
    pass


class EmbeddingError(RAGError):
    """Raised when embedding generation fails."""
    pass


class VectorStoreError(RAGError):
    """Raised when vector store operations fail."""
    pass


class ConfigurationError(NewsAggregatorError):
    """Raised when configuration is invalid."""
    pass


class DatabaseError(NewsAggregatorError):
    """Raised when database operations fail."""
    pass


class EmailError(NewsAggregatorError):
    """Raised when email sending fails."""
    pass


class WorkflowError(NewsAggregatorError):
    """Raised when workflow execution fails."""
    pass
