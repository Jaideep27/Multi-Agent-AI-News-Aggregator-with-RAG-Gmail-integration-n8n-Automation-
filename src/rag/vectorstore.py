"""
Vector Store Module

Manages ChromaDB vector database for storing and retrieving article embeddings.
Supports semantic search, filtering, and similarity-based retrieval.
"""

import os
from typing import List, Dict, Optional, Any
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import structlog

log = structlog.get_logger()


class VectorStore:
    """
    Vector store interface using ChromaDB for semantic search.

    Features:
    - Persistent storage of embeddings
    - Semantic similarity search
    - Metadata filtering
    - Hybrid search (keyword + semantic)
    """

    def __init__(self,
                 persist_directory: str = "./chroma_db",
                 collection_name: str = "ai_news_articles"):
        """
        Initialize ChromaDB vector store.

        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection to use
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        log.info("Initializing ChromaDB vector store",
                persist_dir=persist_directory,
                collection=collection_name)

        try:
            # Initialize ChromaDB client with persistence
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # Cosine similarity
            )

            log.info("Vector store initialized successfully",
                    count=self.collection.count())

        except Exception as e:
            log.error("Failed to initialize vector store", error=str(e))
            raise

    def add_articles(self,
                    article_ids: List[str],
                    embeddings: List[List[float]],
                    documents: List[str],
                    metadatas: List[Dict[str, Any]]):
        """
        Add articles to the vector store.

        Args:
            article_ids: Unique IDs for articles
            embeddings: Embedding vectors
            documents: Text content for each article
            metadatas: Metadata dictionaries (title, url, type, etc.)
        """
        try:
            log.info(f"Adding {len(article_ids)} articles to vector store")

            self.collection.add(
                ids=article_ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )

            log.info(f"Successfully added articles",
                    count=len(article_ids),
                    total_articles=self.collection.count())

        except Exception as e:
            log.error("Failed to add articles", error=str(e))
            raise

    def add_article(self,
                   article_id: str,
                   embedding: List[float],
                   document: str,
                   metadata: Dict[str, Any]):
        """
        Add a single article to the vector store.

        Args:
            article_id: Unique ID for the article
            embedding: Embedding vector
            document: Text content
            metadata: Metadata dict (title, url, type, etc.)
        """
        self.add_articles(
            article_ids=[article_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata]
        )

    def search(self,
              query_embedding: List[float],
              n_results: int = 10,
              where: Optional[Dict[str, Any]] = None,
              where_document: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Semantic search using query embedding.

        Args:
            query_embedding: Query vector
            n_results: Number of results to return
            where: Metadata filter (e.g., {"article_type": "youtube"})
            where_document: Document content filter

        Returns:
            Dict with ids, distances, documents, and metadatas
        """
        try:
            log.info("Executing semantic search",
                    n_results=n_results,
                    filter=where)

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
                where_document=where_document
            )

            log.info(f"Search returned {len(results['ids'][0])} results")
            return self._format_results(results)

        except Exception as e:
            log.error("Search failed", error=str(e))
            raise

    def search_by_text(self,
                      query_text: str,
                      n_results: int = 10,
                      where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search using text query (will be embedded automatically).

        Args:
            query_text: Text query
            n_results: Number of results
            where: Metadata filter

        Returns:
            Search results
        """
        # ChromaDB will handle embedding automatically if we use query_texts
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )

            return self._format_results(results)

        except Exception as e:
            log.error("Text search failed", error=str(e))
            raise

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific article by ID.

        Args:
            article_id: Article ID

        Returns:
            Article data or None if not found
        """
        try:
            result = self.collection.get(
                ids=[article_id],
                include=["embeddings", "documents", "metadatas"]
            )

            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "document": result["documents"][0],
                    "metadata": result["metadatas"][0],
                    "embedding": result["embeddings"][0]
                }
            return None

        except Exception as e:
            log.error("Failed to get article", article_id=article_id, error=str(e))
            return None

    def delete_article(self, article_id: str):
        """Delete an article from the vector store."""
        try:
            self.collection.delete(ids=[article_id])
            log.info("Article deleted", article_id=article_id)
        except Exception as e:
            log.error("Failed to delete article", article_id=article_id, error=str(e))

    def count(self) -> int:
        """Get total number of articles in the store."""
        return self.collection.count()

    def reset(self):
        """Delete all articles from the collection."""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            log.info("Vector store reset")
        except Exception as e:
            log.error("Failed to reset vector store", error=str(e))

    def _format_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format ChromaDB results into a cleaner structure."""
        formatted = []

        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["ids"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None,
                "document": results["documents"][0][i] if "documents" in results else None,
                "metadata": results["metadatas"][0][i] if "metadatas" in results else None
            })

        return {
            "results": formatted,
            "count": len(formatted)
        }


# Singleton instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create singleton vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store


if __name__ == "__main__":
    # Test the vector store
    store = VectorStore(persist_directory="./test_chroma_db")

    # Test adding an article
    test_embedding = [0.1] * 384  # Dummy embedding
    store.add_article(
        article_id="test_1",
        embedding=test_embedding,
        document="Test article about AI and machine learning",
        metadata={
            "title": "Test Article",
            "article_type": "test",
            "url": "https://example.com"
        }
    )

    print(f"Total articles: {store.count()}")
