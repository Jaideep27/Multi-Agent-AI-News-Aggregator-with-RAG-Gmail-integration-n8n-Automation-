"""Search page - Semantic search with RAG."""

import streamlit as st
from src.rag.retriever import get_article_retriever


@st.cache_resource
def get_cached_retriever():
    """Get article retriever (cached across all users)."""
    return get_article_retriever()


def show():
    """Display search page."""
    st.markdown('<h1 class="main-header">🔍 Semantic Search</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Search your AI news using vector similarity (RAG)</p>', unsafe_allow_html=True)

    # Initialize session state for search
    if 'search_triggered' not in st.session_state:
        st.session_state['search_triggered'] = False

    # Handle quick search query from session state
    default_query = st.session_state.pop('search_query', '')

    # Search interface
    col1, col2 = st.columns([3, 1])

    with col1:
        query = st.text_input(
            "🔎 Search Query",
            value=default_query,
            placeholder="e.g., GPT-5 reasoning capabilities, LLM safety research, AI alignment...",
            help="Enter any topic - the AI will find semantically similar articles",
            key="search_input"
        )

    with col2:
        num_results = st.number_input(
            "📊 Results",
            min_value=1,
            max_value=20,
            value=5,
            help="Number of results to return"
        )

    # Filter options
    col1, col2 = st.columns(2)

    with col1:
        article_type = st.selectbox(
            "📂 Filter by Type",
            ["All Types", "Official Blogs", "Research Papers", "News Sites", "AI Safety", "YouTube"],
            help="Filter results by source category"
        )

    type_map = {
        "All Types": None,
        "Official Blogs": "official",
        "Research Papers": "research",
        "News Sites": "news",
        "AI Safety": "safety",
        "YouTube": "youtube"
    }

    # Search button - only trigger on button click or when quick search is used
    search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

    # Trigger search if button clicked or if coming from quick search
    if search_clicked or (default_query and not st.session_state['search_triggered']):
        st.session_state['search_triggered'] = True

        if not query:
            st.warning("⚠️ Please enter a search query")
            st.session_state['search_triggered'] = False
            return

        with st.spinner("🔄 Searching with AI..."):
            try:
                retriever = get_cached_retriever()
                results = retriever.find_similar(
                    query=query,
                    n_results=num_results,
                    article_type=type_map[article_type]
                )

                if not results:
                    st.info("🤷 No results found. Try a different query or run the workflow to index more articles.")
                    return

                # Display results
                st.success(f"✅ Found {len(results)} relevant articles")
                st.markdown("---")

                for i, result in enumerate(results, 1):
                    metadata = result.get("metadata", {})
                    distance = result.get("distance", 0)
                    similarity = (1 - distance) * 100 if distance is not None else 0

                    # Result card
                    with st.container():
                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.markdown(f"### {i}. {metadata.get('title', 'N/A')}")

                        with col2:
                            st.metric("Relevance", f"{similarity:.0f}%")

                        # Type badge
                        article_type_str = metadata.get('article_type', 'unknown')
                        type_emoji = {
                            'official': '🏢',
                            'research': '🔬',
                            'news': '📰',
                            'safety': '🛡️',
                            'youtube': '📺'
                        }
                        emoji = type_emoji.get(article_type_str, '📄')

                        st.markdown(f"{emoji} **Type:** `{article_type_str}`")

                        # Summary
                        document = result.get("document", "")
                        if document:
                            with st.expander("📝 Summary"):
                                st.write(document)

                        # Link
                        url = metadata.get("url", "")
                        if url:
                            st.markdown(f"[🔗 Read Full Article]({url})")

                        st.markdown("---")

            except Exception as e:
                st.error(f"❌ Search failed: {str(e)}")
                st.exception(e)
            finally:
                # Reset search trigger to prevent auto-rerun
                st.session_state['search_triggered'] = False

    # Search tips
    with st.expander("💡 Search Tips"):
        st.markdown("""
        ### How Semantic Search Works

        This search uses **vector similarity (RAG)** powered by AI embeddings:

        - **Not just keywords**: Understands meaning and context
        - **Semantic matching**: Finds related concepts even with different words
        - **AI-powered**: Uses sentence transformers for understanding

        ### Example Queries

        ✅ **Good queries:**
        - "Large language model reasoning capabilities"
        - "AI safety and alignment research"
        - "GPT-5 multimodal features"
        - "Transformer architecture improvements"

        ✅ **What makes it better than keyword search:**
        - Query: "LLM thinking" → Finds articles about "reasoning", "chain of thought", etc.
        - Query: "AI dangers" → Finds articles about "safety", "alignment", "risks", etc.

        ### Tips for Best Results

        1. **Be specific**: "GPT-4 vision capabilities" > "AI images"
        2. **Use full phrases**: "neural network training techniques" > "training"
        3. **Natural language**: Write like you're asking a person
        4. **Try variations**: If first search doesn't work, rephrase
        """)

    # Quick search examples
    st.markdown("### 🎯 Quick Search Examples")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 LLM Reasoning", use_container_width=True):
            st.session_state['search_query'] = "large language model reasoning and chain of thought"
            st.session_state['search_triggered'] = False
            st.rerun()

    with col2:
        if st.button("🛡️ AI Safety", use_container_width=True):
            st.session_state['search_query'] = "AI safety alignment and risks"
            st.session_state['search_triggered'] = False
            st.rerun()

    with col3:
        if st.button("🔬 Research Papers", use_container_width=True):
            st.session_state['search_query'] = "recent AI research breakthroughs"
            st.session_state['search_triggered'] = False
            st.rerun()
