"""
AI News Aggregator - Streamlit Frontend

A beautiful, interactive dashboard for your AI news aggregator.

Pages:
- 🏠 Dashboard - Overview and stats
- 🔍 Search - Semantic search with RAG
- 📰 Digests - Recent AI summaries
- 🕷️ Scrape - Trigger scraping
- 🚀 Workflow - Run complete workflow
- ⚙️ Settings - Configuration
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="AI News Aggregator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .source-badge {
        background: #f0f2f6;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("# 🤖 AI News Aggregator")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "🔍 Search", "📰 Digests", "🕷️ Scrape", "🚀 Workflow", "📧 Email", "⚙️ Settings"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Actions")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()

if st.sidebar.button("📧 Send Email Now", use_container_width=True, type="primary"):
    st.switch_page("pages/email.py")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
**AI News Aggregator v2.0**

Intelligent news aggregation with:
- 23 Sources (3 YouTube + 20 Web)
- AI Summaries (Gemini)
- RAG Search (ChromaDB)
- Personalized Ranking
""")

# Load appropriate page
if page == "🏠 Dashboard":
    from pages import dashboard
    dashboard.show()
elif page == "🔍 Search":
    from pages import search
    search.show()
elif page == "📰 Digests":
    from pages import digests
    digests.show()
elif page == "🕷️ Scrape":
    from pages import scrape
    scrape.show()
elif page == "🚀 Workflow":
    from pages import workflow
    workflow.show()
elif page == "📧 Email":
    from pages import email
    email.show()
elif page == "⚙️ Settings":
    from pages import settings
    settings.show()
