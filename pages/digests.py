"""Digests page - View AI-generated summaries."""

import streamlit as st
from datetime import datetime
from src.database.repository import Repository


@st.cache_resource
def get_cached_repository():
    """Get database repository (cached)."""
    return Repository()


@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_recent_digests_cached(hours: int):
    """Get recent digests from database (cached)."""
    repo = get_cached_repository()
    return repo.get_recent_digests(hours=hours)


def show():
    """Display digests page."""
    st.markdown('<h1 class="main-header">📰 AI Digests</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">View AI-generated article summaries</p>', unsafe_allow_html=True)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        hours = st.selectbox(
            "⏱️ Time Period",
            [24, 72, 168, 720],
            index=2,
            format_func=lambda x: {
                24: "Last 24 hours",
                72: "Last 3 days",
                168: "Last week",
                720: "Last month"
            }[x]
        )

    with col2:
        limit = st.number_input(
            "📊 Max Results",
            min_value=5,
            max_value=100,
            value=20,
            step=5
        )

    with col3:
        filter_type = st.selectbox(
            "📂 Filter by Type",
            ["All", "official", "research", "news", "safety", "youtube"]
        )

    # Load digests (cached)
    digests = get_recent_digests_cached(hours=hours)

    # Apply type filter
    if filter_type != "All":
        digests = [d for d in digests if d['article_type'] == filter_type]

    # Limit results
    digests = digests[:limit]

    # Display stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    # Count by type
    type_counts = {}
    for d in digests:
        t = d['article_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    with col1:
        st.metric("📚 Total Digests", len(digests))

    with col2:
        official_count = type_counts.get('official', 0)
        st.metric("🏢 Official", official_count)

    with col3:
        research_count = type_counts.get('research', 0)
        st.metric("🔬 Research", research_count)

    with col4:
        news_count = type_counts.get('news', 0)
        st.metric("📰 News", news_count)

    st.markdown("---")

    if not digests:
        st.info("""
        ### No digests found

        **Possible reasons:**
        - No articles have been processed yet
        - Try expanding the time period
        - Run the workflow to generate new digests

        **Quick actions:**
        - Go to 🕷️ Scrape to collect articles
        - Go to 🚀 Workflow to process and generate summaries
        """)
        return

    # Display digests
    st.subheader(f"📋 {len(digests)} Digests Found")

    # Group by date
    by_date = {}
    for digest in digests:
        date_str = digest['created_at'].strftime('%Y-%m-%d')
        if date_str not in by_date:
            by_date[date_str] = []
        by_date[date_str].append(digest)

    # Display by date
    for date_str, date_digests in sorted(by_date.items(), reverse=True):
        st.markdown(f"### 📅 {date_str} ({len(date_digests)} articles)")

        for digest in date_digests:
            # Type emoji
            type_emoji = {
                'official': '🏢',
                'research': '🔬',
                'news': '📰',
                'safety': '🛡️',
                'youtube': '📺'
            }
            emoji = type_emoji.get(digest['article_type'], '📄')

            with st.expander(f"{emoji} {digest['title']}", expanded=False):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**Type:** `{digest['article_type']}`")

                with col2:
                    time_str = digest['created_at'].strftime('%H:%M')
                    st.markdown(f"**Time:** {time_str}")

                st.markdown("---")
                st.markdown("**📝 Summary:**")
                st.write(digest['summary'])

                st.markdown("---")
                st.markdown(f"[🔗 Read Full Article]({digest['url']})")

                # Copy summary button
                if st.button(f"📋 Copy Summary", key=f"copy_{digest['id']}"):
                    st.code(digest['summary'], language="text")
                    st.success("✅ Summary ready to copy!")

    # Export option
    st.markdown("---")
    st.subheader("💾 Export Digests")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Export as Markdown", use_container_width=True):
            markdown_content = f"# AI News Digests - {datetime.now().strftime('%Y-%m-%d')}\n\n"

            for date_str, date_digests in sorted(by_date.items(), reverse=True):
                markdown_content += f"## {date_str}\n\n"

                for digest in date_digests:
                    markdown_content += f"### {digest['title']}\n\n"
                    markdown_content += f"**Type:** {digest['article_type']}\n\n"
                    markdown_content += f"**Summary:** {digest['summary']}\n\n"
                    markdown_content += f"**Link:** {digest['url']}\n\n"
                    markdown_content += "---\n\n"

            st.download_button(
                label="⬇️ Download Markdown",
                data=markdown_content,
                file_name=f"ai_news_digests_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

    with col2:
        if st.button("📊 Export as JSON", use_container_width=True):
            import json

            export_data = []
            for digest in digests:
                export_data.append({
                    'title': digest['title'],
                    'type': digest['article_type'],
                    'summary': digest['summary'],
                    'url': digest['url'],
                    'created_at': digest['created_at'].isoformat()
                })

            json_content = json.dumps(export_data, indent=2)

            st.download_button(
                label="⬇️ Download JSON",
                data=json_content,
                file_name=f"ai_news_digests_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
