"""
Article Retriever Module

High-level interface for semantic article retrieval using RAG.
Combines embedding generation and vector search for intelligent retrieval.
"""

from typing import List, Dict, Optional, Any
import structlog
from .embeddings import EmbeddingGenerator, get_embedding_generator
from .vectorstore import VectorStore, get_vector_store

log = structlog.get_logger()


class ArticleRetriever:
    """
    High-level interface for retrieving articles using semantic search.

    Features:
    - Semantic similarity search
    - Hybrid search (keyword + semantic)
    - Contextual retrieval for better ranking
    - Duplicate detection
    """

    def __init__(self,
                 embedding_generator: Optional[EmbeddingGenerator] = None,
                 vector_store: Optional[VectorStore] = None):
        """
        Initialize the article retriever.

        Args:
            embedding_generator: Embedding generator instance
            vector_store: Vector store instance
        """
        self.embedding_generator = embedding_generator or get_embedding_generator()
        self.vector_store = vector_store or get_vector_store()

        log.info("Article retriever initialized",
                embedding_dim=self.embedding_generator.get_embedding_dimension(),
                articles_count=self.vector_store.count())

    def index_article(self,
                     article_id: str,
                     title: str,
                     summary: str,
                     content: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None):
        """
        Index a new article for semantic search.

        Args:
            article_id: Unique article ID (e.g., "youtube:abc123")
            title: Article title
            summary: Article summary
            content: Optional full content
            metadata: Additional metadata (url, type, published_at, etc.)
        """
        try:
            # Generate embedding
            embedding = self.embedding_generator.generate_article_embedding(
                title=title,
                summary=summary,
                content=content
            )

            # Prepare document text for storage
            document = f"{title}. {summary}"
            if content:
                document += f" {content[:500]}"  # Store snippet for context

            # Prepare metadata
            meta = metadata or {}
            meta.update({
                "title": title,
                "summary": summary
            })

            # Store in vector DB
            self.vector_store.add_article(
                article_id=article_id,
                embedding=embedding,
                document=document,
                metadata=meta
            )

            log.info("Article indexed successfully", article_id=article_id)

        except Exception as e:
            log.error("Failed to index article", article_id=article_id, error=str(e))
            raise

    def index_articles_batch(self, articles: List[Dict[str, Any]]):
        """
        Index multiple articles in batch (more efficient).

        Args:
            articles: List of article dicts with keys:
                      - id, title, summary, content (optional), metadata (optional)
        """
        try:
            log.info(f"Indexing {len(articles)} articles in batch")

            # Prepare data for batch processing
            article_ids = []
            documents = []
            metadatas = []

            # Generate all texts for embedding
            texts = []
            for article in articles:
                combined_text = f"{article['title']}. {article['summary']}"
                if article.get('content'):
                    combined_text += f" {article['content'][:1000]}"
                texts.append(combined_text)

                article_ids.append(article['id'])

                doc = f"{article['title']}. {article['summary']}"
                if article.get('content'):
                    doc += f" {article['content'][:500]}"
                documents.append(doc)

                meta = article.get('metadata', {})
                meta.update({
                    "title": article['title'],
                    "summary": article['summary']
                })
                metadatas.append(meta)

            # Generate embeddings in batch (faster)
            embeddings = self.embedding_generator.generate_embeddings(texts)

            # Add to vector store
            self.vector_store.add_articles(
                article_ids=article_ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            log.info(f"Successfully indexed {len(articles)} articles")

        except Exception as e:
            log.error("Failed to index articles batch", error=str(e))
            raise

    def find_similar(self,
                    query: str,
                    n_results: int = 5,
                    article_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Find articles similar to a query.

        Args:
            query: Text query
            n_results: Number of results to return
            article_type: Filter by type (youtube, openai, anthropic)

        Returns:
            List of similar articles with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(query)

            # Build filter
            where = None
            if article_type:
                where = {"article_type": article_type}

            # Search vector store
            results = self.vector_store.search(
                query_embedding=query_embedding,
                n_results=n_results,
                where=where
            )

            log.info(f"Found {results['count']} similar articles", query=query[:50])
            return results["results"]

        except Exception as e:
            log.error("Similarity search failed", error=str(e))
            return []

    def find_similar_to_article(self,
                               article_id: str,
                               n_results: int = 5,
                               exclude_self: bool = True) -> List[Dict[str, Any]]:
        """
        Find articles similar to a given article.

        Args:
            article_id: ID of the article to compare
            n_results: Number of results
            exclude_self: Whether to exclude the query article from results

        Returns:
            List of similar articles
        """
        try:
            # Get the article
            article = self.vector_store.get_article(article_id)
            if not article:
                log.warning("Article not found", article_id=article_id)
                return []

            # Search using its embedding
            results = self.vector_store.search(
                query_embedding=article["embedding"],
                n_results=n_results + (1 if exclude_self else 0)
            )

            # Filter out the query article itself
            similar_articles = results["results"]
            if exclude_self:
                similar_articles = [a for a in similar_articles if a["id"] != article_id]

            return similar_articles[:n_results]

        except Exception as e:
            log.error("Failed to find similar articles", article_id=article_id, error=str(e))
            return []

    def is_duplicate(self,
                    title: str,
                    summary: str,
                    threshold: float = 0.95) -> Optional[Dict[str, Any]]:
        """
        Check if an article is a duplicate based on semantic similarity.

        Args:
            title: Article title
            summary: Article summary
            threshold: Similarity threshold (0-1, higher = more strict)

        Returns:
            Duplicate article info if found, None otherwise
        """
        try:
            # Search for highly similar articles
            similar = self.find_similar(
                query=f"{title}. {summary}",
                n_results=1
            )

            if similar and similar[0]["distance"] is not None:
                similarity = 1 - similar[0]["distance"]  # Convert distance to similarity
                if similarity >= threshold:
                    log.info("Potential duplicate detected",
                            similarity=similarity,
                            existing_id=similar[0]["id"])
                    return similar[0]

            return None

        except Exception as e:
            log.error("Duplicate check failed", error=str(e))
            return None

    def get_context_for_ranking(self,
                               user_query: str,
                               n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Get historical context to improve ranking.

        Used by CuratorAgent to understand what similar articles
        the user has liked in the past.

        Args:
            user_query: Description of user interests
            n_results: Number of historical articles to retrieve

        Returns:
            List of relevant historical articles
        """
        return self.find_similar(user_query, n_results=n_results)

    def count_articles(self) -> int:
        """Get total number of indexed articles."""
        return self.vector_store.count()


# Singleton instance
_retriever: Optional[ArticleRetriever] = None


def get_article_retriever() -> ArticleRetriever:
    """Get or create singleton article retriever instance."""
    global _retriever
    if _retriever is None:
        _retriever = ArticleRetriever()
    return _retriever


if __name__ == "__main__":
    # Test the retriever
    import structlog
    structlog.configure(
        processors=[structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )

    retriever = ArticleRetriever()

    # Test indexing
    retriever.index_article(
        article_id="test_rag_1",
        title="Introduction to Retrieval-Augmented Generation",
        summary="RAG combines retrieval with generation for better AI outputs",
        metadata={"article_type": "test", "url": "https://example.com"}
    )

    # Test search
    results = retriever.find_similar("What is RAG?", n_results=2)
    print(f"Found {len(results)} results")
    if results:
        print(f"Top result: {results[0]['metadata']['title']}")
