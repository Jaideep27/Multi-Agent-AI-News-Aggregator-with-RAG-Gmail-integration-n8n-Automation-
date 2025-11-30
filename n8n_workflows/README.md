# 📧 n8n Workflows for AI News Aggregator

This directory contains n8n workflow templates for automating email digests and other operations.

## 🚀 Available Workflows

### 1. **hourly_email_digest.json** ⏰
**Purpose:** Sends AI news digest email every hour automatically

**Features:**
- ✅ Runs every hour (cron: `0 * * * *`)
- ✅ Calls FastAPI endpoint: `POST /api/v1/email/send`
- ✅ Sends last 24 hours of articles (top 10)
- ✅ Success/error logging
- ✅ Automatic retry on failure

**Configuration:**
- Default: 24 hours, top 10 articles
- Email sent to configured `MY_EMAIL`
- Runs on localhost:8000 (FastAPI)

---

## 📋 Prerequisites

### 1. **FastAPI Server Running**
```bash
python main.py
# Should be running on http://localhost:8000
```

### 2. **n8n Installed**

**Option A: Docker (Recommended)**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option B: npm**
```bash
npm install n8n -g
n8n start
```

Access n8n at: **http://localhost:5678**

### 3. **Email Configuration**
Ensure `.env` file has:
```env
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-gmail-app-password
```

---

## 🔧 Setup Instructions

### Step 1: Import Workflow to n8n

1. Open n8n UI: http://localhost:5678
2. Click **"+ Add workflow"** or **"Import from file"**
3. Upload `hourly_email_digest.json`
4. Click **"Import"**

### Step 2: Configure Workflow (Optional)

The workflow is pre-configured to work with localhost. If your setup is different:

1. Click on **"Send Email Digest"** node
2. Update URL if FastAPI runs on different port:
   - Default: `http://localhost:8000/api/v1/email/send`
   - Change to your FastAPI URL if needed

3. Customize parameters (optional):
   - `hours`: Time window (default: 24)
   - `top_n`: Number of articles (default: 10)

### Step 3: Activate Workflow

1. Click the **toggle switch** in top-right corner
2. Workflow is now **ACTIVE** ✅
3. Will run every hour automatically

### Step 4: Test Manually (Optional)

1. Click **"Execute Workflow"** button
2. Watch it run in real-time
3. Check logs for success/error

---

## 📊 Workflow Details

### Hourly Email Digest Flow

```
┌─────────────────┐
│  Every Hour     │  Cron: 0 * * * *
│  (Schedule)     │  Runs at: 00:00, 01:00, 02:00, etc.
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Send Email     │  POST /api/v1/email/send
│  Digest         │  {hours: 24, top_n: 10}
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Email Sent?    │  Check response.success
└────┬───────┬────┘
     │       │
   YES      NO
     │       │
     ▼       ▼
┌────────┐ ┌────────┐
│  Log   │ │  Log   │
│Success │ │ Error  │
└────────┘ └────────┘
```

---

## ⚙️ Customization

### Change Schedule

Edit the "Every Hour" node:

**Every 2 hours:**
```
Cron: 0 */2 * * *
```

**Every 6 hours:**
```
Cron: 0 */6 * * *
```

**Daily at 8 AM:**
```
Cron: 0 8 * * *
```

**Monday to Friday at 9 AM:**
```
Cron: 0 9 * * 1-5
```

[Cron Expression Generator](https://crontab.guru/)

### Change Time Window

Edit the "Send Email Digest" node:

```json
{
  "hours": 48,     // Last 48 hours
  "top_n": 15      // Top 15 articles
}
```

### Add Recipient

Edit the "Send Email Digest" node:

```json
{
  "hours": 24,
  "top_n": 10,
  "recipient": "custom@email.com"  // Override MY_EMAIL
}
```

### Custom Subject

```json
{
  "hours": 24,
  "top_n": 10,
  "subject": "🔥 Breaking AI News - Hourly Update"
}
```

---

## 🔍 Monitoring

### View Execution History

1. Go to n8n UI → **"Executions"** tab
2. See all past runs with timestamps
3. Click any execution to see details

### Check Logs

n8n logs show:
- ✅ Success: Articles count, recipient, timestamp
- ❌ Error: Error message, status code

### Email Verification

Check your email inbox for:
- Subject: `🤖 AI News Digest - Top 10 Articles`
- From: Your configured `MY_EMAIL`
- Content: Formatted HTML digest

---

## 🚨 Troubleshooting

### Issue: "Connection refused"

**Cause:** FastAPI not running

**Solution:**
```bash
# Terminal 1: Start FastAPI
python main.py

# Verify it's running
curl http://localhost:8000/health
```

### Issue: "No digests found"

**Cause:** No articles processed in the time window

**Solution:**
```bash
# Run workflow to generate digests
python cli.py run --hours 168

# Or use Streamlit → Workflow page
```

### Issue: "Email not configured"

**Cause:** Missing `MY_EMAIL` or `APP_PASSWORD` in `.env`

**Solution:**
```bash
# Add to .env file
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password

# Restart FastAPI
python main.py
```

### Issue: "n8n not connecting to localhost"

**Cause:** Docker network isolation (if running n8n in Docker)

**Solution:**

Use `host.docker.internal` instead of `localhost`:
```
http://host.docker.internal:8000/api/v1/email/send
```

Or run n8n with `--network=host`:
```bash
docker run -it --rm \
  --name n8n \
  --network=host \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

---

## 📈 Advanced Workflows

### Multi-Platform Distribution

Create workflow to send to:
- Email (via FastAPI)
- Slack (via Slack node)
- Discord (via Discord webhook)
- Telegram (via Telegram node)

### Conditional Sending

Only send if:
- Article count > 5
- Contains specific keywords
- High-priority articles detected

### Smart Scheduling

- Weekdays: Every 2 hours
- Weekends: Once at 10 AM
- Different recipients for different topics

---

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [Cron Expression Guide](https://crontab.guru/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

## 🎉 Quick Start Summary

```bash
# 1. Start FastAPI
python main.py  # Port 8000

# 2. Start n8n
n8n start  # Port 5678

# 3. Import workflow
# Go to http://localhost:5678
# Import: n8n_workflows/hourly_email_digest.json

# 4. Activate workflow
# Toggle switch → ON

# 5. Done! ✅
# Emails sent every hour automatically
```

---

**Questions?** Check the main project README or open an issue!
