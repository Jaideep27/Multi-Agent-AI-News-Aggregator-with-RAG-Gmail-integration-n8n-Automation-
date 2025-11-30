"""
Base class for all scrapers.

Provides common functionality for scraping news sources.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import List, TypeVar, Generic
import structlog

log = structlog.get_logger()

# Type variable for article type
ArticleType = TypeVar('ArticleType')


class BaseScraper(ABC, Generic[ArticleType]):
    """
    Abstract base class for all scrapers.

    Provides:
    - Common scraping interface
    - Time filtering
    - Error handling
    - Logging
    """

    def __init__(self, source_name: str):
        """
        Initialize the base scraper.

        Args:
            source_name: Name of the news source (e.g., "YouTube", "OpenAI")
        """
        self.source_name = source_name
        self.log = log.bind(scraper=source_name)
        self.log.info("Scraper initialized")

    @abstractmethod
    def get_articles(self, hours: int = 24) -> List[ArticleType]:
        """
        Get articles from the source.

        Must be implemented by subclasses.

        Args:
            hours: Time window in hours (default: 24)

        Returns:
            List of articles
        """
        pass

    def _get_cutoff_time(self, hours: int) -> datetime:
        """
        Calculate cutoff time for filtering articles.

        Args:
            hours: Number of hours to look back

        Returns:
            Cutoff datetime in UTC
        """
        return datetime.now(timezone.utc) - timedelta(hours=hours)

    def _is_recent(self, published_at: datetime, hours: int) -> bool:
        """
        Check if article is within the time window.

        Args:
            published_at: Article publication datetime
            hours: Time window in hours

        Returns:
            True if article is recent enough
        """
        cutoff = self._get_cutoff_time(hours)
        return published_at >= cutoff

    def __repr__(self) -> str:
        """String representation of the scraper."""
        return f"{self.__class__.__name__}(source={self.source_name})"
