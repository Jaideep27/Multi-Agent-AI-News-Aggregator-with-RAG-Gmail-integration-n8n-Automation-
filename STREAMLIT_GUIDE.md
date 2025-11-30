# 🚀 Streamlit Frontend Guide

## Overview

The AI News Aggregator now includes a comprehensive **Streamlit web interface** that provides a modern, interactive dashboard for all system functionality.

**Features:**
- 📊 Real-time dashboard with statistics and charts
- 🔍 Semantic search with RAG-powered AI
- 📰 Browse and export AI-generated summaries
- 🕷️ Trigger article scraping with progress tracking
- 🚀 Run complete 6-stage workflow with monitoring
- ⚙️ System configuration and health checks

---

## 🎯 Quick Start

### 1. Install Dependencies

If you haven't already installed the Streamlit dependencies:

```bash
pip install -r requirements.txt
```

This includes:
- `streamlit>=1.32.0` - Web framework
- `plotly>=5.19.0` - Interactive charts
- `pandas>=2.2.0` - Data manipulation

### 2. Start the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will automatically open in your browser at: **http://localhost:8501**

### 3. Navigate

Use the sidebar to navigate between pages:
- 🏠 Dashboard
- 🔍 Search
- 📰 Digests
- 🕷️ Scrape
- 🚀 Workflow
- ⚙️ Settings

---

## 📄 Page Overview

### 🏠 Dashboard

**Purpose:** System overview and quick insights

**Features:**
- **4 Stat Cards:**
  - Total indexed articles
  - Weekly digests count
  - Active sources (23)
  - System version

- **Activity Chart:**
  - Interactive Plotly bar chart
  - Shows digest creation over time
  - Grouped by day

- **Category Distribution:**
  - Pie chart of article types
  - Official blogs, research, news, safety, YouTube

- **System Configuration:**
  - AI models (Gemini 2.5 Flash)
  - Embeddings (all-MiniLM-L6-v2)
  - Databases (PostgreSQL, ChromaDB)

- **Data Sources:**
  - 3 YouTube channels
  - 20 web sources

- **Recent Activity:**
  - Preview of latest 5 digests
  - Quick links to full articles

**Use Case:** Start here to see system health and recent activity

---

### 🔍 Search

**Purpose:** Semantic search with RAG-powered AI

**Features:**
- **Search Interface:**
  - Query input with natural language support
  - Filter by article type (Official, Research, News, Safety, YouTube)
  - Adjust number of results (1-20)

- **Results Display:**
  - Relevance score (0-100%)
  - Article type badges with emojis
  - AI-generated summaries
  - Direct links to full articles

- **Search Tips:**
  - How semantic search works
  - Example queries
  - Best practices

- **Quick Search Buttons:**
  - LLM Reasoning
  - AI Safety
  - Research Papers

**Use Case:** Find specific topics using AI-powered semantic understanding

**Example Queries:**
- "GPT-5 reasoning capabilities"
- "AI safety and alignment research"
- "Transformer architecture improvements"

---

### 📰 Digests

**Purpose:** Browse and export AI-generated article summaries

**Features:**
- **Filters:**
  - Time period (24h, 3 days, 1 week, 1 month)
  - Max results (5-100)
  - Filter by type (All, Official, Research, News, Safety, YouTube)

- **Statistics:**
  - Total digests
  - Count by category

- **Digest Display:**
  - Grouped by date
  - Type emoji badges
  - Full AI summaries
  - Links to original articles
  - Copy summary button

- **Export Options:**
  - Download as Markdown (.md)
  - Download as JSON (.json)
  - Timestamp in filename

**Use Case:** Review AI summaries and export for sharing or archiving

---

### 🕷️ Scrape

**Purpose:** Trigger article scraping from 23 sources

**Features:**
- **Source Information:**
  - 3 YouTube channels
  - 20 web sources (9 official, 3 research, 5 news, 3 safety)

- **Configuration:**
  - Time window (24h, 3 days, 1 week, 1 month)
  - Estimated time display

- **Progress Tracking:**
  - Progress bar
  - Status updates
  - Real-time feedback

- **Results Display:**
  - YouTube videos count
  - Web articles count
  - Total articles
  - Breakdown by category (Official, Research, News, Safety)
  - Sample articles preview

- **Next Steps:**
  - Guidance on what to do after scraping

**Use Case:** Collect fresh articles without processing (fast, ~2-3 minutes)

**Note:** Scraped articles are saved to database but NOT yet processed by AI. Use the Workflow page for complete processing.

---

### 🚀 Workflow

**Purpose:** Run the complete 6-stage AI news aggregation pipeline

**Features:**
- **Workflow Diagram:**
  - Visual representation of 6 stages
  - Estimated time for each stage

- **Configuration:**
  - Time window (24h, 3 days, 1 week, 1 month)
  - Articles in email (5-50)

- **Stage Explanations:**
  - Stage 1: Scraping (~2-3 minutes)
  - Stage 2: Processing (~30-60 seconds)
  - Stage 3: AI Digest (~3-8 minutes)
  - Stage 4: RAG Indexing (~30-60 seconds)
  - Stage 5: Ranking (~1-2 minutes)
  - Stage 6: Email (~5-10 seconds)

- **Progress Monitoring:**
  - Real-time progress updates
  - Stage-by-stage tracking

- **Results Display:**
  - Workflow metrics (scraped, digests, ranked, email)
  - Top N articles preview
  - Relevance scores
  - AI reasoning for ranking

- **Tips & Troubleshooting:**
  - Best practices for daily/weekly/monthly digests
  - Gemini API limits
  - Common issues and solutions

**Use Case:** Complete end-to-end workflow from scraping to email delivery

**Total Time:** 5-15 minutes (depending on article count)

**Note:** This is the FULL pipeline. If you only want to scrape, use the Scrape page.

---

### ⚙️ Settings

**Purpose:** System configuration and health monitoring

**Features:**
- **Environment Info:**
  - Application name and version
  - Environment (development/production)
  - Debug mode status
  - Python version and platform
  - Working directory

- **AI Models Configuration:**
  - **Gemini AI:**
    - Digest generator model (gemini-2.0-flash-exp)
    - Article curator model (gemini-2.0-flash-exp)
    - Temperature settings
    - API key status
    - Free tier limits

  - **Embeddings:**
    - Model (all-MiniLM-L6-v2)
    - Dimension (384)
    - Device (CPU)

- **Database Configuration:**
  - **PostgreSQL:**
    - Host, port, database, user
    - Test connection button
    - Table info display

  - **ChromaDB:**
    - Persist directory
    - Collection name
    - Test connection button
    - Article count

- **Email Configuration:**
  - SMTP host, port, user
  - From/to email addresses
  - TLS status
  - Password status

- **API Configuration:**
  - **FastAPI:**
    - Host, port, workers
    - CORS status
    - Open Swagger UI button

  - **FastMCP:**
    - Transport, protocol
    - Available tools (5)
    - View docs link

- **Workflow Settings:**
  - Default time window
  - Default top N articles
  - Max retries
  - Log level

- **Data Sources:**
  - **YouTube (3 channels):**
    - Channel names and IDs
    - Direct links

  - **Web (20 sources):**
    - Source name, category
    - URL, RSS URL
    - Scrape type
    - Description

- **Environment Variables:**
  - Masked sensitive values
  - API keys, database credentials, SMTP password

- **System Actions:**
  - Reload configuration
  - Clear caches

**Use Case:** Verify system configuration, test connections, troubleshoot issues

---

## 🎨 UI Features

### Custom Styling

- **Gradient Headers:** Eye-catching purple gradient text
- **Stat Cards:** Colorful gradient background cards
- **Type Badges:** Emoji-based category indicators
  - 🏢 Official Blogs
  - 🔬 Research Papers
  - 📰 News Sites
  - 🛡️ AI Safety
  - 📺 YouTube Videos

### Interactive Elements

- **Charts:** Plotly interactive visualizations (hover, zoom, pan)
- **Filters:** Dynamic filtering with immediate updates
- **Expanders:** Collapsible sections to reduce clutter
- **Buttons:** Action buttons with progress feedback
- **Download:** Direct download buttons for exports

---

## 🔧 Configuration

### Prerequisites

Before using the Streamlit app, ensure:

1. **Database is running:**
   ```bash
   docker compose up -d
   ```

2. **Database is initialized:**
   ```bash
   python setup_database.py
   ```

3. **Environment variables are set:**
   - `.env` file with:
     - `GEMINI_API_KEY`
     - `POSTGRES_*` credentials
     - `SMTP_*` configuration (optional for email)

### Port Configuration

By default, Streamlit runs on **port 8501**.

To change the port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Browser Configuration

Streamlit auto-opens in your default browser. To disable:
```bash
streamlit run streamlit_app.py --server.headless true
```

Then manually navigate to: http://localhost:8501

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Database connection failed"

**Symptoms:** Error on Dashboard or Settings page when testing connections

**Solutions:**
1. Verify Docker containers are running:
   ```bash
   docker compose ps
   ```

2. Check environment variables:
   ```bash
   cat .env
   ```

3. Test database setup:
   ```bash
   python setup_database.py
   ```

### Issue: "ChromaDB connection failed"

**Solutions:**
1. Ensure you've run the workflow at least once to create the ChromaDB collection
2. Check the persist directory exists:
   ```bash
   ls -la ./chromadb_data
   ```

3. Try running a scrape + digest workflow:
   ```bash
   python cli.py run --hours 168
   ```

### Issue: "No digests found"

**Symptoms:** Empty state on Digests or Dashboard pages

**Solutions:**
1. Run the complete workflow to generate digests:
   - Use the 🚀 Workflow page in Streamlit, OR
   - Run via CLI: `python cli.py run --hours 168`

2. Try expanding the time period filter to 1 week or 1 month

### Issue: "Search returns no results"

**Solutions:**
1. Ensure articles are indexed in ChromaDB (run workflow first)
2. Try broader search queries
3. Remove type filters
4. Check ChromaDB article count on Settings page

### Issue: "Email sending failed"

**Symptoms:** Workflow completes but email not received

**Solutions:**
1. Verify SMTP configuration in `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   MY_EMAIL=recipient@example.com
   ```

2. Check SMTP password status on Settings page

3. For Gmail, use an App Password (not your regular password)

### Issue: "Gemini API quota exceeded"

**Symptoms:** Workflow fails during digest generation

**Solutions:**
1. Wait 1 minute (free tier: 10 requests/minute)
2. Reduce the time window to process fewer articles
3. Consider upgrading to paid tier
4. Check quota at: https://ai.google.dev/gemini-api/docs/rate-limits

---

## 💡 Tips & Best Practices

### Daily Digest Workflow

**Recommended Settings:**
- Time Window: 24 hours
- Top N: 5-10 articles
- Frequency: Run once per day

**Steps:**
1. Go to 🚀 Workflow page
2. Select "24 hours"
3. Set 5-10 articles
4. Click "Run Complete Workflow"
5. Check email for digest

### Weekly Digest Workflow

**Recommended Settings:**
- Time Window: 168 hours (1 week)
- Top N: 10-15 articles
- Frequency: Run once per week

### Monthly Review Workflow

**Recommended Settings:**
- Time Window: 720 hours (1 month)
- Top N: 20-30 articles
- Frequency: Run once per month

### Fast Scraping Only

If you just want to collect articles without AI processing:

1. Go to 🕷️ Scrape page
2. Select time window
3. Click "Start Scraping"
4. Wait ~2-3 minutes

**Note:** Articles are saved but not processed. No AI summaries, no ranking, no email.

### Using Search Effectively

**Good Queries:**
- "GPT-5 reasoning capabilities"
- "AI safety and alignment research"
- "Transformer architecture improvements"
- "LLM fine-tuning techniques"

**Why it works:** Semantic search understands meaning, not just keywords.

**Example:**
- Query: "LLM thinking" → Finds articles about "reasoning", "chain of thought", "inference"
- Query: "AI dangers" → Finds articles about "safety", "alignment", "risks", "misuse"

---

## 📊 Performance Notes

### Speed Expectations

- **Dashboard:** Instant (cached data)
- **Search:** 1-2 seconds per query
- **Digests:** Instant (database query)
- **Scrape:** 2-3 minutes for 23 sources
- **Workflow:** 5-15 minutes (complete pipeline)

### Resource Usage

- **CPU:** Moderate during embedding generation
- **Memory:** ~500MB-1GB (depends on article count)
- **Disk:** ChromaDB grows with indexed articles
- **Network:** Bandwidth during scraping

### Gemini API Limits (Free Tier)

- **Rate Limit:** 10 requests per minute
- **Impact:** Digest generation is rate-limited
- **Workaround:** Workflow automatically handles retries with exponential backoff

---

## 🔗 Related Documentation

- **Main README:** `README.md` - Project overview
- **CLI Guide:** Use `python cli.py --help` for command-line usage
- **MCP Guide:** `MCP_SETUP.md` - FastMCP server setup
- **Web Sources:** `src/config/web_sources.py` - 20 web source definitions

---

## 🆘 Getting Help

### Debug Mode

To see detailed logs in Streamlit:

1. Check terminal output where you ran `streamlit run`
2. Look for error messages and stack traces
3. Use Settings page to verify configuration

### Check System Health

1. Go to ⚙️ Settings page
2. Click "Test PostgreSQL Connection"
3. Click "Test ChromaDB Connection"
4. Verify all environment variables are set

### Common Commands

**Reset everything:**
```bash
# Stop containers
docker compose down -v

# Restart containers
docker compose up -d

# Reinitialize database
python setup_database.py

# Run workflow
python cli.py run --hours 168
```

**Check logs:**
```bash
# View Docker logs
docker compose logs -f

# View Streamlit logs
# (shown in terminal where you ran streamlit)
```

---

## 🎉 Summary

The Streamlit frontend provides a **complete, user-friendly interface** for the AI News Aggregator:

✅ **6 comprehensive pages** covering all functionality
✅ **Real-time statistics** and interactive charts
✅ **Semantic search** with RAG-powered AI
✅ **Progress tracking** for long-running operations
✅ **Export capabilities** (Markdown, JSON)
✅ **System health monitoring** with test buttons
✅ **Modern UI** with gradients, emojis, and responsive design

**Quick Start:**
```bash
streamlit run streamlit_app.py
```

Then open: http://localhost:8501

Enjoy your AI-powered news aggregation experience! 🚀
