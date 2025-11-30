"""
Professional CLI interface for the AI News Aggregator.

Uses Click for a rich command-line experience with commands, options, and help text.
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import get_settings
from src.core.logging import configure_logging
from src.workflows.workflow import run_workflow
from src.rag.retriever import get_article_retriever
from src.database.repository import Repository

console = Console()


@click.group()
@click.version_option(version="2.0.0", prog_name="AI News Aggregator")
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.pass_context
def cli(ctx, debug):
    """
    AI News Aggregator - Production Edition

    Intelligent news aggregation with LangGraph, RAG, and Gemini AI.
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug

    # Configure logging
    settings = get_settings()
    if debug:
        settings.log_level = "DEBUG"
    configure_logging(settings)


@cli.command()
@click.option('--hours', default=24, help='Time window for scraping (hours)', show_default=True)
@click.option('--top-n', default=10, help='Number of articles in digest', show_default=True)
@click.option('--skip-scraping', is_flag=True, help='Skip scraping, use existing data')
@click.option('--skip-email', is_flag=True, help='Skip sending email')
def run(hours, top_n, skip_scraping, skip_email):
    """
    Run the complete AI news aggregator workflow.

    This executes all stages:
    - Scraping (23 sources: 3 YouTube + 20 Web)
    - Processing (YouTube transcripts)
    - Digest generation (AI summaries)
    - RAG indexing (vector database)
    - Ranking (personalized curation)
    - Email (send digest)
    """
    console.print("\n[bold blue]AI News Aggregator - Workflow Starting[/bold blue]\n")

    with console.status("[bold green]Running workflow...") as status:
        try:
            result = run_workflow(hours=hours, top_n=top_n)

            if result and result.get("success"):
                console.print("\n[bold green][SUCCESS] Workflow completed successfully![/bold green]\n")

                # Display summary table
                table = Table(title="Workflow Summary")
                table.add_column("Stage", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Count", justify="right", style="yellow")

                articles_count = len(result.get("articles", []))
                digests_count = len(result.get("digests", []))
                ranked_count = len(result.get("ranked_articles", []))

                table.add_row("Articles Scraped", "✓" if articles_count > 0 else "SKIP", str(articles_count))
                table.add_row("Digests Created", "✓" if digests_count > 0 else "SKIP", str(digests_count))
                table.add_row("Vector Indexed", "✓" if result.get("vector_indexed") else "SKIP", str(digests_count) if result.get("vector_indexed") else "0")
                table.add_row("Articles Ranked", "✓" if ranked_count > 0 else "SKIP", str(ranked_count))
                table.add_row("Email Sent", "✓" if result.get("success") else "✗", str(min(ranked_count, result.get("top_n", 10))))

                console.print(table)
            else:
                console.print("\n[bold red][FAILED] Workflow failed[/bold red]\n")
                if result:
                    errors = result.get("errors", [])
                    if errors:
                        console.print(f"[red]Errors: {len(errors)}[/red]")
                sys.exit(1)

        except Exception as e:
            console.print(f"\n[bold red][ERROR] {str(e)}[/bold red]\n")
            sys.exit(1)


@cli.command()
@click.option('--hours', default=24, help='Time window (hours)', show_default=True)
@click.option('--limit', default=50, help='Maximum results', show_default=True)
def digests(hours, limit):
    """
    List recent article digests from the database.
    """
    console.print(f"\n[bold]Recent Digests (last {hours}h)[/bold]\n")

    try:
        repo = Repository()
        results = repo.get_recent_digests(hours=hours)

        if not results:
            console.print("[yellow]No digests found[/yellow]")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Title", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("URL", style="blue")

        for digest in results[:limit]:
            table.add_row(
                digest["id"][:20] + "...",
                digest["title"][:60] + "..." if len(digest["title"]) > 60 else digest["title"],
                digest["article_type"],
                digest["url"][:40] + "..." if len(digest["url"]) > 40 else digest["url"]
            )

        console.print(table)
        console.print(f"\n[dim]Showing {min(len(results), limit)} of {len(results)} digests[/dim]\n")

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--results', default=5, help='Number of results', show_default=True)
@click.option('--type', 'article_type', help='Filter by type (youtube/openai/anthropic)')
def search(query, results, article_type):
    """
    Semantic search using RAG (vector similarity).

    Find articles similar to your query using embeddings.

    Example:
        python cli.py search "RAG systems and vector databases"
    """
    console.print(f"\n[bold]Searching for: '{query}'[/bold]\n")

    try:
        retriever = get_article_retriever()
        similar = retriever.find_similar(
            query=query,
            n_results=results,
            article_type=article_type
        )

        if not similar:
            console.print("[yellow]No results found[/yellow]")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Similarity", justify="right", style="green")
        table.add_column("Title", style="cyan")
        table.add_column("Type", style="yellow")

        for result in similar:
            similarity = 1 - result.get("distance", 0) if result.get("distance") is not None else 0
            title = result.get("metadata", {}).get("title", "N/A")
            atype = result.get("metadata", {}).get("article_type", "N/A")

            table.add_row(
                f"{similarity:.2%}",
                title[:70] + "..." if len(title) > 70 else title,
                atype
            )

        console.print(table)
        console.print(f"\n[dim]Found {len(similar)} similar articles[/dim]\n")

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
def stats():
    """
    Display system statistics.
    """
    console.print("\n[bold]System Statistics[/bold]\n")

    try:
        # Vector store stats
        retriever = get_article_retriever()
        vector_count = retriever.count_articles()

        # Database stats
        repo = Repository()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Count/Info", justify="right", style="yellow")

        table.add_row("Vector Store (ChromaDB)", "Healthy", str(vector_count))
        table.add_row("Database (PostgreSQL)", "Connected", "")

        console.print(table)

        # Settings info
        settings = get_settings()
        console.print(f"\n[dim]Environment: {settings.environment}[/dim]")
        console.print(f"[dim]Gemini Model: {settings.gemini_model_digest}[/dim]")
        console.print(f"[dim]Embedding Model: {settings.embedding_model}[/dim]\n")

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
def config():
    """
    Display current configuration.
    """
    console.print("\n[bold]Configuration[/bold]\n")

    settings = get_settings()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="yellow")

    # Display safe settings (hide secrets)
    safe_settings = {
        "App Name": settings.app_name,
        "Version": settings.app_version,
        "Environment": settings.environment,
        "Debug": str(settings.debug),
        "Email": settings.my_email,
        "Gemini Model (Digest)": settings.gemini_model_digest,
        "Gemini Model (Curator)": settings.gemini_model_curator,
        "Embedding Model": settings.embedding_model,
        "Embedding Dimension": str(settings.embedding_dimension),
        "Database Host": settings.postgres_host,
        "Database Name": settings.postgres_db,
        "Redis Host": settings.redis_host,
        "ChromaDB Path": settings.chroma_persist_directory,
        "Default Hours": str(settings.default_hours),
        "Default Top N": str(settings.default_top_n),
        "Max Retries": str(settings.max_retries),
        "Log Level": settings.log_level,
    }

    for key, value in safe_settings.items():
        table.add_row(key, value)

    console.print(table)
    console.print()


@cli.command()
@click.option('--hours', default=24, help='Time window (hours)', show_default=True)
def scrape(hours):
    """
    Run only the scraping stage (no AI processing).
    """
    console.print(f"\n[bold]Scraping articles (last {hours}h)[/bold]\n")

    try:
        from src.core.runner import run_scrapers

        with console.status("[bold green]Scraping...") as status:
            results = run_scrapers(hours=hours)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Source", style="cyan")
        table.add_column("Articles", justify="right", style="yellow")

        table.add_row("YouTube", str(len(results.get("youtube", []))))
        table.add_row("Web", str(len(results.get("web", []))))
        table.add_row("TOTAL", str(results.get("total", 0)), style="bold green")

        console.print(table)
        console.print()

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    cli(obj={})
