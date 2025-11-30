from datetime import datetime, timedelta, timezone
from typing import List, Optional
import asyncio
import feedparser
from pydantic import BaseModel

from ..core.crawler import WebCrawler


class GoogleAIArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class GoogleAIScraper:
    def __init__(self):
        self.rss_url = "https://blog.google/technology/ai/rss/"
        self.crawler = WebCrawler(headless=True, verbose=False)

    def get_articles(self, hours: int = 24) -> List[GoogleAIArticle]:
        """
        Get articles from Google AI blog RSS feed.

        Args:
            hours: Time window to filter articles (default: 24 hours)

        Returns:
            List of GoogleAIArticle objects
        """
        feed = feedparser.parse(self.rss_url)
        if not feed.entries:
            return []

        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=hours)
        articles = []

        for entry in feed.entries:
            published_parsed = getattr(entry, "published_parsed", None)
            if not published_parsed:
                continue

            published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
            if published_time >= cutoff_time:
                articles.append(GoogleAIArticle(
                    title=entry.get("title", ""),
                    description=entry.get("description", ""),
                    url=entry.get("link", ""),
                    guid=entry.get("id", entry.get("link", "")),
                    published_at=published_time,
                    category=entry.get("tags", [{}])[0].get("term") if entry.get("tags") else None
                ))

        return articles

    def url_to_markdown(self, url: str) -> Optional[str]:
        """
        Convert URL to markdown using Crawl4AI.

        Args:
            url: URL to convert

        Returns:
            Markdown content or None if conversion fails
        """
        try:
            # Run async crawler in sync context
            return asyncio.run(self.crawler.crawl_to_markdown(url, timeout=60000))
        except Exception as e:
            print(f"Error converting URL to markdown: {e}")
            return None

    async def url_to_markdown_async(self, url: str) -> Optional[str]:
        """
        Async version of url_to_markdown.

        Args:
            url: URL to convert

        Returns:
            Markdown content or None if conversion fails
        """
        try:
            return await self.crawler.crawl_to_markdown(url, timeout=60000)
        except Exception as e:
            print(f"Error converting URL to markdown: {e}")
            return None


if __name__ == "__main__":
    scraper = GoogleAIScraper()
    articles = scraper.get_articles(hours=168)  # Last week
    print(f"Found {len(articles)} articles")
    for article in articles[:5]:
        print(f"- {article.title}")
