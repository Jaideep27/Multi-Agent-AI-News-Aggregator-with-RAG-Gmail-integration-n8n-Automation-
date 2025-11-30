"""Workflow page - Run complete 6-stage workflow."""

import streamlit as st
from datetime import datetime
from src.workflows.workflow import run_workflow


def show():
    """Display workflow page."""
    st.markdown('<h1 class="main-header">🚀 Complete Workflow</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Run the full 6-stage AI news aggregation pipeline</p>', unsafe_allow_html=True)

    # Workflow diagram
    st.markdown("""
    ### 🔄 Workflow Stages

    ```
    1. 🕷️  Scraping      → Collect from 23 sources
    2. 🔧 Processing     → Get YouTube transcripts
    3. 📝 Digest         → Generate AI summaries (Gemini)
    4. 🗄️  RAG Indexing   → Index in ChromaDB
    5. 🎯 Ranking        → AI-powered curation
    6. 📧 Email          → Send personalized digest
    ```
    """)

    st.info("""
    **⏱️ Estimated Time:** 5-15 minutes (depending on number of articles)

    **Note:** This runs the COMPLETE pipeline. For just scraping, use the 🕷️ Scrape page.
    """)

    # Configuration
    st.markdown("---")
    st.subheader("⚙️ Workflow Configuration")

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
        top_n = st.number_input(
            "📊 Articles in Email",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            help="Number of top articles to include in email digest"
        )

    # Show what will happen
    st.markdown("---")
    st.subheader("📋 What Will Happen")

    with st.expander("🕷️ Stage 1: Scraping", expanded=True):
        st.markdown("""
        - Scrape 3 YouTube channels
        - Scrape 20 web sources (RSS + Crawl4AI)
        - Save raw articles to database
        - **Time:** ~2-3 minutes
        """)

    with st.expander("🔧 Stage 2: Processing"):
        st.markdown("""
        - Fetch YouTube transcripts (if missing)
        - Web articles already have content from Crawl4AI
        - **Time:** ~30-60 seconds
        """)

    with st.expander("📝 Stage 3: AI Digest Generation"):
        st.markdown("""
        - Use Gemini AI to generate summaries
        - Extract key points and insights
        - Save digests to database
        - **Time:** ~3-8 minutes (depends on article count)
        - **Note:** Limited by Gemini API quota (10 requests/minute for free tier)
        """)

    with st.expander("🗄️ Stage 4: RAG Indexing"):
        st.markdown("""
        - Generate embeddings using sentence-transformers
        - Index in ChromaDB vector database
        - Enable semantic search
        - **Time:** ~30-60 seconds
        """)

    with st.expander("🎯 Stage 5: Ranking"):
        st.markdown("""
        - Use Gemini AI to rank articles by relevance
        - Consider user preferences and interests
        - RAG-enhanced context from historical articles
        - **Time:** ~1-2 minutes
        """)

    with st.expander("📧 Stage 6: Email"):
        st.markdown("""
        - Generate personalized email content
        - Include top N ranked articles
        - Send via configured SMTP
        - **Time:** ~5-10 seconds
        """)

    st.markdown("---")

    # Run button
    if st.button("🚀 Run Complete Workflow", type="primary", use_container_width=True):
        # Progress tracking
        progress = st.progress(0)
        status = st.empty()
        stage_info = st.empty()

        try:
            # Run workflow
            status.markdown("### 🔄 Running Workflow...")

            # Create a placeholder for stage updates
            stage_container = st.container()

            with st.spinner("⏳ This may take 5-15 minutes..."):
                result = run_workflow(hours=hours, top_n=top_n)

            if result and result.get("success"):
                progress.progress(100)
                status.markdown("### ✅ Workflow Complete!")

                # Display results
                st.success("🎉 Workflow completed successfully!")

                st.markdown("---")
                st.subheader("📊 Workflow Results")

                # Metrics
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    articles_scraped = len(result.get("articles", []))
                    st.metric("📚 Articles Scraped", articles_scraped)

                with col2:
                    digests_created = len(result.get("digests", []))
                    st.metric("📝 Digests Created", digests_created)

                with col3:
                    articles_ranked = len(result.get("ranked_articles", []))
                    st.metric("🎯 Articles Ranked", articles_ranked)

                with col4:
                    email_sent = "✅" if result.get("success") else "❌"
                    st.metric("📧 Email Status", email_sent)

                # Top articles preview
                if result.get("ranked_articles"):
                    st.markdown("---")
                    st.subheader(f"🏆 Top {top_n} Articles (Sent in Email)")

                    for i, article in enumerate(result["ranked_articles"][:top_n], 1):
                        with st.expander(f"#{i} - {article['title']}", expanded=(i <= 3)):
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"**Relevance Score:** {article['relevance_score']:.1f}/10")

                            with col2:
                                st.markdown(f"**Rank:** #{article['rank']}")

                            st.markdown("---")
                            st.markdown("**📝 Summary:**")
                            st.write(article['summary'])

                            st.markdown("---")
                            st.markdown("**🤔 Why This Article?**")
                            st.info(article.get('reasoning', 'N/A'))

                            st.markdown(f"[🔗 Read Full Article]({article['url']})")

                # Next steps
                st.markdown("---")
                st.success(f"""
                ### ✅ Workflow Complete!

                **What happened:**
                - ✅ Scraped {articles_scraped} articles from 23 sources
                - ✅ Generated {digests_created} AI summaries
                - ✅ Ranked {articles_ranked} articles by relevance
                - ✅ Sent email with top {top_n} articles

                **Next steps:**
                - Check your email inbox for the digest
                - Go to **🔍 Search** to find specific topics
                - Go to **📰 Digests** to browse all summaries
                """)

            else:
                progress.progress(0)
                status.markdown("### ❌ Workflow Failed")
                st.error("Workflow did not complete successfully")

                if result:
                    errors = result.get("errors", [])
                    if errors:
                        st.markdown("---")
                        st.subheader("❌ Errors")
                        for error in errors:
                            st.error(f"**{error['stage']}:** {error['message']}")

        except Exception as e:
            progress.progress(0)
            status.markdown("### ❌ Workflow Failed")
            st.error(f"Error: {str(e)}")
            st.exception(e)

    # Tips
    st.markdown("---")
    with st.expander("💡 Workflow Tips"):
        st.markdown("""
        ### Best Practices

        **Daily Digest:**
        - Time Window: 24 hours
        - Top N: 5-10 articles
        - Run once per day

        **Weekly Digest:**
        - Time Window: 168 hours (1 week)
        - Top N: 10-15 articles
        - Run once per week

        **Monthly Review:**
        - Time Window: 720 hours (1 month)
        - Top N: 20-30 articles
        - Run once per month

        ### Performance Notes

        **Gemini API Limits (Free Tier):**
        - 10 requests per minute
        - If you have many articles, processing will be slower
        - Consider upgrading to paid tier for faster processing

        **What Can Go Wrong:**
        - ⚠️ Gemini API quota exceeded → Processing pauses and retries
        - ⚠️ Some sources may be temporarily unavailable
        - ⚠️ Email sending may fail if SMTP not configured

        ### Troubleshooting

        **If workflow fails:**
        1. Check your `.env` file for API keys
        2. Verify database is running
        3. Check Gemini API quota at https://ai.google.dev
        4. Try running just the scraper first to isolate issues
        """)
