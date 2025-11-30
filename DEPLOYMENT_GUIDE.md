# 🚀 Professional Deployment Guide - AI News Aggregator

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Service Details](#service-details)
6. [Email Automation](#email-automation)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This AI News Aggregator is a **professional-grade, fully-integrated system** with:

- **FastAPI** - REST API for programmatic access
- **Streamlit** - Modern web UI for manual operations
- **n8n** - Workflow automation for scheduled emails
- **FastMCP** - AI assistant integration (Claude Desktop)
- **PostgreSQL** - Relational database
- **ChromaDB** - Vector database for RAG
- **Docker** - Containerized deployment

### Key Features

✅ **Hourly Email Automation** - n8n sends emails every hour
✅ **On-Demand Emails** - Send immediately via Streamlit UI button
✅ **REST API** - External integrations via FastAPI
✅ **AI Assistant** - Query via Claude Desktop with MCP
✅ **23 News Sources** - 3 YouTube + 20 web sources
✅ **AI-Powered** - Gemini for summaries, RAG for search

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  USER INTERFACES                                        │
│                                                         │
│  👤 Streamlit UI     http://localhost:8501              │
│     ├─ Dashboard                                        │
│     ├─ Search (RAG)                                     │
│     ├─ Digests                                          │
│     ├─ Scrape                                           │
│     ├─ Workflow                                         │
│     └─ 📧 Email (NEW - Send Now button)                │
│                                                         │
│  🤖 Claude Desktop   (via FastMCP)                      │
│     └─ Conversational access to news                    │
│                                                         │
│  🔄 n8n Automation   http://localhost:5678              │
│     └─ Hourly email automation                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  API LAYER                                              │
│                                                         │
│  🌐 FastAPI          http://localhost:8000              │
│     ├─ GET  /health                                     │
│     ├─ POST /api/v1/scrape                              │
│     ├─ POST /api/v1/workflow/run                        │
│     ├─ POST /api/v1/email/send        ⭐ NEW            │
│     ├─ GET  /api/v1/digests                             │
│     ├─ POST /api/v1/search                              │
│     ├─ GET  /api/v1/stats                               │
│     └─ GET  /api/v1/articles                            │
│                                                         │
│  🔌 FastMCP          (stdio protocol)                   │
│     ├─ search_ai_news()                                 │
│     ├─ get_latest_digests()                             │
│     ├─ run_news_scraper()                               │
│     ├─ get_news_stats()                                 │
│     ├─ run_full_workflow()                              │
│     └─ send_email_digest()            ⭐ NEW            │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  CORE SYSTEM                                            │
│                                                         │
│  📊 PostgreSQL       Port 5432                          │
│     └─ youtube_videos, web_articles, digests           │
│                                                         │
│  🗄️  ChromaDB         ./chromadb_data                   │
│     └─ Vector embeddings for RAG search                │
│                                                         │
│  🤖 Gemini AI        (Cloud API)                        │
│     └─ Summaries, ranking, email generation            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

### Option 1: Docker (Recommended for Production)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 2. Start all services
docker compose -f docker-compose.production.yml up -d

# 3. Access services
# - Streamlit: http://localhost:8501
# - FastAPI:   http://localhost:8000/docs
# - n8n:       http://localhost:5678

# 4. Import n8n workflow
# Go to http://localhost:5678
# Import: n8n_workflows/hourly_email_digest.json
# Activate workflow
```

### Option 2: Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start PostgreSQL (Docker)
docker compose up -d postgres

# 3. Initialize database
python setup_database.py

# 4. Start services (separate terminals)

# Terminal 1: FastAPI
python main.py          # Port 8000

# Terminal 2: Streamlit
streamlit run streamlit_app.py  # Port 8501

# Terminal 3: n8n (optional)
n8n start               # Port 5678
```

---

## 📝 Detailed Setup

### Step 1: Environment Configuration

Create `.env` file:

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_news
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Email (Gmail)
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your_gmail_app_password

# SMTP Settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_USE_TLS=True

# Application
APP_NAME=AI News Aggregator
APP_VERSION=2.0.0
ENVIRONMENT=production
DEBUG=False
```

**Gmail Setup:**
1. Enable 2FA on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character app password (not your regular password)

### Step 2: Database Setup

```bash
# Start PostgreSQL
docker compose up -d postgres

# Wait for healthy status
docker compose ps

# Initialize schema
python setup_database.py

# Verify
python cli.py --help
```

### Step 3: Test Core Functionality

```bash
# Run workflow to generate initial data
python cli.py run --hours 168 --top-n 10

# Expected output:
# ✓ Articles Scraped: ~50-100
# ✓ Digests Created: ~50-100
# ✓ Articles Ranked: 10
# ✓ Email Sent: ✓
```

### Step 4: Start FastAPI

```bash
python main.py

# Verify:
# - Visit http://localhost:8000/docs
# - Try GET /health endpoint
# - Should return {"status": "healthy", ...}
```

### Step 5: Start Streamlit

```bash
streamlit run streamlit_app.py

# Access http://localhost:8501
# Navigate to:
# - 🏠 Dashboard (see stats)
# - 📧 Email (NEW - send email now button)
```

### Step 6: Configure n8n

```bash
# Start n8n
n8n start

# Access http://localhost:5678
# 1. Create account (first time)
# 2. Import workflow: n8n_workflows/hourly_email_digest.json
# 3. Activate workflow (toggle switch)
# 4. Test: Click "Execute Workflow"
```

### Step 7: Test Email Sending

**Option A: Streamlit UI**
1. Go to http://localhost:8501
2. Click "📧 Email" in sidebar
3. Configure parameters (hours, top_n)
4. Click "📧 Send Email Now"
5. Check your email inbox!

**Option B: FastAPI**
```bash
curl -X POST http://localhost:8000/api/v1/email/send \
  -H "Content-Type: application/json" \
  -d '{"hours": 24, "top_n": 10}'
```

**Option C: n8n**
- Workflow runs automatically every hour
- Check n8n execution history

---

## 🔧 Service Details

### 1. FastAPI (Port 8000)

**Purpose:** REST API for external access

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/email/send` ⭐ **NEW** - Send email on-demand
- `POST /api/v1/workflow/run` - Run complete workflow
- `GET /api/v1/digests` - Get recent summaries
- `POST /api/v1/search` - Semantic search
- `GET /api/v1/stats` - System statistics

**Start:**
```bash
python main.py
# or
uvicorn main:app --reload
```

**Swagger UI:** http://localhost:8000/docs

### 2. Streamlit (Port 8501)

**Purpose:** User-friendly web interface

**Pages:**
- 🏠 Dashboard - Overview and stats
- 🔍 Search - RAG semantic search
- 📰 Digests - Browse summaries
- 🕷️ Scrape - Trigger scraping
- 🚀 Workflow - Run complete pipeline
- 📧 Email ⭐ **NEW** - Send email now button
- ⚙️ Settings - Configuration

**Start:**
```bash
streamlit run streamlit_app.py
```

**Features:**
- Real-time stats and charts
- Interactive search
- One-click email sending
- Workflow monitoring

### 3. n8n (Port 5678)

**Purpose:** Workflow automation

**Features:**
- Scheduled email sending (hourly/daily/custom)
- Visual workflow builder
- Error handling and logging
- 100+ integrations

**Workflow: Hourly Email**
```
Every Hour (0 * * * *)
  → Call FastAPI: POST /api/v1/email/send
  → Check success
  → Log result
```

**Start:**
```bash
n8n start
# or with Docker
docker run -p 5678:5678 n8nio/n8n
```

### 4. FastMCP (stdio)

**Purpose:** AI assistant integration

**Tools:**
1. `search_ai_news()` - Semantic search
2. `get_latest_digests()` - Recent summaries
3. `run_news_scraper()` - Scrape sources
4. `get_news_stats()` - System info
5. `run_full_workflow()` - Complete pipeline
6. `send_email_digest()` ⭐ **NEW** - Send email

**Start:**
```bash
fastmcp dev mcp_server.py
```

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "ai-news": {
      "command": "python",
      "args": ["-m", "fastmcp", "dev", "mcp_server.py"]
    }
  }
}
```

---

## 📧 Email Automation

### Method 1: n8n Scheduled (Recommended)

**Setup:**
1. Import workflow: `n8n_workflows/hourly_email_digest.json`
2. Activate workflow
3. Done! Emails sent every hour automatically

**Customize schedule:**
- Edit "Every Hour" node
- Change cron expression:
  - `0 * * * *` = Every hour
  - `0 8 * * *` = Daily at 8 AM
  - `0 */2 * * *` = Every 2 hours

### Method 2: Streamlit On-Demand

**Steps:**
1. Open http://localhost:8501
2. Go to 📧 Email page
3. Configure:
   - Time window (1h to 1 week)
   - Number of articles (1-50)
   - Optional: custom recipient
4. Click "📧 Send Email Now"
5. Wait for success message
6. Check email inbox!

**Use cases:**
- Quick manual send
- Testing email format
- Custom parameters
- Immediate delivery needed

### Method 3: FastAPI Programmatic

**cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "hours": 24,
    "top_n": 10,
    "recipient": "optional@email.com",
    "subject": "Custom Subject"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/email/send",
    json={"hours": 24, "top_n": 10}
)

print(response.json())
# {'success': True, 'articles_count': 10, 'recipient': '...'}
```

**Use cases:**
- External integrations
- Custom automation scripts
- Webhooks

### Method 4: Claude Desktop (MCP)

**In Claude Desktop:**
```
You: "Send me the latest AI news digest"

Claude: [Calls send_email_digest tool]
        "I've sent you an email with the top 10 AI articles
         from the last 24 hours!"
```

---

## 🐳 Production Deployment

### Docker Compose (All Services)

```bash
# Start everything
docker compose -f docker-compose.production.yml up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Stop and remove volumes
docker compose down -v
```

**Services included:**
- PostgreSQL (Port 5432)
- FastAPI (Port 8000)
- Streamlit (Port 8501)
- n8n (Port 5678)

### Environment Variables

All services use the same `.env` file:
```env
POSTGRES_DB=ai_news
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_here
GEMINI_API_KEY=your_key_here
MY_EMAIL=your@email.com
APP_PASSWORD=gmail_app_password
```

### Health Checks

**PostgreSQL:**
```bash
docker compose exec postgres pg_isready
```

**FastAPI:**
```bash
curl http://localhost:8000/health
```

**All services:**
```bash
docker compose ps
# All should show (healthy)
```

### Logs and Monitoring

**View logs:**
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f fastapi
docker compose logs -f streamlit
docker compose logs -f n8n
```

**n8n execution history:**
- http://localhost:5678 → Executions tab

**FastAPI requests:**
- Check terminal output
- Or use FastAPI `/docs` → Try it out

---

## 🔧 Troubleshooting

### Issue: "FastAPI Connection Refused"

**Symptoms:** Streamlit can't send email, n8n fails

**Solution:**
```bash
# Check if FastAPI is running
curl http://localhost:8000/health

# If not, start it
python main.py

# Verify
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### Issue: "No Digests Found"

**Symptoms:** Email page shows "No digests found"

**Solution:**
```bash
# Run workflow to generate digests
python cli.py run --hours 168

# Or use Streamlit → Workflow page
# Wait for completion (~5-15 minutes)

# Verify
python -c "from src.database.repository import Repository; print(len(Repository().get_recent_digests(168)))"
```

### Issue: "Email Not Received"

**Checklist:**
1. ✅ Check spam folder
2. ✅ Verify `MY_EMAIL` in `.env`
3. ✅ Verify `APP_PASSWORD` is Gmail App Password (not regular password)
4. ✅ Check FastAPI logs for errors
5. ✅ Test email manually:
   ```bash
   python -c "from src.services.email import send_email_to_self; send_email_to_self('Test', 'Hello!')"
   ```

### Issue: "n8n Can't Reach FastAPI"

**Symptoms:** n8n workflow fails with connection error

**Solutions:**

**If n8n in Docker:**
```
Use: http://host.docker.internal:8000/api/v1/email/send
Instead of: http://localhost:8000/api/v1/email/send
```

**Or run n8n with host network:**
```bash
docker run --network=host -p 5678:5678 n8nio/n8n
```

### Issue: "ChromaDB Errors"

**Symptoms:** Search fails, vector indexing errors

**Solution:**
```bash
# Delete and reinitialize
rm -rf chromadb_data/
python cli.py run --hours 168
```

### Issue: "Gemini API Quota Exceeded"

**Symptoms:** Digest generation fails, 429 errors

**Solutions:**
- Wait 1 minute (free tier: 10 requests/minute)
- Reduce articles being processed
- Upgrade to paid tier
- Check quota: https://ai.google.dev/gemini-api/docs/rate-limits

---

## 📊 Usage Examples

### Daily Morning Digest

**n8n Workflow:**
```
Schedule: 0 8 * * *  (Every day at 8 AM)
Config: {hours: 24, top_n: 5}
Result: Wake up to top 5 AI articles in inbox
```

### Breaking News Alerts

**n8n Workflow:**
```
Schedule: 0 * * * *  (Every hour)
Config: {hours: 1, top_n: 3}
Result: Hourly updates of latest 3 articles
```

### Weekly Summary

**n8n Workflow:**
```
Schedule: 0 18 * * 5  (Friday 6 PM)
Config: {hours: 168, top_n: 20}
Result: Comprehensive weekly roundup
```

### On-Demand Research

**Streamlit:**
1. Go to 📧 Email page
2. Set: hours=720 (1 month), top_n=30
3. Click "Send Email Now"
4. Get month's top 30 articles instantly

---

## 🎉 Summary

**You now have a complete professional AI news aggregation system with:**

✅ **Automated emails** every hour via n8n
✅ **On-demand emails** via Streamlit button
✅ **REST API** for external integrations
✅ **AI assistant access** via Claude Desktop
✅ **Beautiful web UI** with Streamlit
✅ **Docker deployment** for production
✅ **23 AI news sources** automatically tracked
✅ **RAG-powered search** for semantic queries

**Quick Reference:**
- **Streamlit UI:** http://localhost:8501
- **FastAPI Docs:** http://localhost:8000/docs
- **n8n Workflows:** http://localhost:5678
- **Send Email:** Streamlit → 📧 Email → Send Email Now

**Need Help?**
- Check logs: `docker compose logs -f`
- Test services: `curl http://localhost:8000/health`
- Review docs: `README.md`, `n8n_workflows/README.md`

Enjoy your AI-powered news aggregation! 🚀
