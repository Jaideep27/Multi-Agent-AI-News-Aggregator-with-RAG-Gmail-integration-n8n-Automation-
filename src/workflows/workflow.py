"""
LangGraph Workflow Definition

Creates and executes the stateful workflow graph for the AI news aggregator.
"""

from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import structlog

from .state import WorkflowState, create_initial_state
from .nodes import (
    scraping_node,
    processing_node,
    digest_node,
    rag_indexing_node,
    ranking_node,
    email_node,
    error_handler_node
)

log = structlog.get_logger()


def should_continue(state: WorkflowState) -> Literal["continue", "error", "end"]:
    """
    Conditional edge: Decide whether to continue or handle errors.

    Returns:
        "continue" - Continue to next stage
        "error" - Go to error handler
        "end" - End workflow
    """
    # Check if we have errors
    if state["errors"] and state["retry_count"] < 3:
        return "error"

    # Check if workflow completed successfully
    if state["success"]:
        return "end"

    # Check if we're in a failed state
    if "failed" in state["current_stage"]:
        return "error"

    # Continue to next stage
    return "continue"


def route_after_scraping(state: WorkflowState) -> str:
    """
    Conditional edge after scraping: route to processing or error.
    """
    if state["current_stage"] == "scraping_failed":
        return "error_handler"

    if state["current_stage"] == "scraping_skipped":
        return "digest"  # Skip directly to digest if scraping skipped

    return "processing"


def route_after_processing(state: WorkflowState) -> str:
    """
    Conditional edge after processing: route to digest or error.
    """
    if state["current_stage"] == "processing_failed":
        return "error_handler"

    return "digest"


def route_after_digest(state: WorkflowState) -> str:
    """
    Conditional edge after digest: route to RAG indexing or error.
    """
    if state["current_stage"] == "digest_failed":
        return "error_handler"

    return "rag_indexing"


def route_after_rag(state: WorkflowState) -> str:
    """
    Conditional edge after RAG: route to ranking (even if indexing failed).
    """
    # Continue to ranking even if RAG indexing failed
    # (ranking can work without RAG context)
    return "ranking"


def route_after_ranking(state: WorkflowState) -> str:
    """
    Conditional edge after ranking: route to email or error.
    """
    if state["current_stage"] == "ranking_failed":
        return "error_handler"

    return "email"


def route_after_email(state: WorkflowState) -> str:
    """
    Conditional edge after email: end workflow.
    """
    if state["current_stage"] == "email_failed":
        return "error_handler"

    return END


def create_workflow() -> StateGraph:
    """
    Create the LangGraph workflow.

    Workflow stages:
    1. Scraping - Collect articles from sources
    2. Processing - Get transcripts/markdown
    3. Digest - Generate AI summaries
    4. RAG Indexing - Index in vector DB
    5. Ranking - Rank with RAG context
    6. Email - Send personalized digest

    Returns:
        Compiled StateGraph workflow
    """
    log.info("Creating LangGraph workflow")

    # Create graph
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("scraping", scraping_node)
    workflow.add_node("processing", processing_node)
    workflow.add_node("digest", digest_node)
    workflow.add_node("rag_indexing", rag_indexing_node)
    workflow.add_node("ranking", ranking_node)
    workflow.add_node("email", email_node)
    workflow.add_node("error_handler", error_handler_node)

    # Set entry point
    workflow.set_entry_point("scraping")

    # Add conditional edges
    workflow.add_conditional_edges(
        "scraping",
        route_after_scraping,
        {
            "processing": "processing",
            "digest": "digest",
            "error_handler": "error_handler"
        }
    )

    workflow.add_conditional_edges(
        "processing",
        route_after_processing,
        {
            "digest": "digest",
            "error_handler": "error_handler"
        }
    )

    workflow.add_conditional_edges(
        "digest",
        route_after_digest,
        {
            "rag_indexing": "rag_indexing",
            "error_handler": "error_handler"
        }
    )

    workflow.add_conditional_edges(
        "rag_indexing",
        route_after_rag,
        {
            "ranking": "ranking"
        }
    )

    workflow.add_conditional_edges(
        "ranking",
        route_after_ranking,
        {
            "email": "email",
            "error_handler": "error_handler"
        }
    )

    workflow.add_conditional_edges(
        "email",
        route_after_email,
        {
            "error_handler": "error_handler",
            END: END
        }
    )

    # Error handler can either retry or end
    workflow.add_conditional_edges(
        "error_handler",
        lambda state: "scraping" if state["current_stage"] == "retrying" else END,
        {
            "scraping": "scraping",
            END: END
        }
    )

    # Compile the workflow
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    log.info("Workflow created successfully")
    return app


def run_workflow(hours: int = 24, top_n: int = 10, config: Dict[str, Any] = None) -> WorkflowState:
    """
    Run the complete workflow.

    Args:
        hours: Time window for article scraping
        top_n: Number of articles to include in email
        config: Optional LangGraph configuration

    Returns:
        Final workflow state
    """
    log.info("=" * 60)
    log.info("Starting AI News Aggregator Workflow (LangGraph)")
    log.info("=" * 60)

    # Create initial state
    initial_state = create_initial_state(hours=hours, top_n=top_n)

    # Create workflow
    app = create_workflow()

    # Run workflow
    config = config or {"configurable": {"thread_id": "1"}}

    try:
        # Stream workflow and track progress
        for state in app.stream(initial_state, config):
            # Log progress
            for node_name, node_state in state.items():
                log.info(f"Completed node: {node_name}",
                        stage=node_state.get("current_stage"),
                        errors=len(node_state.get("errors", [])))

        # Get the final accumulated state
        final_state = app.get_state(config)
        final_state_values = final_state.values if hasattr(final_state, 'values') else final_state

        log.info("=" * 60)
        log.info("Workflow Complete")
        log.info("=" * 60)

        if final_state_values:
            log.info(f"Success: {final_state_values.get('success', False)}")
            log.info(f"Total errors: {len(final_state_values.get('errors', []))}")
            log.info(f"Articles scraped: {len(final_state_values.get('articles', []))}")
            log.info(f"Digests created: {len(final_state_values.get('digests', []))}")
            log.info(f"Articles ranked: {len(final_state_values.get('ranked_articles', []))}")

        return final_state_values

    except Exception as e:
        log.error("Workflow failed with exception", error=str(e))
        raise


if __name__ == "__main__":
    # Configure logging
    import logging
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    # Run workflow
    result = run_workflow(hours=24, top_n=10)

    if result and result.get("success"):
        print("\n✓ Workflow completed successfully!")
        print(f"Email sent with {len(result.get('ranked_articles', [])[:result.get('top_n', 10)])} articles")
    else:
        print("\n✗ Workflow failed")
        if result:
            print(f"Errors: {len(result.get('errors', []))}")
