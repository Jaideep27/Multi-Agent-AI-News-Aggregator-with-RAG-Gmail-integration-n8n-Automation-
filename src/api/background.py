"""Background task handlers for long-running operations."""

import structlog
from typing import Dict, Any
from src.workflows.workflow import run_workflow
from src.core.runner import run_scrapers

log = structlog.get_logger()


async def run_workflow_background(hours: int, top_n: int, skip_email: bool = False) -> Dict[str, Any]:
    """
    Run the complete workflow in the background.
    
    Args:
        hours: Time window for scraping
        top_n: Number of top articles
        skip_email: Whether to skip email delivery
        
    Returns:
        Workflow result dictionary
    """
    try:
        log.info("Starting background workflow", hours=hours, top_n=top_n)
        result = run_workflow(hours=hours, top_n=top_n)
        log.info("Background workflow completed", success=result.get("success", False))
        return result
    except Exception as e:
        log.error("Background workflow failed", error=str(e))
        return {
            "success": False,
            "errors": [str(e)]
        }


async def run_scraping_background(hours: int) -> Dict[str, Any]:
    """
    Run scraping in the background.
    
    Args:
        hours: Time window for scraping
        
    Returns:
        Scraping result dictionary
    """
    try:
        log.info("Starting background scraping", hours=hours)
        result = run_scrapers(hours=hours)
        log.info("Background scraping completed", total=result.get("total", 0))
        return result
    except Exception as e:
        log.error("Background scraping failed", error=str(e))
        return {
            "youtube": [],
            "web": [],
            "total": 0,
            "error": str(e)
        }
