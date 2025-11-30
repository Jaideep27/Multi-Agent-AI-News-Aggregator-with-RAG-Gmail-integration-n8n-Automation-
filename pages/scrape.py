"""Scrape page - Trigger article scraping."""

import streamlit as st
from datetime import datetime
from src.core.runner import run_scrapers


def show():
    """Display scrape page."""
    st.markdown('<h1 class="main-header">🕷️ Scrape Articles</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Collect fresh articles from 23 sources</p>', unsafe_allow_html=True)

    # Information about sources
    st.info("""
    ### 📡 Data Sources (23 Total)

    **3 YouTube Channels:**
    - Varun Mayya (AI Tools & Entrepreneurship)
    - Krish Naik (AI Tutorials & ML)
    - Codebasics (Data Science & Python)

    **20 Web Sources:**
    - 9 Official AI Blogs (OpenAI, Anthropic, DeepMind, Google Research, Meta AI, Hugging Face, EleutherAI, Stability AI, LAION)
    - 3 Research (arXiv AI, arXiv ML, Papers With Code)
    - 5 News (VentureBeat, TechCrunch, MIT Tech Review, The Decoder, Ars Technica)
    - 3 AI Safety (Alignment Forum, LessWrong, Center for AI Safety)
    """)

    # Configuration
    st.markdown("---")
    st.subheader("⚙️ Scrape Configuration")

    col1, col2 = st.columns(2)

    with col1:
        hours = st.selectbox(
            "⏱️ Time Window",
            [24, 72, 168, 720],
            index=2,
            format_func=lambda x: {
                24: "Last 24 hours (1 day)",
                72: "Last 72 hours (3 days)",
                168: "Last 168 hours (1 week)",
                720: "Last 720 hours (1 month)"
            }[x],
            help="How far back to scrape articles"
        )

    with col2:
        st.markdown("**⏱️ Estimated Time**")
        st.code("""
YouTube (3):  ~10-15 seconds
Web RSS (17): ~30-40 seconds
Web Crawl (3): ~60-90 seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total:        ~2-3 minutes
        """, language="text")

    st.markdown("---")

    # Scrape button
    if st.button("🚀 Start Scraping", type="primary", use_container_width=True):
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Start scraping
            status_text.text("🔄 Starting scraper...")
            progress_bar.progress(10)

            with st.spinner("🕷️ Scraping articles from 23 sources..."):
                results = run_scrapers(hours=hours)

            progress_bar.progress(100)
            status_text.text("✅ Scraping complete!")

            # Display results
            st.success("🎉 Successfully scraped articles!")

            st.markdown("---")
            st.subheader("📊 Scraping Results")

            # Summary metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                youtube_count = len(results.get("youtube", []))
                st.metric(
                    "📺 YouTube Videos",
                    youtube_count,
                    delta=f"+{youtube_count}" if youtube_count > 0 else None
                )

            with col2:
                web_count = len(results.get("web", []))
                st.metric(
                    "🌐 Web Articles",
                    web_count,
                    delta=f"+{web_count}" if web_count > 0 else None
                )

            with col3:
                total = results.get("total", 0)
                st.metric(
                    "📚 Total Articles",
                    total,
                    delta=f"+{total}" if total > 0 else None
                )

            # Detailed breakdown
            if results.get("web"):
                st.markdown("---")
                st.subheader("🌐 Web Articles Breakdown")

                # Count by category
                by_category = {}
                for article in results["web"]:
                    cat = article.category
                    by_category[cat] = by_category.get(cat, 0) + 1

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("🏢 Official", by_category.get('official', 0))
                with col2:
                    st.metric("🔬 Research", by_category.get('research', 0))
                with col3:
                    st.metric("📰 News", by_category.get('news', 0))
                with col4:
                    st.metric("🛡️ Safety", by_category.get('safety', 0))

            # Sample articles
            if results.get("youtube") or results.get("web"):
                st.markdown("---")
                st.subheader("📋 Sample Articles")

                # Show first few YouTube
                if results.get("youtube"):
                    st.markdown("**📺 YouTube Videos:**")
                    for video in results["youtube"][:3]:
                        with st.expander(f"▶️ {video.title}"):
                            st.write(f"**Video ID:** {video.video_id}")
                            st.write(f"**Published:** {video.published_at}")
                            st.write(f"**URL:** {video.url}")
                            if video.description:
                                st.write(f"**Description:** {video.description[:200]}...")

                # Show first few web
                if results.get("web"):
                    st.markdown("**🌐 Web Articles:**")
                    for article in results["web"][:5]:
                        emoji = {
                            'official': '🏢',
                            'research': '🔬',
                            'news': '📰',
                            'safety': '🛡️'
                        }.get(article.category, '📄')

                        with st.expander(f"{emoji} {article.title}"):
                            st.write(f"**Source:** {article.source_name}")
                            st.write(f"**Category:** {article.category}")
                            st.write(f"**Published:** {article.published_at}")
                            st.write(f"**URL:** {article.url}")

            # Next steps
            st.markdown("---")
            st.success("""
            ### ✅ Scraping Complete!

            **Next Steps:**
            1. Go to **🚀 Workflow** to process articles and generate AI summaries
            2. Or wait and scraping will happen automatically during the next workflow run

            **Note:** These articles are now in your database but haven't been processed by AI yet.
            """)

        except Exception as e:
            progress_bar.progress(0)
            status_text.text("❌ Scraping failed")
            st.error(f"Error: {str(e)}")
            st.exception(e)

    # Tips
    st.markdown("---")
    with st.expander("💡 Scraping Tips"):
        st.markdown("""
        ### When to Scrape

        - **Daily**: Use 24 hours for daily updates
        - **Weekly**: Use 168 hours (1 week) for weekly digests
        - **Monthly**: Use 720 hours (1 month) for comprehensive reviews

        ### What Happens During Scraping

        1. **YouTube (RSS)**: Fast RSS feed parsing for 3 channels
        2. **Web (RSS)**: Quick RSS parsing for 17 sources
        3. **Web (Crawl)**: Browser-based scraping for 3 sources (EleutherAI, Stability AI, Center for AI Safety)

        ### After Scraping

        Articles are saved to your PostgreSQL database but are NOT yet:
        - ❌ Processed by AI
        - ❌ Indexed in vector database
        - ❌ Ranked or curated

        To do that, run the **complete workflow** from the 🚀 Workflow page.

        ### Performance

        - Scraping is **fast** (~2-3 minutes for all 23 sources)
        - No AI processing, just data collection
        - Duplicate articles are automatically skipped
        """)
