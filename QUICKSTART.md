# ⚡ Quick Start - AI News Aggregator

**Get running in 5 minutes!**

---

## 🎯 What You'll Get

- ✅ Hourly email digests (automated via n8n)
- ✅ Send email on-demand (Streamlit button)
- ✅ Beautiful web UI (Streamlit)
- ✅ REST API (FastAPI)
- ✅ AI assistant access (FastMCP)

---

## 🚀 5-Minute Setup

### 1. Clone & Configure (1 min)

```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator

# Copy and edit environment file
cp .env.example .env
# Edit .env with your:
# - GEMINI_API_KEY (get from https://ai.google.dev)
# - MY_EMAIL (your Gmail)
# - APP_PASSWORD (Gmail App Password)
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Create new app password
3. Copy 16-character password to `.env`

### 2. Install & Setup (2 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Start database
docker compose up -d

# Initialize database
python setup_database.py
```

### 3. Generate Initial Data (2 min)

```bash
# Run workflow to scrape and generate articles
python cli.py run --hours 168 --top-n 10

# Wait ~5-15 minutes
# You'll get: articles, summaries, email sent
```

### 4. Start Services (30 sec)

**Terminal 1: FastAPI**
```bash
python main.py
# Running on http://localhost:8000
```

**Terminal 2: Streamlit**
```bash
streamlit run streamlit_app.py
# Opens browser at http://localhost:8501
```

**Terminal 3: n8n (Optional)**
```bash
n8n start
# Opens at http://localhost:5678
```

### 5. Send Your First Email! (30 sec)

**Option A: Streamlit UI (Easiest)**
1. Go to http://localhost:8501
2. Click "📧 Email" in sidebar
3. Click "📧 Send Email Now"
4. Check your inbox! 📬

**Option B: API**
```bash
curl -X POST http://localhost:8000/api/v1/email/send \
  -H "Content-Type: application/json" \
  -d '{"hours": 24, "top_n": 10}'
```

---

## 🔄 Hourly Automation with n8n

### Setup (2 minutes)

1. **Open n8n:** http://localhost:5678
2. **Import workflow:**
   - Click "Import from file"
   - Select: `n8n_workflows/hourly_email_digest.json`
   - Click "Import"
3. **Activate:**
   - Toggle switch in top-right corner
   - Done! ✅

**Result:** Email sent every hour automatically! 🎉

---

## 📊 What Each Service Does

| Service | URL | Purpose |
|---------|-----|---------|
| **Streamlit** | http://localhost:8501 | Beautiful web UI |
| **FastAPI** | http://localhost:8000/docs | REST API |
| **n8n** | http://localhost:5678 | Workflow automation |
| **PostgreSQL** | localhost:5432 | Database |

---

## 🎨 Streamlit Pages

Access at http://localhost:8501:

- **🏠 Dashboard** - Stats, charts, recent activity
- **🔍 Search** - RAG semantic search
- **📰 Digests** - Browse AI summaries
- **🕷️ Scrape** - Trigger scraping
- **🚀 Workflow** - Run complete pipeline
- **📧 Email** ⭐ **NEW** - Send email now!
- **⚙️ Settings** - Configuration

---

## 📧 Email Methods

### Method 1: n8n Scheduled ⏰
**Best for:** Daily/hourly automation
```
✅ Activate n8n workflow
✅ Emails sent automatically every hour
✅ No manual intervention needed
```

### Method 2: Streamlit Button 🖱️
**Best for:** On-demand sending
```
✅ Go to 📧 Email page
✅ Click "Send Email Now"
✅ Instant delivery
```

### Method 3: FastAPI Call 🔌
**Best for:** External integrations
```bash
curl -X POST http://localhost:8000/api/v1/email/send \
  -H "Content-Type: application/json" \
  -d '{"hours": 24, "top_n": 10}'
```

### Method 4: Claude Desktop 🤖
**Best for:** Conversational access
```
You: "Send me the latest AI news"
Claude: [Sends email using MCP tool]
```

---

## 🆘 Quick Troubleshooting

### "No digests found"
```bash
# Run workflow first
python cli.py run --hours 168
```

### "FastAPI connection refused"
```bash
# Start FastAPI
python main.py
```

### "Email not received"
```bash
# Check spam folder
# Verify .env file has:
# - MY_EMAIL=your@gmail.com
# - APP_PASSWORD=gmail_app_password
```

### "n8n can't reach FastAPI"
```
# In n8n workflow, change URL to:
http://host.docker.internal:8000/api/v1/email/send
```

---

## 📚 Full Documentation

- **Complete Guide:** `DEPLOYMENT_GUIDE.md`
- **Performance:** `PERFORMANCE_OPTIMIZATIONS.md`
- **n8n Workflows:** `n8n_workflows/README.md`
- **MCP Setup:** `MCP_SETUP.md`

---

## 🎯 Next Steps

1. **Customize n8n schedule:**
   - Edit cron expression
   - Examples:
     - `0 8 * * *` = Daily at 8 AM
     - `0 */2 * * *` = Every 2 hours
     - `0 9 * * 1-5` = Weekdays at 9 AM

2. **Add more sources:**
   - Edit `src/config/web_sources.py`
   - Add RSS feeds or crawl targets

3. **Customize email template:**
   - Edit `src/agents/email.py`
   - Modify `src/services/email.py`

4. **Deploy to production:**
   ```bash
   docker compose -f docker-compose.production.yml up -d
   ```

---

## 🎉 You're All Set!

**Your AI News Aggregator is now:**
- ✅ Scraping 23 sources
- ✅ Generating AI summaries
- ✅ Sending hourly emails (if n8n activated)
- ✅ Ready for on-demand emails via Streamlit
- ✅ Accessible via REST API
- ✅ Integrated with Claude Desktop (if configured)

**Enjoy your AI-powered news! 🚀**

---

**Need Help?**
- Check logs: `docker compose logs -f`
- Test API: http://localhost:8000/docs
- View UI: http://localhost:8501

**Questions?** Open an issue or check the full `DEPLOYMENT_GUIDE.md`
