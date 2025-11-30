"""Settings page - Configuration and system info."""

import streamlit as st
import os
from src.config.settings import get_settings


@st.cache_resource
def get_cached_repository():
    """Get database repository (cached)."""
    from src.database.repository import Repository
    return Repository()


@st.cache_resource
def get_cached_retriever():
    """Get article retriever (cached)."""
    from src.rag.retriever import get_article_retriever
    return get_article_retriever()


def show():
    """Display settings page."""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">System configuration and environment</p>', unsafe_allow_html=True)

    settings = get_settings()

    # Environment info
    st.subheader("🌍 Environment")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Application**")
        st.code(f"""
Name:        {settings.app_name}
Version:     {settings.app_version}
Environment: {settings.environment}
Debug:       {settings.debug}
        """, language="text")

    with col2:
        st.markdown("**Runtime**")
        st.code(f"""
Python:      {os.sys.version.split()[0]}
Platform:    {os.sys.platform}
Working Dir: {os.getcwd()[:40]}...
        """, language="text")

    # AI Models
    st.markdown("---")
    st.subheader("🤖 AI Models Configuration")

    tab1, tab2 = st.tabs(["Gemini AI", "Embeddings"])

    with tab1:
        st.markdown("**Google Gemini Configuration**")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Digest Generator**")
            st.code(f"""
Model:       {settings.gemini_model_digest}
Temperature: 0.5
Purpose:     Generate article summaries
            """, language="text")

        with col2:
            st.markdown("**Article Curator**")
            st.code(f"""
Model:       {settings.gemini_model_curator}
Temperature: 0.3
Purpose:     Rank and curate articles
            """, language="text")

        # API Key status
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            st.success(f"✅ API Key configured: {api_key[:10]}...{api_key[-4:]}")
            st.info("""
            **Free Tier Limits:**
            - 10 requests per minute
            - Monitor usage at: https://ai.google.dev/gemini-api/docs/rate-limits
            """)
        else:
            st.error("❌ GEMINI_API_KEY not found in environment")

    with tab2:
        st.markdown("**Sentence Transformers Configuration**")

        st.code(f"""
Model:      {settings.embedding_model}
Dimension:  {settings.embedding_dimension}
Device:     CPU (automatic)
Purpose:    Generate embeddings for semantic search
        """, language="text")

        st.info("""
        **About Embeddings:**
        - Model: all-MiniLM-L6-v2 from Hugging Face
        - Creates 384-dimensional vectors
        - Fast and efficient for semantic search
        - Runs locally (no API calls needed)
        """)

    # Database Configuration
    st.markdown("---")
    st.subheader("💾 Database Configuration")

    tab1, tab2 = st.tabs(["PostgreSQL", "ChromaDB"])

    with tab1:
        st.markdown("**PostgreSQL Connection**")

        st.code(f"""
Host:     {settings.postgres_host}
Port:     {settings.postgres_port}
Database: {settings.postgres_db}
User:     {settings.postgres_user}
        """, language="text")

        # Test connection
        if st.button("🔌 Test PostgreSQL Connection"):
            try:
                repo = get_cached_repository()
                st.success("✅ Database connection successful!")

                # Show table info
                digests = repo.get_recent_digests(hours=1)
                st.info(f"Database is healthy. Found {len(digests)} recent digests.")

            except Exception as e:
                st.error(f"❌ Database connection failed: {str(e)}")

    with tab2:
        st.markdown("**ChromaDB (Vector Store)**")

        st.code(f"""
Directory: {settings.chroma_persist_directory}
Collection: ai_news_articles
Purpose: Semantic search with RAG
        """, language="text")

        # Test ChromaDB
        if st.button("🔌 Test ChromaDB Connection"):
            try:
                retriever = get_cached_retriever()
                count = retriever.count_articles()
                st.success(f"✅ ChromaDB connection successful! {count} articles indexed.")

            except Exception as e:
                st.error(f"❌ ChromaDB connection failed: {str(e)}")

    # Email Configuration
    st.markdown("---")
    st.subheader("📧 Email Configuration")

    st.code(f"""
SMTP Host:     {settings.smtp_host}
SMTP Port:     {settings.smtp_port}
Email:         {settings.my_email}
Use TLS:       Yes (Port 587)
    """, language="text")

    app_password = os.getenv("APP_PASSWORD", "")
    if app_password:
        st.success(f"✅ Gmail App Password configured")
    else:
        st.warning("⚠️ APP_PASSWORD not found in environment")
        st.info("""
        **To set up Gmail App Password:**
        1. Go to Google Account Settings
        2. Enable 2-Factor Authentication
        3. Go to "App Passwords"
        4. Generate password for "Mail"
        5. Copy to APP_PASSWORD in .env
        """)

    # API Configuration
    st.markdown("---")
    st.subheader("🌐 API Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**FastAPI (REST)**")
        st.code(f"""
Host:    {settings.api_host}
Port:    {settings.api_port}
Workers: {settings.api_workers}
CORS:    Enabled
        """, language="text")

        if st.button("🔗 Open Swagger UI"):
            import webbrowser
            webbrowser.open("http://localhost:8000/docs")

    with col2:
        st.markdown("**FastMCP (AI Tools)**")
        st.code("""
Transport: stdio
Protocol:  JSON-RPC
Tools:     5 available
Status:    Ready
        """, language="text")

        if st.button("📖 View MCP Docs"):
            st.info("See MCP_SETUP.md for configuration instructions")

    # Workflow Settings
    st.markdown("---")
    st.subheader("🚀 Workflow Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Default Parameters**")
        st.code(f"""
Time Window: {settings.default_hours} hours
Top N:       {settings.default_top_n} articles
Max Retries: {settings.max_retries}
        """, language="text")

    with col2:
        st.markdown("**Logging**")
        st.code(f"""
Log Level:  {settings.log_level}
Format:     Structured (structlog)
Output:     Console
        """, language="text")

    # Data Sources
    st.markdown("---")
    st.subheader("📡 Data Sources")

    tab1, tab2 = st.tabs(["YouTube", "Web"])

    with tab1:
        st.markdown("**YouTube Channels (3)**")

        channels = settings.youtube_channels
        for i, channel_id in enumerate(channels, 1):
            channel_names = {
                "UCyR2Ct3pDOeZSRyZH5hPO-Q": "Varun Mayya",
                "UCNU_lfiiWBdtULKOw6X0Dig": "Krish Naik",
                "UCh9nVJoWXmFb7sLApWGcLPQ": "Codebasics"
            }
            name = channel_names.get(channel_id, "Unknown")

            st.markdown(f"**{i}. {name}**")
            st.code(f"Channel ID: {channel_id}")
            st.markdown(f"[🔗 Visit Channel](https://youtube.com/channel/{channel_id})")

    with tab2:
        st.markdown("**Web Sources (20)**")

        from src.config.web_sources import ALL_WEB_SOURCES

        for i, source in enumerate(ALL_WEB_SOURCES, 1):
            with st.expander(f"{i}. {source.name} - {source.category}"):
                st.markdown(f"**URL:** {source.url}")
                st.markdown(f"**Category:** `{source.category}`")
                st.markdown(f"**Scrape Type:** `{source.scrape_type}`")
                if source.rss_url:
                    st.markdown(f"**RSS URL:** {source.rss_url}")
                st.markdown(f"**Description:** {source.description}")

    # Environment Variables
    st.markdown("---")
    with st.expander("🔐 Environment Variables (.env file)"):
        st.warning("⚠️ Sensitive information - be careful!")

        env_vars = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "Not set"),
            "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "Not set"),
            "POSTGRES_PORT": os.getenv("POSTGRES_PORT", "Not set"),
            "POSTGRES_DB": os.getenv("POSTGRES_DB", "Not set"),
            "POSTGRES_USER": os.getenv("POSTGRES_USER", "Not set"),
            "SMTP_HOST": os.getenv("SMTP_HOST", "Not set"),
            "SMTP_PORT": os.getenv("SMTP_PORT", "Not set"),
            "MY_EMAIL": os.getenv("MY_EMAIL", "Not set"),
            "APP_PASSWORD": os.getenv("APP_PASSWORD", "Not set"),
        }

        for key, value in env_vars.items():
            if "KEY" in key or "PASSWORD" in key:
                # Mask sensitive values
                if value and value != "Not set":
                    masked = f"{value[:4]}...{value[-4:]}"
                    st.code(f"{key}={masked}")
                else:
                    st.code(f"{key}={value}")
            else:
                st.code(f"{key}={value}")

    # Actions
    st.markdown("---")
    st.subheader("🔧 System Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Reload Configuration", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("✅ Configuration reloaded!")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear Caches", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("✅ Caches cleared!")
