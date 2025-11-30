# 🎯 23 AI News Sources - Complete Setup Guide

## 📊 Overview

Your AI News Aggregator now scrapes **23 sources**:
- **3 YouTube Channels**
- **20 Web Sources** (Official blogs, research papers, news sites, safety forums)

---

## 📺 YouTube Channels (3)

| # | Channel | Focus | URL |
|---|---------|-------|-----|
| 1 | **Varun Mayya** | AI tools, entrepreneurship | https://www.youtube.com/@VarunMayya |
| 2 | **Krish Naik** | AI tutorials, ML courses | https://www.youtube.com/@krishnaik06 |
| 3 | **Codebasics** | Data science, Python, AI | https://www.youtube.com/@codebasics |

**What's Scraped:**
- Video titles
- Video descriptions
- Full transcripts (for AI summarization)
- Published dates

---

## 🌐 Web Sources (20)

### 1️⃣ Official AI Company Blogs (9 sources)

| # | Source | What You Get | RSS |
|---|--------|--------------|-----|
| 1 | **OpenAI Blog** | GPT updates, ChatGPT features, research | ✅ |
| 2 | **Anthropic Blog** | Claude updates, safety research | ✅ |
| 3 | **Google DeepMind** | Breakthrough papers, Gemini updates | ✅ |
| 4 | **Google Research** | AI/ML innovation from Google labs | ✅ |
| 5 | **Meta AI** | Llama models, open-source research | ✅ |
| 6 | **Hugging Face** | Model launches, datasets, tools | ✅ |
| 7 | **EleutherAI** | GPT-Neo, open-source research | 🕷️ Crawl |
| 8 | **Stability AI** | Stable Diffusion updates | 🕷️ Crawl |
| 9 | **LAION AI** | Multimodal datasets, research | ✅ |

### 2️⃣ Research Papers (3 sources)

| # | Source | What You Get | RSS |
|---|--------|--------------|-----|
| 10 | **arXiv AI** | Daily AI research papers | ✅ |
| 11 | **arXiv ML** | Machine learning breakthroughs | ✅ |
| 12 | **Papers With Code** | Papers + code + benchmarks | ✅ |

### 3️⃣ AI News & Media (5 sources)

| # | Source | What You Get | RSS |
|---|--------|--------------|-----|
| 13 | **VentureBeat AI** | Industry news, startups, enterprise AI | ✅ |
| 14 | **TechCrunch AI** | AI startups, product launches | ✅ |
| 15 | **MIT Technology Review** | High-quality AI journalism | ✅ |
| 16 | **The Decoder** | Daily AI model updates & comparisons | ✅ |
| 17 | **Ars Technica AI** | Tech science updates | ✅ |

### 4️⃣ AI Safety & Policy (3 sources)

| # | Source | What You Get | RSS |
|---|--------|--------------|-----|
| 18 | **Alignment Forum** | AGI safety discussions | ✅ |
| 19 | **LessWrong AI** | AI ethics, alignment, philosophy | ✅ |
| 20 | **Center for AI Safety** | AI safety research, governance | 🕷️ Crawl |

**Legend:**
- ✅ = RSS Feed (fast, reliable)
- 🕷️ Crawl = Web Crawl with Crawl4AI (LLM-friendly markdown)

---

## 🚀 Setup Instructions

### Step 1: Run Database Setup

The new web_articles table needs to be created:

```bash
# Navigate to project
cd C:\AI\ai-news-aggregator-master\latest-aggregator

# Activate virtual environment
venv\Scripts\activate

# Run database setup
python setup_database.py
```

Expected output:
```
[OK] Database 'ai_news_aggregator' already exists
Creating tables in 'ai_news_aggregator'...
[OK] Tables created successfully

Created tables: youtube_videos, web_articles, digests, ...
```

### Step 2: Test Scraping

Test that all 23 sources are working:

```bash
# Test scrape (no AI processing)
python cli.py scrape --hours 168
```

Expected output:
```
┌─────────┬──────────┐
│ Source  │ Articles │
├─────────┼──────────┤
│ YouTube │ XX       │
│ Web     │ XXX      │
│ TOTAL   │ XXX      │
└─────────┴──────────┘
```

### Step 3: Run Full Workflow

```bash
# Run complete workflow (scrape + AI + email)
python cli.py run --hours 168 --top-n 15
```

This will:
1. ✅ Scrape all 23 sources
2. ✅ Generate AI summaries (Gemini)
3. ✅ Index in vector database (ChromaDB)
4. ✅ Rank articles (personalized for you)
5. ✅ Send email digest

---

## 📊 Understanding the Results

### By Category

Articles are categorized as:
- **official**: Company blogs (OpenAI, Google, Meta, etc.)
- **research**: Academic papers (arXiv, Papers With Code)
- **news**: Tech journalism (TechCrunch, MIT TR)
- **safety**: AI safety & ethics (Alignment Forum, LessWrong)

### By Source

Each article tracks which of the 23 sources it came from:

```python
# Example article
{
    "source_name": "OpenAI Blog",  # Which source
    "category": "official",         # Which category
    "title": "GPT-5 Announcement",
    "url": "https://openai.com/...",
    "content": "Full markdown...",  # From Crawl4AI
}
```

---

## 🧪 Testing Individual Sources

### Test YouTube Scraping

```bash
cd src/scrapers
python youtube.py
```

### Test Web Scraping

```bash
cd src/scrapers
python web_scraper.py
```

Expected output:
```
Testing Unified Web Scraper for 20 AI News Sources
============================================================

✅ Total articles found: XXX

📊 Articles by category:
  official: XX
  research: XX
  news: XX
  safety: XX

📰 Articles by source:
  OpenAI Blog: X
  Anthropic Blog: X
  ... (all 20 sources)
```

### Test Web Sources Configuration

```bash
cd src/config
python web_sources.py
```

Output shows all 20 sources configured:
```
Web Sources Configuration
==================================================
Total sources: 20
  Official blogs: 9
  Research: 3
  News sites: 5
  Safety & Policy: 3

Scrape methods:
  RSS feeds: 17
  Web crawl: 3
```

---

## 🔧 Customization

### Change YouTube Channels

Edit `src/config/settings.py`:

```python
youtube_channels: List[str] = Field(
    default=[
        "UCyR2Ct3pDOeZSRyZH5hPO-Q",  # Varun Mayya
        "UCNU_lfiiWBdtULKOw6X0Dig",  # Krish Naik
        "UCh9nVJoWXmFb7sLApWGcLPQ",  # Codebasics
        "YOUR_CHANNEL_ID",              # Add more
    ]
)
```

### Add/Remove Web Sources

Edit `src/config/web_sources.py`:

```python
# Add a new source
WebSource(
    name="New AI Blog",
    url="https://example.com/blog",
    category="official",
    scrape_type="rss",
    rss_url="https://example.com/feed.xml",
    description="Description here"
)
```

### Change Time Window

```bash
# Last 24 hours (default)
python cli.py run

# Last 7 days
python cli.py run --hours 168

# Last month
python cli.py run --hours 720
```

---

## 📈 Performance

### Scraping Speed

| Source Type | Speed | Notes |
|-------------|-------|-------|
| YouTube (3) | ~10s | RSS + transcript API |
| RSS Feeds (17) | ~30s | Fast, reliable |
| Web Crawl (3) | ~60s | Uses Crawl4AI + Playwright |
| **Total** | **~2 min** | For all 23 sources |

### Database Storage

Approximate sizes per article:
- YouTube: ~5-10 KB (with transcript)
- Web (RSS): ~1-2 KB (description only)
- Web (Crawl): ~10-50 KB (full markdown)

**Total:** ~100 articles/week = ~1 MB

---

## 🐛 Troubleshooting

### Issue: "No web_articles table"

```bash
# Solution: Run database setup
python setup_database.py
```

### Issue: "Browser not found" (for web crawling)

```bash
# Solution: Install Playwright
python -m playwright install --with-deps chromium
```

### Issue: Some sources return 0 articles

**Possible causes:**
1. No articles published in time window
2. RSS feed changed URL
3. Website blocking scrapers

**Solutions:**
```bash
# Try longer time window
python cli.py run --hours 720  # Last month

# Check individual source
cd src/scrapers
python web_scraper.py  # Shows which sources fail
```

### Issue: Scraping is slow

```bash
# Use async mode (faster)
# Edit src/core/runner.py and change:
web_articles = web_scraper.get_all_articles(hours=hours)
# To:
web_articles = await web_scraper.get_all_articles_async(hours=hours)
```

---

## 📊 Database Schema

### New Table: `web_articles`

```sql
CREATE TABLE web_articles (
    guid VARCHAR PRIMARY KEY,
    source_name VARCHAR NOT NULL,  -- One of 20 sources
    title VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    description TEXT,
    published_at TIMESTAMP NOT NULL,
    category VARCHAR NOT NULL,      -- official/research/news/safety
    content TEXT,                   -- Full markdown from Crawl4AI
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Query Examples

```sql
-- Articles by category
SELECT category, COUNT(*)
FROM web_articles
GROUP BY category;

-- Most active sources
SELECT source_name, COUNT(*)
FROM web_articles
GROUP BY source_name
ORDER BY COUNT(*) DESC;

-- Recent research papers
SELECT title, url, published_at
FROM web_articles
WHERE category = 'research'
ORDER BY published_at DESC
LIMIT 10;
```

---

## ✅ Verification Checklist

- [ ] Database setup complete (`python setup_database.py`)
- [ ] YouTube channels configured (3 channels)
- [ ] Web sources verified (20 sources in config)
- [ ] Crawl4AI installed (`crawl4ai-setup`)
- [ ] Test scraping works (`python cli.py scrape --hours 168`)
- [ ] Full workflow runs (`python cli.py run --hours 168`)
- [ ] Email received with articles from all sources

---

## 🎯 Expected Results

After running `python cli.py run --hours 168`:

```
✅ Scraped 23 sources successfully
   YouTube: ~10-30 videos (3 channels)
   Web: ~100-500 articles (20 sources)

✅ Generated AI summaries using Gemini
   Processed: XXX articles

✅ Ranked articles by relevance
   Top 15 selected for email

✅ Email sent successfully
   Check your inbox!
```

---

## 📚 Files Modified

```
✅ src/config/settings.py         - YouTube channels (3)
✅ src/config/web_sources.py      - Web sources (20) NEW
✅ src/scrapers/web_scraper.py    - Unified scraper NEW
✅ src/database/models.py         - WebArticle model NEW
✅ src/database/repository.py     - bulk_create_web_articles() NEW
✅ src/core/runner.py             - Updated to use 23 sources
```

---

**You now have a comprehensive AI news aggregator covering 23 sources!** 🎉

Test it with:
```bash
python cli.py run --hours 168 --top-n 15
```
