# AI News Aggregator with RAG & Multi-Agent System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.55-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5.23-purple.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Automated personalized AI news delivery with 6-stage LangGraph pipeline, RAG-powered semantic search, and multi-agent orchestration.**

---

## 🎯 **Overview**

An intelligent news aggregation system that automatically scrapes **23 AI news sources**, generates AI-powered summaries using **Gemini 2.5 Flash**, indexes content in a **vector database**, ranks articles using **RAG semantic search**, and delivers personalized **top-10 daily digests** via email.

### **Key Features**

- ✅ **6-Stage LangGraph Pipeline** - Production-ready state machine workflow
- ✅ **23 Data Sources** - 3 YouTube channels + 20 web sources (RSS & crawling)
- ✅ **AI-Powered Summarization** - Gemini 2.5 Flash for concise article digests
- ✅ **RAG Semantic Search** - 384-dimensional embeddings with ChromaDB
- ✅ **Intelligent Ranking** - Multi-agent curation based on user preferences
- ✅ **Automated Delivery** - Daily email digests via n8n orchestration
- ✅ **Multi-Interface** - CLI, FastAPI REST API, Streamlit Dashboard
- ✅ **Production Ready** - Docker deployment, PostgreSQL storage, monitoring

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    23 NEWS SOURCES                           │
├──────────────────────────┬──────────────────────────────────┤
│  YouTube (3 channels)    │   Web Sources (20)               │
│  - Varun Mayya           │   - Official Blogs (9)          │
│  - Krish Naik            │   - Research Papers (3)         │
│  - Codebasics            │   - News Sites (5)              │
│                          │   - AI Safety (3)               │
└──────────────────────────┴──────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           │    LANGGRAPH PIPELINE         │
           ├───────────────────────────────┤
           │  1. SCRAPING     (Crawl4AI)  │
           │  2. PROCESSING   (Transcripts)│
           │  3. DIGEST       (Gemini AI) │
           │  4. RAG INDEXING (ChromaDB)  │
           │  5. RANKING      (Multi-Agent)│
           │  6. EMAIL        (SMTP)      │
           └───────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           │   STORAGE & INTERFACES        │
           ├───────────────────────────────┤
           │  PostgreSQL  │  ChromaDB      │
           │  FastAPI     │  Streamlit     │
           │  n8n         │  CLI           │
           └───────────────────────────────┘
```

---

## 📊 **The 6-Stage Pipeline**

### **Stage 1: Scraping** 🌐
- **Sources:** 23 total (3 YouTube + 20 web)
- **Tools:** Crawl4AI for web scraping, feedparser for RSS, YouTube Transcript API
- **Output:** Raw articles with metadata (title, URL, content, timestamp)

### **Stage 2: Processing** 📝
- **YouTube:** Extracts video transcripts
- **Web:** Full article content extraction
- **Storage:** PostgreSQL database

### **Stage 3: Digest Generation** 🤖
- **AI Model:** Google Gemini 2.5 Flash
- **Temperature:** 0.7 (balanced creativity)
- **Output:** AI-generated title + 2-3 sentence summary
- **Agent:** DigestAgent with structured JSON output

### **Stage 4: RAG Indexing** 🔍
- **Embedding Model:** SentenceTransformer (all-MiniLM-L6-v2)
- **Dimensions:** 384-dimensional vectors
- **Vector DB:** ChromaDB with persistent storage
- **Similarity:** Cosine distance metric

### **Stage 5: Ranking** 📊
- **AI Model:** Gemini 2.5 Flash (Temperature 0.3 - deterministic)
- **Method:** RAG-powered semantic search for historical context
- **Scoring:** 0.0-10.0 based on user preferences
- **Agent:** CuratorAgent with multi-criteria evaluation

### **Stage 6: Email Delivery** 📧
- **Selection:** Top 10 ranked articles
- **Format:** Professional HTML email
- **Delivery:** Gmail SMTP
- **Agent:** EmailAgent for personalized content

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- PostgreSQL 16+
- Gmail account (for email delivery)
- Google Gemini API key

### **Installation**

```bash
# Clone repository
git clone https://github.com/Jaideep27/Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-.git
cd Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys and credentials

# Initialize database
python setup_database.py

# Run complete workflow
python cli.py run
```

---

## 💻 **Usage**

### **CLI Interface**

```bash
# Run complete 6-stage workflow
python cli.py run --hours 24 --top-n 10

# Scrape only
python cli.py scrape --hours 48

# View recent digests
python cli.py digests --limit 20

# Semantic search
python cli.py search "RAG systems" --results 10

# System statistics
python cli.py stats
```

### **FastAPI REST API**

```bash
# Start API server
uvicorn main:app --reload

# Access at: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/scrape` - Trigger scraping
- `POST /api/v1/workflow/run` - Run complete pipeline
- `GET /api/v1/digests` - List recent summaries
- `POST /api/v1/search` - Semantic search
- `POST /api/v1/email/send` - Send digest email
- `GET /api/v1/stats` - System statistics
- `GET /api/v1/articles` - Get articles by source

### **Streamlit Dashboard**

```bash
# Start dashboard
streamlit run streamlit_app.py

# Access at: http://localhost:8501
```

**Pages:**
1. **Dashboard** - System overview & statistics
2. **Search** - Semantic search interface
3. **Digests** - View AI-generated summaries
4. **Scrape** - Trigger scraping with options
5. **Workflow** - Run complete pipeline
6. **Email** - Send on-demand digest

---

## 🐳 **Docker Deployment**

```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.production.yml up -d

# Services:
# - PostgreSQL: localhost:5432
# - FastAPI: localhost:8000
# - Streamlit: localhost:8501
# - n8n: localhost:5678
```

---

## 🔧 **Configuration**

### **Environment Variables (.env)**

```bash
# API Keys
GEMINI_API_KEY=your_gemini_api_key

# Email Configuration
MY_EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# AI Models
GEMINI_MODEL_DIGEST=gemini-2.5-flash
GEMINI_MODEL_CURATOR=gemini-2.5-flash
GEMINI_MODEL_EMAIL=gemini-2.5-flash

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Workflow
DEFAULT_HOURS=24
DEFAULT_TOP_N=10
MAX_RETRIES=3
```

### **User Preferences**

Edit `src/config/user_profile.py` to customize:
- Name and background
- Technical interests (LLMs, RAG, agents, etc.)
- Content preferences (practical, research-focused, avoid hype)
- Expertise level

---

## 📁 **Project Structure**

```
latest-aggregator/
├── src/
│   ├── agents/              # AI agents (Digest, Curator, Email)
│   ├── api/                 # FastAPI REST API (8 endpoints)
│   ├── config/              # Settings & user preferences
│   ├── core/                # Runner, crawler, logging, retry
│   ├── database/            # PostgreSQL ORM models
│   ├── rag/                 # RAG system (embeddings, vectorstore)
│   ├── scrapers/            # YouTube & web scrapers
│   ├── services/            # Business logic services
│   └── workflows/           # LangGraph pipeline
├── pages/                   # Streamlit UI pages (6 pages)
├── n8n_workflows/           # Automation workflows
├── cli.py                   # Click CLI interface
├── main.py                  # FastAPI entry point
├── streamlit_app.py         # Streamlit entry point
├── setup_database.py        # Database initialization
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container image
├── docker-compose.production.yml  # Full stack
└── .env.example             # Environment template
```

---

## 🤖 **AI Agents**

### **DigestAgent**
- **Purpose:** Generate concise article summaries
- **Model:** Gemini 2.5 Flash (Temperature 0.7)
- **Output:** JSON with title + 2-3 sentence summary
- **Features:** Structured responses, rate limit handling

### **CuratorAgent**
- **Purpose:** Rank articles based on user preferences
- **Model:** Gemini 2.5 Flash (Temperature 0.3)
- **Scoring:** 0.0-10.0 across multiple criteria:
  - Relevance to interests
  - Technical depth
  - Novelty & significance
  - Expertise alignment
  - Actionability
- **RAG Integration:** Uses historical context for better rankings

### **EmailAgent**
- **Purpose:** Generate personalized email content
- **Model:** Gemini 2.5 Flash (Temperature 0.7)
- **Output:** Greeting + introduction overview
- **Features:** Markdown to HTML conversion, professional styling

---

## 📚 **Data Sources (23 Total)**

### **YouTube Channels (3)**
1. Varun Mayya - AI tutorials
2. Krish Naik - ML/AI education
3. Codebasics - Data science

### **Official AI Blogs (9)**
- OpenAI, Anthropic, Google DeepMind
- Google Research, Meta AI, Hugging Face
- EleutherAI, Stability AI, LAION

### **Research Papers (3)**
- arXiv AI, arXiv ML, Papers With Code

### **AI News Sites (5)**
- VentureBeat, TechCrunch, MIT Tech Review
- The Decoder, Ars Technica

### **AI Safety & Policy (3)**
- Alignment Forum, LessWrong, Center for AI Safety

---

## 🔍 **RAG System**

### **Embedding Model**
- **Model:** `all-MiniLM-L6-v2` (SentenceTransformers)
- **Dimensions:** 384
- **Speed:** ~5ms per sentence
- **Trade-off:** Balanced speed/quality

### **Vector Database**
- **Database:** ChromaDB
- **Storage:** Persistent (`./chroma_db/`)
- **Distance:** Cosine similarity
- **Collection:** `ai_news_articles`

### **Retrieval**
- Semantic search by query
- Find similar articles
- Duplicate detection (95% threshold)
- Historical context for ranking

---

## 🔄 **n8n Automation**

### **Hourly Digest Workflow**
- **Trigger:** Cron (every hour: `0 * * * *`)
- **Action:** POST to `/api/v1/email/send`
- **Parameters:** hours=24, top_n=10
- **File:** `n8n_workflows/hourly_email_digest.json`

**Setup:**
1. Import JSON into n8n
2. Configure API endpoint URL
3. Activate workflow
4. Receive automated digests

---

## 🗄️ **Database Schema**

### **PostgreSQL Tables**

**YouTubeVideo**
- video_id, title, url, channel_id
- published_at, description, transcript
- created_at

**WebArticle**
- guid, source_name, title, url
- description, published_at, category
- content, created_at

**Digest**
- id, article_type, article_id
- url, title, summary
- created_at

---

## 📊 **API Endpoints**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/v1/scrape` | POST | Trigger scraping |
| `/api/v1/workflow/run` | POST | Run pipeline |
| `/api/v1/digests` | GET | List summaries |
| `/api/v1/search` | POST | Semantic search |
| `/api/v1/stats` | GET | Statistics |
| `/api/v1/email/send` | POST | Send digest |
| `/api/v1/articles` | GET | Get articles |

---

## 🧪 **Testing**

```bash
# Run all tests (when implemented)
pytest

# Test API endpoints
pytest tests/api/

# Test scrapers
pytest tests/scrapers/

# Test agents
pytest tests/agents/
```

---

## 📈 **Monitoring & Logging**

### **Structured Logging**
- **Framework:** Structlog
- **Format:** JSON (production) or console (dev)
- **Output:** `logs/app.log`
- **Levels:** DEBUG, INFO, WARNING, ERROR

### **Metrics** (Optional)
- Prometheus client available
- Track: articles scraped, digests created, emails sent

---

## 🔒 **Security**

- ✅ Environment-based secrets (no hardcoded credentials)
- ✅ Pydantic validation on all inputs
- ✅ SQLAlchemy ORM (SQL injection prevention)
- ✅ CORS configuration for API
- ✅ Rate limit handling for Gemini API

---

## 🛠️ **Development**

### **Setup Development Environment**

```bash
# Install dev dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (if available)
pre-commit install

# Run in development mode
export DEBUG=True
python cli.py run
```

### **Code Organization**
- **Modular:** Clear separation of concerns
- **Type Hints:** Full type annotations
- **Docstrings:** Comprehensive documentation
- **Pydantic:** Strong data validation
- **Error Handling:** Comprehensive exception management

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **LangGraph** - State machine orchestration
- **Google Gemini** - AI summarization & ranking
- **ChromaDB** - Vector database
- **Crawl4AI** - Web content extraction
- **FastAPI** - Modern API framework
- **Streamlit** - Interactive dashboard

---

## 📧 **Contact**

**Jaideep Chandrasekharuni**
- Email: jaideepch007@gmail.com
- GitHub: [@Jaideep27](https://github.com/Jaideep27)

**Project Link:** [https://github.com/Jaideep27/Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-](https://github.com/Jaideep27/Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-)

---

## 🎓 **Citation**

If you use this project in your research or work, please cite:

```bibtex
@software{ai_news_aggregator_2025,
  author = {Jaideep Chandrasekharuni},
  title = {AI News Aggregator with RAG and Multi-Agent System},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Jaideep27/Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-}
}
```

---

## ⭐ **Star History**

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ using LangGraph, Gemini AI, ChromaDB, and FastAPI**

[Documentation](#) • [Issues](https://github.com/Jaideep27/Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-/issues) • [Pull Requests](https://github.com/Jaideep27/Multi-Agent-AI-News-Aggregator-with-RAG-Gmail-integration-n8n-Automation-/pulls)

</div>
