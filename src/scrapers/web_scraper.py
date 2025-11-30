"""Unified web scraper for 20 AI news sources."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional
import asyncio
import feedparser
from pydantic import BaseModel
import structlog

from ..core.crawler import WebCrawler
from ..config.web_sources import WebSource, ALL_WEB_SOURCES

log = structlog.get_logger()


class WebArticle(BaseModel):
    """Generic web article model for all 20 sources."""
    source_name: str
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: str  # official, research, news, safety
    content: Optional[str] = None  # Full content from Crawl4AI


class UnifiedWebScraper:
    """
    Unified scraper for all 20 web-based AI news sources.

    Handles both RSS feeds (17 sources) and direct web crawling (3 sources).
    """

    def __init__(self):
        self.crawler = WebCrawler(headless=True, verbose=False)
        self.sources = ALL_WEB_SOURCES
        self.log = log.bind(component="web_scraper")

    def get_articles_from_source(
        self,
        source: WebSource,
        hours: int = 24
    ) -> List[WebArticle]:
        """
        Get articles from a single source.

        Args:
            source: WebSource configuration
            hours: Time window in hours

        Returns:
            List of WebArticle objects
        """
        if source.scrape_type == "rss" and source.rss_url:
            return self._scrape_rss(source, hours)
        elif source.scrape_type == "crawl":
            return self._scrape_web(source, hours)
        return []

    def _scrape_rss(
        self,
        source: WebSource,
        hours: int
    ) -> List[WebArticle]:
        """
        Scrape articles from RSS feed.

        Args:
            source: WebSource configuration
            hours: Time window in hours

        Returns:
            List of WebArticle objects
        """
        try:
            self.log.info("Scraping RSS", source=source.name, url=source.rss_url)
            feed = feedparser.parse(source.rss_url)

            if not feed.entries:
                self.log.warning("No entries found", source=source.name)
                return []

            now = datetime.now(timezone.utc)
            cutoff_time = now - timedelta(hours=hours)
            articles = []

            for entry in feed.entries:
                # Try different date fields
                published_parsed = getattr(entry, "published_parsed", None)
                if not published_parsed:
                    published_parsed = getattr(entry, "updated_parsed", None)

                if not published_parsed:
                    # If no date, use current time (for sources without dates)
                    published_time = now
                else:
                    published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)

                if published_time >= cutoff_time:
                    # Get description/summary
                    description = entry.get("description", "")
                    if not description:
                        description = entry.get("summary", "")

                    # Create article
                    article = WebArticle(
                        source_name=source.name,
                        title=entry.get("title", "No title"),
                        description=description[:1000],  # Limit description length
                        url=entry.get("link", ""),
                        guid=f"{source.name}:{entry.get('id', entry.get('link', str(published_time)))}",
                        published_at=published_time,
                        category=source.category
                    )
                    articles.append(article)

            self.log.info("RSS scrape complete", source=source.name, count=len(articles))
            return articles

        except Exception as e:
            self.log.error("RSS scrape failed", source=source.name, error=str(e))
            return []

    def _scrape_web(
        self,
        source: WebSource,
        hours: int
    ) -> List[WebArticle]:
        """
        Scrape articles directly from website using Crawl4AI.

        For sources without RSS feeds.

        Args:
            source: WebSource configuration
            hours: Time window in hours

        Returns:
            List of WebArticle objects
        """
        try:
            self.log.info("Crawling website", source=source.name, url=source.url)

            # Use Crawl4AI to get clean markdown
            markdown = asyncio.run(
                self.crawler.crawl_to_markdown(source.url, timeout=60000)
            )

            if markdown:
                # Create a single article representing latest content
                article = WebArticle(
                    source_name=source.name,
                    title=f"Latest from {source.name}",
                    description=markdown[:500],  # First 500 chars
                    url=source.url,
                    guid=f"{source.name}:{datetime.now().isoformat()}",
                    published_at=datetime.now(timezone.utc),
                    category=source.category,
                    content=markdown  # Full content
                )

                self.log.info("Web crawl complete", source=source.name, size=len(markdown))
                return [article]

            return []

        except Exception as e:
            self.log.error("Web crawl failed", source=source.name, error=str(e))
            return []

    def get_all_articles(self, hours: int = 24) -> List[WebArticle]:
        """
        Get articles from all 20 configured sources sequentially.

        Args:
            hours: Time window in hours

        Returns:
            List of all WebArticle objects from all sources
        """
        all_articles = []

        self.log.info("Starting scrape of all sources", total_sources=len(self.sources), hours=hours)

        for i, source in enumerate(self.sources, 1):
            try:
                self.log.info(f"Scraping source {i}/{len(self.sources)}", source=source.name)
                articles = self.get_articles_from_source(source, hours)
                all_articles.extend(articles)
                self.log.info(f"Found {len(articles)} articles", source=source.name)
            except Exception as e:
                self.log.error(f"Failed to scrape source", source=source.name, error=str(e))

        self.log.info("Scrape complete", total_articles=len(all_articles))
        return all_articles

    async def get_all_articles_async(self, hours: int = 24) -> List[WebArticle]:
        """
        Get articles from all 20 sources concurrently (faster).

        Args:
            hours: Time window in hours

        Returns:
            List of all WebArticle objects from all sources
        """
        self.log.info("Starting async scrape", total_sources=len(self.sources), hours=hours)

        # Create tasks for all sources
        tasks = [
            self._get_source_async(source, hours)
            for source in self.sources
        ]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect all articles
        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                self.log.error("Async task failed", error=str(result))

        self.log.info("Async scrape complete", total_articles=len(all_articles))
        return all_articles

    async def _get_source_async(
        self,
        source: WebSource,
        hours: int
    ) -> List[WebArticle]:
        """Async wrapper for getting articles from a source."""
        try:
            return self.get_articles_from_source(source, hours)
        except Exception as e:
            self.log.error("Async source scrape failed", source=source.name, error=str(e))
            return []


# Test function
if __name__ == "__main__":
    print("Testing Unified Web Scraper for 20 AI News Sources")
    print("=" * 60)

    scraper = UnifiedWebScraper()

    # Test scraping
    articles = scraper.get_all_articles(hours=168)  # Last week

    print(f"\n✅ Total articles found: {len(articles)}")

    # Group by category
    by_category = {}
    by_source = {}

    for article in articles:
        # By category
        cat = article.category
        by_category[cat] = by_category.get(cat, 0) + 1

        # By source
        src = article.source_name
        by_source[src] = by_source.get(src, 0) + 1

    print("\n📊 Articles by category:")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count}")

    print("\n📰 Articles by source:")
    for src, count in sorted(by_source.items(), key=lambda x: x[1], reverse=True):
        print(f"  {src}: {count}")

    # Show sample articles
    print("\n📄 Sample articles (first 3):")
    for i, article in enumerate(articles[:3], 1):
        print(f"\n{i}. {article.title}")
        print(f"   Source: {article.source_name} ({article.category})")
        print(f"   URL: {article.url}")
        print(f"   Published: {article.published_at}")
