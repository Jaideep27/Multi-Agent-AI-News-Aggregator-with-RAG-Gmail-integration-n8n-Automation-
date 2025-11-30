"""Scrapers for AI news sources - YouTube (3 channels) + Web (20 sources)."""

from .base import BaseScraper
from .youtube import YouTubeScraper, ChannelVideo, Transcript
from .web_scraper import UnifiedWebScraper, WebArticle

__all__ = [
    'BaseScraper',
    'YouTubeScraper',
    'ChannelVideo',
    'Transcript',
    'UnifiedWebScraper',
    'WebArticle',
]
