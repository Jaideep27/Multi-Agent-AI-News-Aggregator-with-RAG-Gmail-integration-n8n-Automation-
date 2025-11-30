# 🚀 FastMCP Quick Start

## Install FastMCP

```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
pip install fastmcp
```

---

## Current Server & Client

### Server (What You Have)
- **FastAPI Server** - REST API on port 8000
- **FastMCP Server** - MCP protocol on stdio

### Client (How to Test NOW)

**Option 1: FastMCP Dev Server (Recommended)**
```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
fastmcp dev mcp_server.py
```
Opens web interface in your browser!

**Option 2: Direct Python Test**
```bash
cd C:\AI\ai-news-aggregator-master\latest-aggregator
venv\Scripts\activate
python test_mcp_tools.py
```
Tests all 5 tools and shows results!

**Option 3: Run Server Directly**
```bash
python mcp_server.py
```
Starts MCP server (for use with Claude Desktop)

---

## What MCP Tools Are Available?

1. **search_ai_news** - Semantic search using RAG
2. **get_latest_digests** - Get recent AI summaries
3. **run_news_scraper** - Scrape from 23 sources
4. **get_news_stats** - System statistics
5. **run_full_workflow** - Complete workflow + email

---

## Future Use (When You Want It)

### With Claude Desktop
1. Install Claude Desktop
2. Edit config: `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "ai-news-aggregator": {
      "command": "python",
      "args": ["C:\\AI\\ai-news-aggregator-master\\latest-aggregator\\mcp_server.py"]
    }
  }
}
```
3. Restart Claude Desktop
4. Chat: "Search my AI news for GPT-5 articles"

### With Continue.dev (VS Code)
1. Install Continue extension in VS Code
2. Configure MCP server in Continue settings
3. Use: `@ai-news-aggregator search for LLM reasoning`

---

## Run Both Servers

**Terminal 1: FastAPI**
```bash
python main.py
```
Access: http://localhost:8000/docs

**Terminal 2: FastMCP**
```bash
mcp-inspector python mcp_server.py
```
Access: http://localhost:5173

---

## What's the Difference?

| Feature | FastAPI | FastMCP |
|---------|---------|---------|
| **Interface** | REST/HTTP | MCP Protocol |
| **Access** | Browser, curl, apps | AI assistants |
| **Port** | 8000 | stdio |
| **Best For** | Web apps, scripts | Claude, AI tools |
| **Test With** | Swagger UI | MCP Inspector |

---

## Next Steps

1. **Test NOW:**
   ```bash
   npm install -g @anthropic-ai/mcp-inspector
   mcp-inspector python mcp_server.py
   ```
   Open http://localhost:5173 and try the tools!

2. **Use Later:** When you want AI assistant integration, follow the Claude Desktop or Continue.dev setup in `MCP_SETUP.md`

3. **Keep Using REST API:** FastAPI still works independently at http://localhost:8000/docs

**You now have both traditional API access AND AI-powered access!** 🎉
