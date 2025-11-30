# 🚀 FastMCP Setup Guide - AI News Aggregator

## Overview

Your AI News Aggregator now has **TWO interfaces**:

1. **FastAPI (REST)** - Port 8000
   - HTTP/REST endpoints
   - Swagger UI at http://localhost:8000/docs
   - Use with: Browser, curl, scripts, web apps

2. **FastMCP (MCP Protocol)** - stdio transport
   - MCP tools for AI assistants
   - Use with: Claude Desktop, MCP Inspector, Continue.dev

---

## 📦 Installation

Install FastMCP:

```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
pip install fastmcp
```

---

## 🔧 Current Server & Client Setup

### Server Side

```
┌─────────────────────────────────────┐
│     Your Computer (localhost)       │
├─────────────────────────────────────┤
│                                     │
│  FastAPI Server     FastMCP Server  │
│  (port 8000)        (stdio)         │
│       │                  │          │
│       └────────┬─────────┘          │
│                │                    │
│         Core Services               │
│    (Scraping, RAG, Database)        │
└─────────────────────────────────────┘
```

### Client Options (Current & Future)

**For Testing NOW:**
- ✅ **MCP Inspector** (web-based test tool)
- ✅ **Test script** (test_mcp_client.py)

**For Future Use:**
- 📅 **Claude Desktop** (when you install it)
- 📅 **Continue.dev** (VS Code AI extension)
- 📅 **Zed editor** (built-in MCP support)
- 📅 **Custom MCP clients**

---

## 🎯 Available MCP Tools

Your MCP server exposes 5 tools:

### 1. `search_ai_news`
**Purpose:** Semantic search using RAG
**Arguments:**
- `query` (required): Search text
- `limit` (optional): Number of results (default: 5)
- `article_type` (optional): Filter by type

**Example:**
```
"Search for articles about GPT-5 reasoning capabilities"
```

### 2. `get_latest_digests`
**Purpose:** Get recent AI summaries
**Arguments:**
- `hours` (optional): Time window (default: 168)
- `limit` (optional): Max results (default: 10)

**Example:**
```
"Show me the latest 5 AI news summaries from this week"
```

### 3. `run_news_scraper`
**Purpose:** Scrape from 23 sources
**Arguments:**
- `hours` (optional): Time window (default: 168)

**Example:**
```
"Scrape the latest AI news articles"
```

### 4. `get_news_stats`
**Purpose:** System statistics
**Arguments:** None

**Example:**
```
"What's the status of my AI news aggregator?"
```

### 5. `run_full_workflow`
**Purpose:** Complete 6-stage workflow
**Arguments:**
- `hours` (optional): Scraping window (default: 168)
- `top_n` (optional): Articles in email (default: 10)

**Example:**
```
"Run the weekly AI news digest workflow and send me the top 15 articles"
```

---

## 🧪 Testing the MCP Server

### Option 1: FastMCP Dev Server (Recommended)

**FastMCP** includes a built-in development server for testing.

1. **Start the dev server:**
   ```bash
   cd C:\AI\ai-news-aggregator-master\latest-aggregator
   venv\Scripts\activate
   fastmcp dev mcp_server.py
   ```

2. **Opens automatically in browser**
   - Web interface for testing all tools
   - Fill in arguments and execute
   - See live results!

### Option 2: Direct Python Testing

```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
python test_mcp_tools.py
```

This directly calls and tests all 5 MCP tools with real results.

### Option 3: Run MCP Server

```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
python mcp_server.py
```

This starts the MCP server in stdio mode (for use with Claude Desktop or other clients).

---

## 🖥️ Claude Desktop Setup (Future Use)

When you want to use Claude Desktop in the future:

### 1. Install Claude Desktop
Download from: https://claude.ai/download

### 2. Configure MCP Server

**Windows:** Edit this file:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Add this configuration:**
```json
{
  "mcpServers": {
    "ai-news-aggregator": {
      "command": "python",
      "args": [
        "C:\\AI\\ai-news-aggregator-master\\latest-aggregator\\mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\AI\\ai-news-aggregator-master\\latest-aggregator"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

### 4. Test in Claude

Open Claude Desktop and try:

```
"Use the ai-news-aggregator to search for articles about LLM reasoning"

"Get my latest AI news digests from this week"

"Run the news scraper to get fresh articles"

"Show me system stats for my news aggregator"
```

Claude will automatically use the MCP tools!

---

## 🔍 Continue.dev Setup (VS Code AI Extension)

If you use VS Code with Continue.dev:

### 1. Install Continue.dev Extension
In VS Code: Extensions → Search "Continue" → Install

### 2. Configure MCP Server

Open Continue settings and add:

```json
{
  "mcpServers": [
    {
      "name": "ai-news-aggregator",
      "command": "python",
      "args": [
        "C:\\AI\\ai-news-aggregator-master\\latest-aggregator\\mcp_server.py"
      ]
    }
  ]
}
```

### 3. Use in VS Code

In Continue chat:
```
"@ai-news-aggregator search for GPT-5 articles"
```

---

## 🏃 Running Both Servers

You can run FastAPI and FastMCP simultaneously in separate terminals:

**Terminal 1: FastAPI**
```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
python main.py
```
Access at: http://localhost:8000/docs

**Terminal 2: FastMCP (Dev Mode)**
```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
fastmcp dev mcp_server.py
```
Opens in browser automatically

---

## 📊 Architecture Comparison

### FastAPI (REST)
```
You → HTTP Request → FastAPI → Core Services → Response
```
**Best for:**
- Web apps
- Mobile apps
- Automated scripts
- API integrations

### FastMCP (MCP Protocol)
```
AI Assistant → MCP Tool Call → FastMCP → Core Services → Response → AI
```
**Best for:**
- Claude Desktop
- AI coding assistants
- Conversational interfaces
- AI agents

---

## 🐛 Troubleshooting

### MCP Server won't start
```bash
# Check FastMCP is installed
pip show fastmcp

# Reinstall if needed
pip install --upgrade fastmcp
```

### FastMCP dev mode issues
```bash
# Make sure FastMCP is installed
pip show fastmcp

# Reinstall if needed
pip install --upgrade fastmcp

# Try running directly
python mcp_server.py
```

### Claude Desktop can't find server
- Check config file path: `%APPDATA%\Claude\claude_desktop_config.json`
- Verify Python path is correct
- Restart Claude Desktop after config changes
- Check Windows logs for errors

### Port conflicts
- FastAPI uses port 8000
- MCP uses stdio (no port conflict)
- MCP Inspector uses port 5173

---

## 📝 Summary

**What you have now:**
- ✅ FastAPI server (REST API)
- ✅ FastMCP server (MCP tools)
- ✅ Test client script
- ✅ 5 MCP tools ready to use

**How to test immediately:**
1. Run: `python test_mcp_tools.py` (direct testing)
2. Or run: `fastmcp dev mcp_server.py` (web interface)
3. Test all 5 tools and see the results!

**Future use cases:**
- Install Claude Desktop → Configure → Use conversationally
- Install Continue.dev → Configure → Use in VS Code
- Any other MCP client → Configure → Use anywhere

**Your aggregator is now ready for both traditional API access AND AI-powered conversational access!** 🎉
