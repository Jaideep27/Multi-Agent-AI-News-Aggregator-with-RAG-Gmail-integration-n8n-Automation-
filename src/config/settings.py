"""
Configuration management using Pydantic Settings.

Loads configuration from environment variables and .env files.
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with validation.

    Settings are loaded from environment variables and .env files.
    """

    # Application
    app_name: str = Field(default="AI News Aggregator", description="Application name")
    app_version: str = Field(default="2.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment (development/production)")
    debug: bool = Field(default=False, description="Debug mode")

    # API Keys
    gemini_api_key: str = Field(..., description="Google Gemini API key")

    # Email Configuration
    my_email: str = Field(..., description="Email address to send digests to")
    app_password: Optional[str] = Field(default=None, description="Gmail app password for SMTP")
    smtp_host: str = Field(default="smtp.gmail.com", description="SMTP server host")
    smtp_port: int = Field(default=587, description="SMTP server port")

    # Database Configuration
    postgres_user: str = Field(default="postgres", description="PostgreSQL username")
    postgres_password: str = Field(default="postgres", description="PostgreSQL password")
    postgres_db: str = Field(default="ai_news_aggregator", description="PostgreSQL database name")
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")

    # Redis Configuration (optional)
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")

    # ChromaDB Configuration
    chroma_persist_directory: str = Field(default="./chroma_db", description="ChromaDB persistence directory")
    chroma_collection_name: str = Field(default="ai_news_articles", description="ChromaDB collection name")

    # Embedding Configuration
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Sentence transformer model")
    embedding_dimension: int = Field(default=384, description="Embedding dimension")

    # Gemini Configuration
    gemini_model_digest: str = Field(default="gemini-2.5-flash", description="Gemini model for digests")
    gemini_model_curator: str = Field(default="gemini-2.5-flash", description="Gemini model for curation")
    gemini_model_email: str = Field(default="gemini-2.5-flash", description="Gemini model for emails")
    gemini_temperature_digest: float = Field(default=0.7, description="Temperature for digest generation")
    gemini_temperature_curator: float = Field(default=0.3, description="Temperature for curation")
    gemini_temperature_email: float = Field(default=0.7, description="Temperature for email generation")

    # YouTube Configuration - Only 3 channels
    youtube_channels: List[str] = Field(
        default=[
            "UCyR2Ct3pDOeZSRyZH5hPO-Q",  # Varun Mayya
            "UCNU_lfiiWBdtULKOw6X0Dig",  # Krish Naik
            "UCh9nVJoWXmFb7sLApWGcLPQ",  # Codebasics
        ],
        description="YouTube channel IDs to scrape"
    )

    # Workflow Configuration
    default_hours: int = Field(default=24, description="Default time window for scraping (hours)")
    default_top_n: int = Field(default=10, description="Default number of articles in digest")
    max_retries: int = Field(default=3, description="Maximum workflow retry attempts")

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json/text)")
    log_file: Optional[str] = Field(default="logs/app.log", description="Log file path")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="FastAPI host")
    api_port: int = Field(default=8000, description="FastAPI port")
    api_workers: int = Field(default=1, description="Number of API workers")
    api_cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins"
    )

    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @field_validator("gemini_api_key")
    @classmethod
    def validate_gemini_api_key(cls, v: str) -> str:
        """Validate Gemini API key is not empty."""
        if not v or v.strip() == "":
            raise ValueError("GEMINI_API_KEY must be set")
        return v

    @field_validator("my_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if not v or "@" not in v:
            raise ValueError("MY_EMAIL must be a valid email address")
        return v

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL."""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses LRU cache to ensure settings are loaded only once.
    """
    # Look for .env in root directory
    env_path = Path(".env")
    if env_path.exists():
        return Settings(_env_file=str(env_path))

    # Fall back to environment variables only
    return Settings()


# Global settings instance
settings = get_settings()
