"""Configuration for web-based AI news sources (20 sources)."""

from typing import List, Optional
from pydantic import BaseModel


class WebSource(BaseModel):
    """Configuration for a web news source."""
    name: str
    url: str
    category: str  # "official", "research", "news", "safety"
    scrape_type: str  # "rss" or "crawl"
    rss_url: Optional[str] = None
    description: str


# 1-8: Official AI Company Blogs
OFFICIAL_SOURCES = [
    WebSource(
        name="OpenAI Blog",
        url="https://openai.com/blog",
        category="official",
        scrape_type="rss",
        rss_url="https://openai.com/news/rss.xml",
        description="Official OpenAI updates about GPT, ChatGPT, Sora"
    ),
    WebSource(
        name="Anthropic Blog",
        url="https://www.anthropic.com/news",
        category="official",
        scrape_type="rss",
        rss_url="https://www.anthropic.com/news/rss",
        description="Latest about Claude, safety research"
    ),
    WebSource(
        name="Google DeepMind",
        url="https://deepmind.google/",
        category="official",
        scrape_type="rss",
        rss_url="https://deepmind.google/discover/blog/rss.xml",
        description="Breakthrough papers, Gemini updates, AGI research"
    ),
    WebSource(
        name="Google Research",
        url="https://research.google/",
        category="official",
        scrape_type="rss",
        rss_url="https://research.google/blog/rss/",
        description="General AI + ML innovation from Google labs"
    ),
    WebSource(
        name="Meta AI",
        url="https://ai.meta.com/",
        category="official",
        scrape_type="rss",
        rss_url="https://ai.meta.com/blog/rss/",
        description="Open-source LLMs like Llama, research papers"
    ),
    WebSource(
        name="Hugging Face",
        url="https://huggingface.co/blog",
        category="official",
        scrape_type="rss",
        rss_url="https://huggingface.co/blog/feed.xml",
        description="Open-source model launches, transformers, datasets"
    ),
    WebSource(
        name="EleutherAI",
        url="https://www.eleuther.ai/",
        category="official",
        scrape_type="crawl",
        description="Community behind GPT-Neo, open-source research"
    ),
    WebSource(
        name="Stability AI",
        url="https://stability.ai/news",
        category="official",
        scrape_type="crawl",
        description="Stable Diffusion updates, image/video models"
    ),
    WebSource(
        name="LAION AI",
        url="https://laion.ai/blog/",
        category="official",
        scrape_type="rss",
        rss_url="https://laion.ai/blog/feed/",
        description="Open-source multimodal datasets + research"
    ),
]

# 9-11: Research Papers & Preprint Servers
RESEARCH_SOURCES = [
    WebSource(
        name="arXiv AI",
        url="https://arxiv.org/list/cs.AI/recent",
        category="research",
        scrape_type="rss",
        rss_url="http://export.arxiv.org/rss/cs.AI",
        description="Daily new AI research papers"
    ),
    WebSource(
        name="arXiv ML",
        url="https://arxiv.org/list/cs.LG/recent",
        category="research",
        scrape_type="rss",
        rss_url="http://export.arxiv.org/rss/cs.LG",
        description="Machine learning breakthroughs"
    ),
    WebSource(
        name="Papers With Code",
        url="https://paperswithcode.com/",
        category="research",
        scrape_type="rss",
        rss_url="https://paperswithcode.com/feeds/latest/",
        description="Top papers + code implementations + benchmarks"
    ),
]

# 12-16: AI News & Media
NEWS_SOURCES = [
    WebSource(
        name="VentureBeat AI",
        url="https://venturebeat.com/category/ai/",
        category="news",
        scrape_type="rss",
        rss_url="https://venturebeat.com/category/ai/feed/",
        description="Industry-level AI news, startups, enterprise AI"
    ),
    WebSource(
        name="TechCrunch AI",
        url="https://techcrunch.com/tag/artificial-intelligence/",
        category="news",
        scrape_type="rss",
        rss_url="https://techcrunch.com/tag/artificial-intelligence/feed/",
        description="AI startups, tools, product updates"
    ),
    WebSource(
        name="MIT Technology Review",
        url="https://www.technologyreview.com/topic/artificial-intelligence/",
        category="news",
        scrape_type="rss",
        rss_url="https://www.technologyreview.com/topic/artificial-intelligence/feed",
        description="High-quality journalism on AI trends & ethics"
    ),
    WebSource(
        name="The Decoder",
        url="https://the-decoder.com/",
        category="news",
        scrape_type="rss",
        rss_url="https://the-decoder.com/feed/",
        description="Daily AI model updates & comparisons"
    ),
    WebSource(
        name="Ars Technica AI",
        url="https://arstechnica.com/information-technology/",
        category="news",
        scrape_type="rss",
        rss_url="https://arstechnica.com/feed/category/information-technology/",
        description="AI + tech science updates"
    ),
]

# 17-20: AI Safety, Alignment & Policy
SAFETY_SOURCES = [
    WebSource(
        name="Alignment Forum",
        url="https://www.alignmentforum.org/",
        category="safety",
        scrape_type="rss",
        rss_url="https://www.alignmentforum.org/feed.xml",
        description="Deep discussions on AGI safety & research"
    ),
    WebSource(
        name="LessWrong AI",
        url="https://www.lesswrong.com/tag/artificial-intelligence",
        category="safety",
        scrape_type="rss",
        rss_url="https://www.lesswrong.com/feed.xml?view=community-rss&karmaThreshold=30",
        description="AI ethics, alignment, philosophy of AI"
    ),
    WebSource(
        name="Center for AI Safety",
        url="https://safe.ai/",
        category="safety",
        scrape_type="crawl",
        description="Research on AI safety, governance, risk studies"
    ),
]

# All 20 web sources combined
ALL_WEB_SOURCES = (
    OFFICIAL_SOURCES +    # 9 sources
    RESEARCH_SOURCES +    # 3 sources
    NEWS_SOURCES +        # 5 sources
    SAFETY_SOURCES        # 3 sources
)  # Total: 20 sources


# Summary statistics
def get_sources_summary():
    """Get summary of configured sources."""
    return {
        "total": len(ALL_WEB_SOURCES),
        "official": len(OFFICIAL_SOURCES),
        "research": len(RESEARCH_SOURCES),
        "news": len(NEWS_SOURCES),
        "safety": len(SAFETY_SOURCES),
        "rss": sum(1 for s in ALL_WEB_SOURCES if s.scrape_type == "rss"),
        "crawl": sum(1 for s in ALL_WEB_SOURCES if s.scrape_type == "crawl"),
    }


if __name__ == "__main__":
    summary = get_sources_summary()
    print("Web Sources Configuration")
    print("=" * 50)
    print(f"Total sources: {summary['total']}")
    print(f"  Official blogs: {summary['official']}")
    print(f"  Research: {summary['research']}")
    print(f"  News sites: {summary['news']}")
    print(f"  Safety & Policy: {summary['safety']}")
    print(f"\nScrape methods:")
    print(f"  RSS feeds: {summary['rss']}")
    print(f"  Web crawl: {summary['crawl']}")
    print("\nAll sources:")
    for i, source in enumerate(ALL_WEB_SOURCES, 1):
        print(f"  {i}. {source.name} ({source.scrape_type})")
