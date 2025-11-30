"""
Embedding Generation Module

Generates vector embeddings for articles using sentence-transformers.
Uses a lightweight model optimized for semantic search.
"""

import os
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import structlog

log = structlog.get_logger()


class EmbeddingGenerator:
    """
    Generates semantic embeddings for text using sentence-transformers.

    Uses 'all-MiniLM-L6-v2' model:
    - Fast inference (~5ms per sentence)
    - 384 dimensions
    - Good balance of speed and quality
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator.

        Args:
            model_name: HuggingFace model name for embeddings
        """
        self.model_name = model_name
        log.info(f"Loading embedding model: {model_name}")

        try:
            self.model = SentenceTransformer(model_name)
            log.info(f"Embedding model loaded successfully",
                    model=model_name,
                    dimensions=self.model.get_sentence_embedding_dimension())
        except Exception as e:
            log.error(f"Failed to load embedding model", error=str(e))
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            log.error(f"Failed to generate embedding", error=str(e))
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing).

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            log.info(f"Generating embeddings for {len(texts)} texts")
            embeddings = self.model.encode(texts,
                                          convert_to_numpy=True,
                                          show_progress_bar=True,
                                          batch_size=32)
            log.info(f"Generated {len(embeddings)} embeddings")
            return embeddings.tolist()
        except Exception as e:
            log.error(f"Failed to generate batch embeddings", error=str(e))
            raise

    def generate_article_embedding(self, title: str, summary: str, content: Optional[str] = None) -> List[float]:
        """
        Generate embedding for an article combining title, summary, and content.

        Args:
            title: Article title
            summary: Article summary
            content: Optional full content (truncated to 1000 chars)

        Returns:
            Combined embedding vector
        """
        # Combine text fields with appropriate weighting
        combined_text = f"{title}. {summary}"
        if content:
            # Truncate content to avoid overwhelming the embedding
            content_snippet = content[:1000]
            combined_text += f" {content_snippet}"

        return self.generate_embedding(combined_text)

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        return self.model.get_sentence_embedding_dimension()


# Singleton instance
_embedding_generator: Optional[EmbeddingGenerator] = None


def get_embedding_generator() -> EmbeddingGenerator:
    """Get or create singleton embedding generator instance."""
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator


if __name__ == "__main__":
    # Test the embedding generator
    generator = EmbeddingGenerator()

    test_text = "Google announces new AI model with improved performance"
    embedding = generator.generate_embedding(test_text)

    print(f"Text: {test_text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
