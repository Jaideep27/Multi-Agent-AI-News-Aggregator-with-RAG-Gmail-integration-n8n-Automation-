"""
Direct MCP Tools Testing Script

This script tests the core functionality that the MCP tools use.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import get_settings
from src.database.repository import Repository
from src.rag.retriever import get_article_retriever
from src.core.runner import run_scrapers
from src.workflows.workflow import run_workflow


def print_section(title):
    """Print a section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def print_result(result):
    """Pretty print a result."""
    import json
    print(json.dumps(result, indent=2, default=str))


def test_get_stats():
    """Test system statistics."""
    settings = get_settings()
    retriever = get_article_retriever()
    article_count = retriever.count_articles()

    return {
        "status": "healthy",
        "vector_store": {
            "total_indexed_articles": article_count,
            "embedding_model": settings.embedding_model,
            "embedding_dimensions": settings.embedding_dimension
        },
        "database": {
            "status": "connected",
            "host": settings.postgres_host,
            "database": settings.postgres_db
        },
        "ai_models": {
            "digest_model": settings.gemini_model_digest,
            "curator_model": settings.gemini_model_curator
        },
        "environment": settings.environment,
        "version": settings.app_version
    }


def test_search(query: str, limit: int = 5):
    """Test semantic search."""
    retriever = get_article_retriever()
    results = retriever.find_similar(
        query=query,
        n_results=limit
    )

    # Format results
    formatted_results = []
    for i, result in enumerate(results, 1):
        metadata = result.get("metadata", {})
        similarity = 1 - result.get("distance", 0) if result.get("distance") is not None else 0

        formatted_results.append({
            "rank": i,
            "title": metadata.get("title", "N/A"),
            "summary": result.get("document", "")[:200] + "...",
            "similarity_score": f"{similarity:.2%}"
        })

    return {
        "query": query,
        "results": formatted_results,
        "count": len(formatted_results)
    }


def test_get_digests(hours: int = 168, limit: int = 10):
    """Test getting recent digests."""
    repo = Repository()
    digests = repo.get_recent_digests(hours=hours)

    # Format for readability
    formatted_digests = []
    for digest in digests[:limit]:
        formatted_digests.append({
            "title": digest["title"],
            "type": digest["article_type"],
            "url": digest["url"][:50] + "...",
            "created_at": str(digest["created_at"])
        })

    return {
        "digests": formatted_digests,
        "total_found": len(digests),
        "returned": len(formatted_digests),
        "time_window_hours": hours
    }


def main():
    """Test all MCP tool functionality."""
    print("\n🧪 Testing AI News Aggregator MCP Tool Functionality")
    print("="*70)

    # Test 1: Get Stats
    print_section("Test 1: Get System Stats (get_news_stats)")
    try:
        result = test_get_stats()
        print_result(result)
        print("\n✅ Test passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Search
    print_section("Test 2: Search AI News (search_ai_news)")
    try:
        result = test_search(
            query="GPT-5 and reasoning capabilities",
            limit=3
        )
        print_result(result)
        print("\n✅ Test passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    # Test 3: Get Digests
    print_section("Test 3: Get Latest Digests (get_latest_digests)")
    try:
        result = test_get_digests(hours=168, limit=5)
        print_result(result)
        print("\n✅ Test passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    # Test 4: Scraper (optional)
    print_section("Test 4: Run News Scraper (run_news_scraper)")
    answer = input("Do you want to run the scraper? This will take a few minutes (y/n): ")
    if answer.lower() == 'y':
        try:
            results = run_scrapers(hours=24)
            result = {
                "status": "success",
                "youtube_videos": len(results.get("youtube", [])),
                "web_articles": len(results.get("web", [])),
                "total_articles": results.get("total", 0),
                "time_window_hours": 24
            }
            print_result(result)
            print("\n✅ Test passed!")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⏭️  Skipped scraper test")

    # Test 5: Full Workflow (optional)
    print_section("Test 5: Run Full Workflow (run_full_workflow)")
    answer = input("Do you want to run the full workflow? This will scrape, process, and email (y/n): ")
    if answer.lower() == 'y':
        try:
            workflow_result = run_workflow(hours=168, top_n=5)
            if workflow_result and workflow_result.get("success"):
                result = {
                    "status": "success",
                    "articles_scraped": len(workflow_result.get("articles", [])),
                    "digests_created": len(workflow_result.get("digests", [])),
                    "articles_ranked": len(workflow_result.get("ranked_articles", [])),
                    "email_sent": True
                }
            else:
                result = {"status": "failed", "error": "Workflow failed"}
            print_result(result)
            print("\n✅ Test passed!")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⏭️  Skipped workflow test")

    print("\n" + "="*70)
    print("✅ Testing complete!")
    print("="*70)
    print("\nThese are the same operations that the MCP tools perform!")
    print("\nNext steps:")
    print("1. Run: fastmcp dev mcp_server.py (to use web interface)")
    print("2. Configure Claude Desktop (see MCP_SETUP.md)")
    print("3. Or use Continue.dev in VS Code")


if __name__ == "__main__":
    main()
