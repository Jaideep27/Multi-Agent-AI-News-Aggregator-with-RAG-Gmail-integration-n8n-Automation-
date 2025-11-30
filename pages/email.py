"""Email page - Send AI news digest emails on-demand."""

import streamlit as st
import requests
from datetime import datetime, timedelta
from src.database.repository import Repository


@st.cache_resource
def get_cached_repository():
    """Get database repository (cached)."""
    return Repository()


@st.cache_data(ttl=60)
def get_recent_digests_cached(hours: int):
    """Get recent digests from database (cached for 60 seconds)."""
    try:
        repo = get_cached_repository()
        return repo.get_recent_digests(hours=hours)
    except Exception as e:
        st.error(f"Database error: {e}")
        return []


def show():
    """Display email page."""
    st.markdown('<h1 class="main-header">📧 Email Digest</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Send AI news digest emails on-demand</p>', unsafe_allow_html=True)

    st.info("""
    **📨 Send Email Features:**
    - ✅ Send digest immediately with custom parameters
    - ✅ Preview articles before sending
    - ✅ Customize time window and article count
    - ✅ Track email history

    **Note:** FastAPI must be running on port 8000 for this feature to work.
    """)

    # Configuration
    st.markdown("---")
    st.subheader("⚙️ Email Configuration")

    col1, col2 = st.columns(2)

    with col1:
        hours = st.selectbox(
            "⏱️ Time Window",
            [1, 6, 12, 24, 48, 72, 168],
            index=3,
            format_func=lambda x: {
                1: "Last 1 hour",
                6: "Last 6 hours",
                12: "Last 12 hours",
                24: "Last 24 hours (1 day)",
                48: "Last 48 hours (2 days)",
                72: "Last 72 hours (3 days)",
                168: "Last 168 hours (1 week)"
            }[x],
            help="How far back to include articles"
        )

    with col2:
        top_n = st.number_input(
            "📊 Number of Articles",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            help="How many top articles to include in email"
        )

    # Optional custom recipient
    with st.expander("🔧 Advanced Options"):
        custom_recipient = st.text_input(
            "📬 Custom Recipient (Optional)",
            placeholder="Leave empty to use MY_EMAIL from .env",
            help="Override the default recipient email"
        )

        custom_subject = st.text_input(
            "📝 Custom Subject (Optional)",
            placeholder="Leave empty for default subject",
            help="Custom email subject line"
        )

    # Preview articles
    st.markdown("---")
    st.subheader("📋 Preview Articles")

    # Use cached function to avoid slow page loads
    with st.spinner("Loading articles..."):
        digests = get_recent_digests_cached(hours=hours)

    if digests:
        preview_digests = digests[:top_n]

        st.success(f"✅ Found {len(digests)} digests. Top {len(preview_digests)} will be sent:")

        # Show preview
        for i, digest in enumerate(preview_digests, 1):
            type_emoji = {
                'official': '🏢',
                'research': '🔬',
                'news': '📰',
                'safety': '🛡️',
                'youtube': '📺'
            }.get(digest['article_type'], '📄')

            with st.expander(f"{type_emoji} #{i} - {digest['title'][:60]}...", expanded=(i <= 3)):
                st.markdown(f"**Type:** `{digest['article_type']}`")
                st.markdown(f"**Published:** {digest['created_at'].strftime('%Y-%m-%d %H:%M')}")
                st.markdown("**Summary:**")
                st.write(digest['summary'])
                st.markdown(f"[🔗 Read Full Article]({digest['url']})")
    else:
        st.warning(f"⚠️ No digests found in the last {hours} hours.")
        st.info("""
        **To generate digests:**
        1. Go to the 🚀 Workflow page
        2. Run the complete workflow
        3. Come back here to send email
        """)

    # Send Email Button
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        send_button = st.button(
            "📧 Send Email Now",
            type="primary",
            use_container_width=True,
            disabled=(len(digests) == 0)
        )

    if send_button:
        # Show loading
        with st.spinner("📤 Sending email..."):
            try:
                # Prepare request
                payload = {
                    "hours": hours,
                    "top_n": top_n
                }

                if custom_recipient:
                    payload["recipient"] = custom_recipient

                if custom_subject:
                    payload["subject"] = custom_subject

                # Call FastAPI endpoint
                response = requests.post(
                    "http://localhost:8000/api/v1/email/send",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success(f"""
                    ### ✅ Email Sent Successfully!

                    **Recipient:** {result['recipient']}
                    **Articles Sent:** {result['articles_count']}
                    **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                    Check your inbox! 📬
                    """)

                    # Confetti effect
                    st.balloons()

                elif response.status_code == 404:
                    st.error("❌ No digests found. Run the workflow first to generate articles.")

                elif response.status_code == 400:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Configuration Error: {error_detail}")

                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("""
                ### ❌ Connection Error

                **FastAPI server is not running!**

                **To fix:**
                1. Open a terminal
                2. Run: `python main.py`
                3. Wait for "Application startup complete"
                4. Try sending email again

                **FastAPI should be running on:** http://localhost:8000
                """)

            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Email might still be sending...")

            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

    # Email History (show last sent)
    st.markdown("---")
    with st.expander("📜 About Email Digest"):
        st.markdown("""
        ### 📧 Email Features

        **What's Included:**
        - AI-generated personalized greeting
        - Top N ranked articles with summaries
        - Direct links to full articles
        - Beautiful HTML formatting
        - Mobile-responsive design

        **Automatic Scheduling:**
        - Use **n8n** for automated hourly/daily emails
        - See `n8n_workflows/` for templates
        - Run `n8n start` and import the workflow

        **Manual vs Scheduled:**
        - **This page:** Send email RIGHT NOW
        - **n8n workflow:** Send automatically on schedule
        - **Both use the same FastAPI endpoint**

        ### 🔧 Configuration

        Email settings are in `.env`:
        ```
        MY_EMAIL=your-email@gmail.com
        APP_PASSWORD=your-gmail-app-password
        ```

        **Gmail Users:**
        - Use [App Password](https://myaccount.google.com/apppasswords)
        - Not your regular Gmail password
        - Must have 2FA enabled

        ### 📊 Email Format

        **Subject:** `🤖 AI News Digest - Top {N} Articles`

        **Content:**
        1. Personalized greeting with date
        2. Brief overview of articles
        3. Each article with:
           - Title
           - AI-generated summary
           - Read more link
        4. Beautiful HTML styling
        """)

    # Tips
    st.markdown("---")
    with st.expander("💡 Email Tips"):
        st.markdown("""
        ### Best Practices

        **Daily Digest:**
        - Time Window: 24 hours
        - Articles: 5-10
        - Good for: Staying up-to-date daily

        **Weekly Summary:**
        - Time Window: 168 hours (1 week)
        - Articles: 10-20
        - Good for: Weekly roundup

        **Breaking News:**
        - Time Window: 1-6 hours
        - Articles: 3-5
        - Good for: Urgent updates

        ### Automation with n8n

        **Hourly (Recommended):**
        ```
        1. Import: n8n_workflows/hourly_email_digest.json
        2. Activate workflow
        3. Emails sent every hour automatically
        ```

        **Custom Schedule:**
        - Edit cron expression in n8n
        - Examples:
          - `0 8 * * *` = Daily at 8 AM
          - `0 */2 * * *` = Every 2 hours
          - `0 9 * * 1-5` = Weekdays at 9 AM

        ### Troubleshooting

        **"FastAPI not running":**
        ```bash
        python main.py
        # Visit: http://localhost:8000/docs
        ```

        **"No digests found":**
        ```bash
        python cli.py run --hours 168
        # Or use Streamlit Workflow page
        ```

        **"Email not received":**
        1. Check spam folder
        2. Verify MY_EMAIL in .env
        3. Check APP_PASSWORD is correct
        4. Try Gmail App Password
        """)
