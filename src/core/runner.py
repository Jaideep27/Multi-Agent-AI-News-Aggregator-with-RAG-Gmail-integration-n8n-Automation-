"""
Scraper orchestration - runs all 23 sources.

3 YouTube channels + 20 web sources = 23 total sources
"""

from typing import List, Dict
import structlog
from src.config.settings import Settings, get_settings
from src.scrapers.youtube import YouTubeScraper, ChannelVideo
from src.scrapers.web_scraper import UnifiedWebScraper, WebArticle
from src.database.repository import Repository

log = structlog.get_logger()


def run_scrapers(hours: int = 24) -> Dict:
    """
    Run all 23 scrapers (3 YouTube + 20 Web).

    Args:
        hours: Time window in hours

    Returns:
        Dictionary with scraped data from all sources
    """
    settings = get_settings()
    repo = Repository()

    log.info("Starting scraper orchestration", total_sources=23, hours=hours)

    # ========================================
    # 1. YouTube (3 channels)
    # ========================================
    log.info("Scraping YouTube channels", count=len(settings.youtube_channels))
    youtube_scraper = YouTubeScraper()
    youtube_videos = []
    video_dicts = []

    for i, channel_id in enumerate(settings.youtube_channels, 1):
        try:
            log.info(f"Scraping YouTube channel {i}/{len(settings.youtube_channels)}", channel_id=channel_id)
            videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)
            youtube_videos.extend(videos)

            # Convert to dict format for database
            video_dicts.extend([
                {
                    "video_id": v.video_id,
                    "title": v.title,
                    "url": v.url,
                    "channel_id": channel_id,
                    "published_at": v.published_at,
                    "description": v.description,
                    "transcript": v.transcript
                }
                for v in videos
            ])

            log.info(f"Found {len(videos)} videos", channel_id=channel_id)
        except Exception as e:
            log.error("YouTube channel scrape failed", channel_id=channel_id, error=str(e))

    # Save YouTube videos to database
    if video_dicts:
        repo.bulk_create_youtube_videos(video_dicts)
        log.info("Saved YouTube videos to database", count=len(video_dicts))

    # ========================================
    # 2. Web Sources (20 sources)
    # ========================================
    log.info("Scraping web sources", count=20)
    web_scraper = UnifiedWebScraper()
    web_articles = []

    try:
        web_articles = web_scraper.get_all_articles(hours=hours)
        log.info("Web scraping complete", count=len(web_articles))

        # Save web articles to database
        if web_articles:
            article_dicts = [
                {
                    "source_name": a.source_name,
                    "guid": a.guid,
                    "title": a.title,
                    "url": a.url,
                    "published_at": a.published_at,
                    "description": a.description,
                    "category": a.category,
                    "content": a.content
                }
                for a in web_articles
            ]
            repo.bulk_create_web_articles(article_dicts)
            log.info("Saved web articles to database", count=len(article_dicts))

    except Exception as e:
        log.error("Web scraping failed", error=str(e))

    # ========================================
    # Summary
    # ========================================
    total_articles = len(youtube_videos) + len(web_articles)
    log.info("Scraping complete",
             youtube=len(youtube_videos),
             web=len(web_articles),
             total=total_articles)

    return {
        "youtube": youtube_videos,
        "web": web_articles,
        "total": total_articles
    }


if __name__ == "__main__":
    print("AI News Aggregator - Scraper Test")
    print("=" * 60)
    print("Sources: 3 YouTube channels + 20 web sources = 23 total")
    print("=" * 60)

    results = run_scrapers(hours=168)  # Last week

    print(f"\n✅ Scraping Results:")
    print(f"   YouTube videos: {len(results['youtube'])}")
    print(f"   Web articles: {len(results['web'])}")
    print(f"   Total articles: {results['total']}")

    # Show breakdown by web source category
    if results['web']:
        by_category = {}
        for article in results['web']:
            cat = article.category
            by_category[cat] = by_category.get(cat, 0) + 1

        print(f"\n📊 Web articles by category:")
        for cat, count in sorted(by_category.items()):
            print(f"   {cat}: {count}")
