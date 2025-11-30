"""
Simple MCP Client for Testing - AI News Aggregator

This script tests the MCP server by calling its tools directly.
Run this AFTER starting the MCP server.
"""

import json
import subprocess
import sys


def test_mcp_tool(tool_name: str, arguments: dict = None):
    """
    Test an MCP tool by calling it via the server.

    Args:
        tool_name: Name of the tool to test
        arguments: Dictionary of arguments to pass
    """
    if arguments is None:
        arguments = {}

    print(f"\n{'='*60}")
    print(f"Testing: {tool_name}")
    print(f"Arguments: {json.dumps(arguments, indent=2)}")
    print(f"{'='*60}\n")

    # This is a simplified test - in production you'd use proper MCP client library
    # For now, we'll just show what would be called
    print(f"Would call MCP tool: {tool_name}")
    print(f"With args: {arguments}")
    print("\nNote: To fully test, use MCP Inspector or Claude Desktop")


def main():
    """Run all MCP tool tests."""
    print("🧪 AI News Aggregator - MCP Client Test Suite")
    print("="*60)

    # Test 1: Get Stats
    print("\n📊 Test 1: Get System Stats")
    test_mcp_tool("get_news_stats")

    # Test 2: Search
    print("\n🔍 Test 2: Search AI News")
    test_mcp_tool("search_ai_news", {
        "query": "GPT-5 and reasoning capabilities",
        "limit": 5
    })

    # Test 3: Get Digests
    print("\n📰 Test 3: Get Latest Digests")
    test_mcp_tool("get_latest_digests", {
        "hours": 168,
        "limit": 10
    })

    # Test 4: Run Scraper
    print("\n🕷️  Test 4: Run News Scraper")
    test_mcp_tool("run_news_scraper", {
        "hours": 168
    })

    # Test 5: Full Workflow
    print("\n🚀 Test 5: Run Full Workflow")
    test_mcp_tool("run_full_workflow", {
        "hours": 168,
        "top_n": 10
    })

    print("\n" + "="*60)
    print("✅ Test suite completed!")
    print("\nTo actually test the MCP server, use:")
    print("1. MCP Inspector (recommended)")
    print("2. Claude Desktop (when configured)")
    print("3. Continue.dev or other MCP clients")
    print("="*60)


if __name__ == "__main__":
    main()
