# 🤖 AI News Aggregator

An intelligent news aggregation system powered by **Google Gemini AI**, **LangGraph**, and **RAG (Retrieval-Augmented Generation)**. Automatically scrapes, summarizes, ranks, and delivers personalized AI news digests to your inbox.

## ✨ Features

- **Multi-Source Scraping**: YouTube videos, OpenAI blog, Anthropic blog
- **AI-Powered Summaries**: Gemini 2.5 Flash generates concise digests
- **RAG-Based Ranking**: Semantic search using ChromaDB vector database
- **Personalized Curation**: Ranks articles based on your interests
- **Email Delivery**: Beautiful HTML email digests
- **LangGraph Workflows**: State machine orchestration with error handling
- **CLI Interface**: Rich terminal UI with Click

## 🏗️ Architecture

```
├── src/
│   ├── agents/         # AI agents (digest, curator, email)
│   ├── config/         # Configuration & settings
│   ├── core/           # Core utilities
│   ├── database/       # PostgreSQL models & repository
│   ├── rag/            # RAG system (embeddings, vector store)
│   ├── scrapers/       # Source scrapers (YouTube, OpenAI, Anthropic)
│   ├── services/       # Business logic
│   └── workflows/      # LangGraph workflows
├── cli.py              # CLI entry point
├── setup_database.py   # Database setup script
├── requirements.txt    # Python dependencies
└── .env               # Environment configuration
```

## 📋 Prerequisites

- **Python 3.12+**
- **PostgreSQL 16+**
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))
- **Gmail Account** (for sending emails)

## 🚀 Quick Start

### 1. Clone & Navigate

```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your credentials:
# - GEMINI_API_KEY (required)
# - MY_EMAIL (required)
# - APP_PASSWORD (Gmail app password - required)
# - PostgreSQL credentials (if different from defaults)
```

**Getting Gmail App Password:**
1. Go to [Google Account Settings](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication
3. Go to "App Passwords"
4. Generate password for "Mail"
5. Copy to `APP_PASSWORD` in `.env`

### 5. Setup PostgreSQL Database

**Option A: Using Docker**
```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
```

**Option B: Local Installation**
- Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
- Ensure it's running on `localhost:5432`

### 6. Initialize Database

```bash
python setup_database.py
```

Expected output:
```
============================================================
AI News Aggregator - Database Setup
============================================================
Connecting to PostgreSQL at localhost:5432...
[OK] Database 'ai_news_aggregator' created successfully

Creating tables in 'ai_news_aggregator'...
[OK] Tables created successfully

Created tables: youtube_videos, openai_articles, anthropic_articles, digests

============================================================
[SUCCESS] Database setup complete!
============================================================
```

### 7. Run the Aggregator

```bash
# Run complete workflow (scrape, process, rank, email)
python cli.py run

# Or with custom options:
python cli.py run --hours 48 --top-n 5
```

## 📚 CLI Commands

```bash
# Main workflow
python cli.py run                    # Run complete workflow
python cli.py run --hours 24        # Last 24 hours
python cli.py run --top-n 10        # Top 10 articles
python cli.py run --skip-email      # Skip email delivery

# Scraping only
python cli.py scrape                # Scrape without AI processing
python cli.py scrape --hours 48     # Last 48 hours

# View digests
python cli.py digests               # List recent digests
python cli.py digests --limit 20    # Limit results

# Semantic search
python cli.py search "RAG systems"  # Search by query
python cli.py search "LLMs" --results 10

# System info
python cli.py stats                 # System statistics
python cli.py config                # Show configuration
```

## ⚙️ Configuration

### Edit User Profile

Edit `src/config/user_profile.py` to customize your interests:

```python
USER_PROFILE = {
    "name": "Your Name",
    "background": "Your background",
    "interests": [
        "Large Language Models",
        "RAG systems",
        "AI agents",
        # ... add your interests
    ],
    "expertise_level": "Advanced"  # Beginner, Intermediate, Advanced
}
```

### Add YouTube Channels

Edit `src/config/settings.py`:

```python
youtube_channels: List[str] = Field(
    default=[
        "UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
        "YOUR_CHANNEL_ID",             # Add more
    ]
)
```

**Find YouTube Channel ID:**
1. Go to channel page
2. Click "About" tab
3. Click "Share channel"
4. Copy the ID from URL

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **AI/ML** | Google Gemini 2.5 Flash, Sentence Transformers |
| **Orchestration** | LangGraph, LangChain |
| **Databases** | PostgreSQL, ChromaDB (vector DB) |
| **Web Scraping** | BeautifulSoup4, Feedparser, Docling |
| **CLI** | Click, Rich |
| **Logging** | Structlog |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |

## 📊 How It Works

1. **Scraping**: Fetches articles from YouTube, OpenAI, Anthropic
2. **Processing**: Extracts transcripts and markdown content
3. **Digest Generation**: Gemini creates AI summaries
4. **RAG Indexing**: Embeds articles into ChromaDB vector store
5. **Ranking**: AI ranks articles based on your profile + RAG context
6. **Email**: Sends personalized HTML digest

## 🔧 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
# Windows:
services.msc  # Look for "postgresql"

# macOS/Linux:
sudo systemctl status postgresql

# Or check if port is listening:
netstat -an | findstr 5432
```

### Import Errors

```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### ChromaDB Errors

```bash
# Delete and recreate ChromaDB
rm -rf chroma_db  # macOS/Linux
rmdir /s chroma_db  # Windows
```

### Email Not Sending

1. Check Gmail app password is correct
2. Ensure 2FA is enabled on Google Account
3. Check `MY_EMAIL` and `APP_PASSWORD` in `.env`

## 📖 Project Structure Details

```
latest-aggregator/
├── src/
│   ├── agents/
│   │   ├── base.py          # Base agent class
│   │   ├── digest.py        # Digest generation
│   │   ├── curator.py       # Article ranking
│   │   └── email.py         # Email generation
│   ├── config/
│   │   ├── settings.py      # Pydantic settings
│   │   └── user_profile.py  # User preferences
│   ├── core/
│   │   ├── enums.py         # Enumerations
│   │   ├── exceptions.py    # Custom exceptions
│   │   ├── logging.py       # Logging config
│   │   └── runner.py        # Scraper orchestration
│   ├── database/
│   │   ├── connection.py    # DB connection
│   │   ├── models.py        # SQLAlchemy models
│   │   └── repository.py    # Data access layer
│   ├── rag/
│   │   ├── embeddings.py    # Embedding generation
│   │   ├── vectorstore.py   # ChromaDB interface
│   │   └── retriever.py     # RAG retrieval
│   ├── scrapers/
│   │   ├── base.py          # Base scraper
│   │   ├── youtube.py       # YouTube scraper
│   │   ├── openai.py        # OpenAI blog scraper
│   │   └── anthropic.py     # Anthropic blog scraper
│   ├── services/
│   │   ├── email.py         # Email service
│   │   ├── digest_processor.py
│   │   ├── anthropic_processor.py
│   │   └── youtube_processor.py
│   └── workflows/
│       ├── state.py         # LangGraph state
│       ├── nodes.py         # Workflow nodes
│       └── workflow.py      # Workflow definition
├── cli.py                   # CLI interface
├── setup_database.py        # Database setup
├── requirements.txt         # Dependencies
├── .env.example             # Example config
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📝 License

MIT License - feel free to use for personal or commercial projects

## 🎯 Next Steps

After setup, you can:

1. **Customize user profile** in `src/config/user_profile.py`
2. **Add more YouTube channels** in `src/config/settings.py`
3. **Create custom scrapers** for other sources
4. **Schedule daily runs** using cron/Task Scheduler
5. **Deploy to cloud** (AWS, GCP, Azure)

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review error logs in `logs/app.log`
- Check database with `python cli.py stats`

---

**Built with ❤️ using Google Gemini, LangGraph, and Python**
