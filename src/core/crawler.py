"""
Crawl4AI wrapper for LLM-friendly web crawling.

Provides async web crawling with clean markdown extraction.
"""

import asyncio
from typing import Optional, Dict, Any
import structlog
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

log = structlog.get_logger()


class WebCrawler:
    """
    Async web crawler using Crawl4AI for LLM-friendly content extraction.

    Features:
    - Clean markdown extraction
    - Async/await support
    - Automatic browser management
    - Caching support
    """

    def __init__(
        self,
        headless: bool = True,
        verbose: bool = False,
        cache_mode: CacheMode = CacheMode.ENABLED
    ):
        """
        Initialize the web crawler.

        Args:
            headless: Run browser in headless mode
            verbose: Enable verbose logging
            cache_mode: Caching strategy (ENABLED, DISABLED, BYPASS)
        """
        self.browser_config = BrowserConfig(
            headless=headless,
            verbose=verbose
        )
        self.cache_mode = cache_mode
        self.log = log.bind(component="crawler")

    async def crawl_to_markdown(
        self,
        url: str,
        wait_for: Optional[str] = None,
        timeout: int = 30000,
        **kwargs
    ) -> Optional[str]:
        """
        Crawl a URL and return clean markdown content.

        Args:
            url: URL to crawl
            wait_for: CSS selector to wait for before extracting content
            timeout: Timeout in milliseconds
            **kwargs: Additional CrawlerRunConfig parameters

        Returns:
            Markdown content or None if crawling fails
        """
        try:
            self.log.info("Crawling URL", url=url)

            # Configure crawler run
            run_config = CrawlerRunConfig(
                cache_mode=self.cache_mode,
                wait_for=wait_for,
                page_timeout=timeout,
                **kwargs
            )

            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=run_config
                )

                if result.success:
                    self.log.info("Successfully crawled URL", url=url, size=len(result.markdown))
                    return result.markdown
                else:
                    self.log.error("Failed to crawl URL", url=url, error=result.error_message)
                    return None

        except Exception as e:
            self.log.error("Crawling exception", url=url, error=str(e))
            return None

    async def crawl_batch(
        self,
        urls: list[str],
        max_concurrent: int = 3,
        **kwargs
    ) -> Dict[str, Optional[str]]:
        """
        Crawl multiple URLs concurrently.

        Args:
            urls: List of URLs to crawl
            max_concurrent: Maximum concurrent crawls
            **kwargs: Additional crawl parameters

        Returns:
            Dictionary mapping URLs to markdown content
        """
        self.log.info("Starting batch crawl", count=len(urls), max_concurrent=max_concurrent)

        results = {}
        semaphore = asyncio.Semaphore(max_concurrent)

        async def crawl_with_semaphore(url: str):
            async with semaphore:
                markdown = await self.crawl_to_markdown(url, **kwargs)
                results[url] = markdown

        # Create tasks for all URLs
        tasks = [crawl_with_semaphore(url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)

        success_count = sum(1 for v in results.values() if v is not None)
        self.log.info("Batch crawl complete", total=len(urls), success=success_count)

        return results


# Synchronous wrapper for easier use
def crawl_url_sync(url: str, **kwargs) -> Optional[str]:
    """
    Synchronous wrapper for crawling a single URL.

    Args:
        url: URL to crawl
        **kwargs: Additional crawler parameters

    Returns:
        Markdown content or None
    """
    crawler = WebCrawler()
    return asyncio.run(crawler.crawl_to_markdown(url, **kwargs))


# Example usage
if __name__ == "__main__":
    async def main():
        crawler = WebCrawler()

        # Single URL
        markdown = await crawler.crawl_to_markdown(
            "https://www.anthropic.com/research/emergent-misalignment-reward-hacking"
        )
        if markdown:
            print(f"Extracted {len(markdown)} characters")
            print(markdown[:500])

        # Batch crawl
        urls = [
            "https://www.anthropic.com/research",
            "https://openai.com/news"
        ]
        results = await crawler.crawl_batch(urls, max_concurrent=2)
        for url, content in results.items():
            print(f"\n{url}: {'Success' if content else 'Failed'}")

    asyncio.run(main())
