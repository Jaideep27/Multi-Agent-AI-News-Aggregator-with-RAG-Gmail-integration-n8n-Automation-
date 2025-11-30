"""Dashboard page - Overview and statistics."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

from src.config.settings import get_settings
from src.database.repository import Repository
from src.rag.retriever import get_article_retriever


@st.cache_resource
def get_cached_retriever():
    """Get article retriever (cached)."""
    try:
        return get_article_retriever()
    except Exception as e:
        st.warning(f"Could not load retriever: {e}")
        return None


@st.cache_resource
def get_cached_repository():
    """Get database repository (cached)."""
    return Repository()


@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_recent_digests_cached(hours: int):
    """Get recent digests from database (cached)."""
    repo = get_cached_repository()
    return repo.get_recent_digests(hours=hours)


@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_vector_count():
    """Get vector store article count (cached)."""
    retriever = get_cached_retriever()
    if retriever:
        return retriever.count_articles()
    return 0


def show():
    """Display dashboard page."""
    st.markdown('<h1 class="main-header">📊 Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">System Overview & Statistics</p>', unsafe_allow_html=True)

    # Get data (cached)
    settings = get_settings()
    vector_count = get_vector_count()
    digests = get_recent_digests_cached(hours=168)

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{vector_count}</div>
            <div class="stat-label">📚 Indexed Articles</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(digests)}</div>
            <div class="stat-label">📝 Weekly Digests</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">23</div>
            <div class="stat-label">🌐 Active Sources</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{settings.app_version}</div>
            <div class="stat-label">🚀 Version</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📈 Recent Activity")

        # Use already fetched weekly digests
        if digests:
            # Create daily counts
            df_data = []
            for digest in digests:
                df_data.append({
                    'date': digest['created_at'].date(),
                    'type': digest['article_type']
                })

            df = pd.DataFrame(df_data)
            daily_counts = df.groupby('date').size().reset_index(name='count')

            # Plot
            fig = px.bar(
                daily_counts,
                x='date',
                y='count',
                title='Articles Processed (Last 7 Days)',
                labels={'date': 'Date', 'count': 'Articles'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent activity. Run a workflow to see stats!")

    with col2:
        st.subheader("🗂️ Articles by Category")

        if digests:
            # Count by type
            type_counts = df.groupby('type').size().reset_index(name='count')

            # Map types to readable names
            type_map = {
                'official': '🏢 Official Blogs',
                'research': '🔬 Research Papers',
                'news': '📰 News Sites',
                'safety': '🛡️ AI Safety',
                'youtube': '📺 YouTube'
            }
            type_counts['label'] = type_counts['type'].map(type_map)

            # Pie chart
            fig = px.pie(
                type_counts,
                values='count',
                names='label',
                title='Distribution by Source Type',
                color_discrete_sequence=px.colors.sequential.Purples_r
            )
            fig.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available yet.")

    # System information
    st.markdown("---")
    st.subheader("⚙️ System Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🤖 AI Models**")
        st.code(f"""
Digest Generator: {settings.gemini_model_digest}
Article Curator:  {settings.gemini_model_curator}
Embedding Model:  {settings.embedding_model}
Vector Dimension: {settings.embedding_dimension}
        """, language="text")

    with col2:
        st.markdown("**💾 Data Storage**")
        st.code(f"""
Database:    {settings.postgres_db}
Host:        {settings.postgres_host}
Vector DB:   ChromaDB ({vector_count} articles)
Environment: {settings.environment}
        """, language="text")

    # Data sources
    st.markdown("---")
    st.subheader("📡 Data Sources (23 Total)")

    tab1, tab2 = st.tabs(["YouTube (3)", "Web Sources (20)"])

    with tab1:
        st.markdown("""
        <div style='padding: 1rem;'>
            <h4>YouTube Channels</h4>
            <span class="source-badge">📺 Varun Mayya - AI Tools & Entrepreneurship</span>
            <span class="source-badge">📺 Krish Naik - AI Tutorials & ML</span>
            <span class="source-badge">📺 Codebasics - Data Science & Python</span>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("**Official AI Blogs (9)**")
        st.markdown("""
        <span class="source-badge">OpenAI</span>
        <span class="source-badge">Anthropic</span>
        <span class="source-badge">Google DeepMind</span>
        <span class="source-badge">Google Research</span>
        <span class="source-badge">Meta AI</span>
        <span class="source-badge">Hugging Face</span>
        <span class="source-badge">EleutherAI</span>
        <span class="source-badge">Stability AI</span>
        <span class="source-badge">LAION AI</span>
        """, unsafe_allow_html=True)

        st.markdown("<br>**Research Papers (3)**", unsafe_allow_html=True)
        st.markdown("""
        <span class="source-badge">arXiv AI</span>
        <span class="source-badge">arXiv ML</span>
        <span class="source-badge">Papers With Code</span>
        """, unsafe_allow_html=True)

        st.markdown("<br>**AI News (5)**", unsafe_allow_html=True)
        st.markdown("""
        <span class="source-badge">VentureBeat</span>
        <span class="source-badge">TechCrunch</span>
        <span class="source-badge">MIT Tech Review</span>
        <span class="source-badge">The Decoder</span>
        <span class="source-badge">Ars Technica</span>
        """, unsafe_allow_html=True)

        st.markdown("<br>**AI Safety (3)**", unsafe_allow_html=True)
        st.markdown("""
        <span class="source-badge">Alignment Forum</span>
        <span class="source-badge">LessWrong</span>
        <span class="source-badge">Center for AI Safety</span>
        """, unsafe_allow_html=True)

    # Recent digests preview
    st.markdown("---")
    st.subheader("📰 Recent Digests Preview")

    # Filter to last 24 hours from already cached weekly digests
    now = datetime.now()
    cutoff = now - timedelta(hours=24)
    recent = [d for d in digests if d['created_at'] >= cutoff]

    if recent:
        for i, digest in enumerate(recent[:5]):
            with st.expander(f"📄 {digest['title'][:80]}..." if len(digest['title']) > 80 else f"📄 {digest['title']}"):
                st.markdown(f"**Type:** `{digest['article_type']}`")
                st.markdown(f"**Published:** {digest['created_at'].strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Summary:**\n{digest['summary']}")
                st.markdown(f"[🔗 Read More]({digest['url']})")
    else:
        st.info("No recent digests. Run the workflow to generate AI summaries!")
