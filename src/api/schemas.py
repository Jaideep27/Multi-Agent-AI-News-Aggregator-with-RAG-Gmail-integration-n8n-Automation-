"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Health Check
class HealthResponse(BaseModel):
    status: str = Field(default="healthy")
    timestamp: datetime
    version: str


# Scraping
class ScrapeRequest(BaseModel):
    hours: int = Field(default=24, ge=1, le=168, description="Time window in hours (1-168)")


class ScrapeResponse(BaseModel):
    success: bool
    youtube_count: int
    web_count: int
    total_count: int
    message: str


# Workflow
class WorkflowRequest(BaseModel):
    hours: int = Field(default=24, ge=1, le=168, description="Time window in hours")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of top articles")
    skip_email: bool = Field(default=False, description="Skip email delivery")


class WorkflowResponse(BaseModel):
    success: bool
    articles_scraped: int
    digests_created: int
    articles_ranked: int
    email_sent: bool
    message: str
    errors: List[str] = []


# Digests
class DigestResponse(BaseModel):
    id: str
    article_type: str
    article_id: str
    url: str
    title: str
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True


class DigestsListResponse(BaseModel):
    digests: List[DigestResponse]
    total: int
    page: int
    page_size: int


# Search
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    n_results: int = Field(default=5, ge=1, le=50, description="Number of results")
    article_type: Optional[str] = Field(default=None, description="Filter by article type")


class SearchResultItem(BaseModel):
    title: str
    url: str
    article_type: str
    similarity: float
    summary: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResultItem]
    total: int


# Articles
class ArticleResponse(BaseModel):
    id: str
    title: str
    url: str
    published_at: datetime
    source: str
    description: Optional[str] = None


class ArticlesListResponse(BaseModel):
    articles: List[ArticleResponse]
    total: int
    source_type: str


# Statistics
class SourceStats(BaseModel):
    youtube_videos: int
    web_articles: int
    total_digests: int
    vector_store_count: int


class StatsResponse(BaseModel):
    sources: SourceStats
    database_status: str
    vector_store_status: str
    gemini_model: str
    embedding_model: str
    last_updated: datetime


# Email
class SendEmailRequest(BaseModel):
    hours: int = Field(default=24, ge=1, le=720, description="Time window in hours (1-720)")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of top articles to include")
    recipient: Optional[str] = Field(default=None, description="Recipient email (defaults to configured MY_EMAIL)")
    subject: Optional[str] = Field(default=None, description="Custom email subject (optional)")


class SendEmailResponse(BaseModel):
    success: bool
    message: str
    articles_count: int
    recipient: str
    sent_at: datetime
