"""Dependency injection for FastAPI routes."""

from typing import Generator
from sqlalchemy.orm import Session
from src.database.connection import get_session
from src.database.repository import Repository
from src.config.settings import Settings, get_settings
from src.rag.retriever import get_article_retriever


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database session.
    
    Yields:
        SQLAlchemy session
    """
    session = get_session()
    try:
        yield session
    finally:
        session.close()


def get_repository() -> Repository:
    """
    Dependency for repository instance.
        
    Returns:
        Repository instance
    """
    return Repository()


def get_app_settings() -> Settings:
    """
    Dependency for application settings.
    
    Returns:
        Settings instance
    """
    return get_settings()


def get_retriever():
    """
    Dependency for RAG retriever.
    
    Returns:
        Article retriever instance
    """
    return get_article_retriever()
