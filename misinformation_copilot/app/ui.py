"""Streamlit dashboard for Misinformation Debunking Copilot"""

import streamlit as st
import time
import webbrowser
from pathlib import Path
from datetime import datetime
import pyperclip

from .config import Config, SCREENSHOTS_DIR
from .storage import get_storage
from .collector import collect_posts
from .drafting import generate_drafts


# Page config
st.set_page_config(
    page_title="Misinformation Debunking Copilot",
    page_icon="🔍",
    layout="wide"
)


def init_session_state():
    """Initialize session state variables"""
    if 'selected_post_id' not in st.session_state:
        st.session_state.selected_post_id = None
    if 'generated_drafts' not in st.session_state:
        st.session_state.generated_drafts = None
    if 'filter_status' not in st.session_state:
        st.session_state.filter_status = 'queued'
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ''


def main():
    """Main application"""
    init_session_state()

    st.title("🔍 Misinformation Debunking Copilot")
    st.caption("Human-in-the-loop fact-checking assistant")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🎯 Collection", "📈 Statistics", "⚙️ Configuration"],
            label_visibility="collapsed"
        )

        st.divider()

        # LLM Status
        llm_config = Config.get_llm_config()
        if llm_config['enabled']:
            st.success(f"✓ LLM: {llm_config['provider']}")
        else:
            st.warning("⚠ LLM: Mock mode")

        # Quick stats
        storage = get_storage()
        stats = storage.get_stats()
        st.metric("Total Posts", stats['total'])
        st.metric("Queued", stats['by_status'].get('queued', 0))
        st.metric("High Risk", stats['score_distribution'].get('high', 0))

    # Main content
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🎯 Collection":
        show_collection()
    elif page == "📈 Statistics":
        show_statistics()
    elif page == "⚙️ Configuration":
        show_configuration()


def show_dashboard():
    """Main dashboard view"""
    st.header("Post Review Dashboard")

    storage = get_storage()

    # Filters
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "queued", "done", "skip", "needs_research"],
            index=1
        )

    with col2:
        score_filter = st.selectbox(
            "Score Range",
            ["All", "High (70+)", "Medium (40-69)", "Low (<40)", "Unscored"],
        )

    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["collected_at", "misinfo_score", "id"],
            format_func=lambda x: {
                'collected_at': 'Date Collected',
                'misinfo_score': 'Misinfo Score',
                'id': 'ID'
            }[x]
        )

    with col4:
        search = st.text_input("🔍 Search", placeholder="Search text...")

    # Apply filters
    filter_kwargs = {
        'order_by': sort_by,
        'order_dir': 'DESC'
    }

    if status_filter != "All":
        filter_kwargs['status'] = status_filter

    if score_filter == "High (70+)":
        filter_kwargs['min_score'] = 70
    elif score_filter == "Medium (40-69)":
        filter_kwargs['min_score'] = 40
        filter_kwargs['max_score'] = 69
    elif score_filter == "Low (<40)":
        filter_kwargs['max_score'] = 39

    if search:
        filter_kwargs['search_term'] = search

    posts = storage.get_posts(**filter_kwargs)

    st.write(f"Found {len(posts)} posts")

    # Posts list
    if posts:
        for post in posts:
            show_post_card(post, storage)
    else:
        st.info("No posts found. Try adjusting filters or collect some posts.")


def show_post_card(post, storage):
    """Display a post card with actions"""
    post_id = post['id']

    # Determine score color
    score = post.get('misinfo_score', 0)
    if score >= 70:
        score_color = "🔴"
    elif score >= 40:
        score_color = "🟡"
    else:
        score_color = "🟢"

    with st.expander(
        f"{score_color} **{post.get('author', 'Unknown')}** | Score: {score or 'N/A'} | {post.get('target_name', '')}",
        expanded=(st.session_state.selected_post_id == post_id)
    ):
        col1, col2 = st.columns([1, 2])

        with col1:
            # Screenshot
            if post.get('screenshot_path'):
                screenshot_file = SCREENSHOTS_DIR / post['screenshot_path']
                if screenshot_file.exists():
                    st.image(str(screenshot_file), use_container_width=True)
                else:
                    st.warning("Screenshot not found")
            else:
                st.info("No screenshot")

            # Metadata
            st.caption(f"**ID:** {post_id}")
            st.caption(f"**Status:** {post.get('status', 'queued')}")
            st.caption(f"**Collected:** {post.get('collected_at', 'N/A')[:16]}")

        with col2:
            # Post content
            st.subheader("Post Content")
            st.write(post.get('text_content', '')[:500])
            if len(post.get('text_content', '')) > 500:
                with st.expander("Show full text"):
                    st.write(post.get('text_content', ''))

            # Analysis
            if post.get('misinfo_score'):
                st.divider()
                st.subheader("Analysis")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Misinfo Score", f"{score}/100")
                with col_b:
                    tags = post.get('tags', [])
                    if tags:
                        st.write("**Tags:**")
                        st.write(", ".join(tags))

                if post.get('rationale'):
                    st.write("**Rationale:**", post['rationale'])

                if post.get('fact_check_questions'):
                    st.write("**Fact-Check Questions:**")
                    for q in post['fact_check_questions']:
                        st.write(f"- {q}")

            # Actions
            st.divider()
            action_cols = st.columns(5)

            with action_cols[0]:
                if st.button("📝 Generate Drafts", key=f"gen_{post_id}"):
                    generate_drafts_for_post(post, storage)

            with action_cols[1]:
                if post.get('url'):
                    if st.button("🔗 Open Post", key=f"open_{post_id}"):
                        webbrowser.open(post['url'])
                        st.success("Opening in browser...")

            with action_cols[2]:
                if st.button("✅ Done", key=f"done_{post_id}"):
                    storage.update_post(post_id, status='done')
                    st.rerun()

            with action_cols[3]:
                if st.button("⏭ Skip", key=f"skip_{post_id}"):
                    storage.update_post(post_id, status='skip')
                    st.rerun()

            with action_cols[4]:
                if st.button("🔬 Needs Research", key=f"research_{post_id}"):
                    storage.update_post(post_id, status='needs_research')
                    st.rerun()

            # Show drafts if generated
            if post.get('drafts'):
                st.divider()
                st.subheader("Generated Rebuttals")
                drafts = post['drafts']

                for i, draft in enumerate(drafts, 1):
                    style = ["Short Punchy", "Factual Calm", "Snarky"][i - 1]
                    st.write(f"**Draft {i}: {style}**")
                    st.info(draft)
                    if st.button(f"📋 Copy Draft {i}", key=f"copy_{post_id}_{i}"):
                        try:
                            pyperclip.copy(draft)
                            st.success(f"Draft {i} copied to clipboard!")
                        except:
                            st.error("Clipboard access failed. Copy manually:")
                            st.code(draft)


def generate_drafts_for_post(post, storage):
    """Generate rebuttal drafts for a post"""
    with st.spinner("Generating drafts..."):
        try:
            drafts = generate_drafts(
                post.get('text_content', ''),
                post.get('tags', []),
                post.get('rationale', '')
            )

            storage.update_post(post['id'], drafts=drafts)
            st.success("Drafts generated!")
            st.rerun()

        except Exception as e:
            st.error(f"Failed to generate drafts: {e}")


def show_collection():
    """Collection interface"""
    st.header("Post Collection")

    # Load targets
    targets = Config.load_targets()

    st.subheader("Collection Settings")

    col1, col2 = st.columns(2)

    with col1:
        scroll_passes = st.slider(
            "Scroll Passes",
            min_value=1,
            max_value=10,
            value=Config.DEFAULT_SCROLL_PASSES,
            help="Number of times to scroll down the page"
        )

        max_posts = st.number_input(
            "Max Posts per Target",
            min_value=1,
            max_value=100,
            value=Config.DEFAULT_MAX_POSTS_PER_TARGET
        )

    with col2:
        scroll_delay = st.slider(
            "Scroll Delay (seconds)",
            min_value=0.5,
            max_value=10.0,
            value=float(Config.DEFAULT_SCROLL_DELAY),
            step=0.5,
            help="Delay between scrolls - higher is slower but more reliable"
        )

        max_targets = st.number_input(
            "Max Targets per Run",
            min_value=1,
            max_value=20,
            value=Config.DEFAULT_MAX_TARGETS_PER_RUN
        )

    headless = st.checkbox("Run browser in background (headless)", value=False)

    st.divider()

    # Targets management
    st.subheader("Targets")

    if targets:
        st.write(f"Loaded {len(targets)} targets:")

        for i, target in enumerate(targets[:max_targets]):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{target['name']}**")
            with col2:
                st.caption(target.get('type', 'page'))
            with col3:
                st.caption(f"[View]({target['url']})")

        if len(targets) > max_targets:
            st.info(f"Showing first {max_targets} targets. {len(targets) - max_targets} more available.")
    else:
        st.warning("No targets configured. Please add targets in Configuration.")

    st.divider()

    # Collection button
    if st.button("🚀 Start Collection", type="primary", disabled=len(targets) == 0):
        run_collection(targets[:max_targets], max_posts, scroll_passes, scroll_delay, headless)


def run_collection(targets, max_posts, scroll_passes, scroll_delay, headless):
    """Run the collection process"""
    progress_text = st.empty()
    progress_bar = st.progress(0)

    def progress_callback(msg):
        progress_text.text(msg)

    try:
        stats = collect_posts(
            targets=targets,
            max_posts_per_target=max_posts,
            scroll_passes=scroll_passes,
            scroll_delay=scroll_delay,
            headless=headless,
            progress_callback=progress_callback
        )

        progress_bar.progress(100)
        st.success(f"✅ Collection complete! Collected {stats['posts_collected']} posts from {stats['targets_processed']} targets.")

        if stats['errors']:
            with st.expander("⚠️ View Errors"):
                for error in stats['errors']:
                    st.error(error)

    except Exception as e:
        st.error(f"Collection failed: {e}")
        import traceback
        st.code(traceback.format_exc())


def show_statistics():
    """Statistics view"""
    st.header("Statistics")

    storage = get_storage()
    stats = storage.get_stats()

    # Overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Posts", stats['total'])
    with col2:
        st.metric("Queued", stats['by_status'].get('queued', 0))
    with col3:
        st.metric("Done", stats['by_status'].get('done', 0))
    with col4:
        st.metric("Needs Research", stats['by_status'].get('needs_research', 0))

    st.divider()

    # Score distribution
    st.subheader("Misinfo Score Distribution")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🔴 High (70+)", stats['score_distribution']['high'])
    with col2:
        st.metric("🟡 Medium (40-69)", stats['score_distribution']['medium'])
    with col3:
        st.metric("🟢 Low (<40)", stats['score_distribution']['low'])
    with col4:
        st.metric("⚪ Unscored", stats['score_distribution']['unscored'])

    st.divider()

    # Export
    st.subheader("Export Data")

    export_status = st.selectbox(
        "Export posts with status",
        ["All", "queued", "done", "skip", "needs_research"]
    )

    if st.button("📥 Export to CSV"):
        filter_kwargs = {}
        if export_status != "All":
            filter_kwargs['status'] = export_status

        posts = storage.get_posts(**filter_kwargs)

        if posts:
            output_file = Path(f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            storage.export_to_csv(posts, output_file)
            st.success(f"Exported {len(posts)} posts to {output_file}")

            with open(output_file, 'r', encoding='utf-8') as f:
                st.download_button(
                    "💾 Download CSV",
                    data=f.read(),
                    file_name=output_file.name,
                    mime='text/csv'
                )
        else:
            st.warning("No posts to export")


def show_configuration():
    """Configuration view"""
    st.header("Configuration")

    # Targets editor
    st.subheader("Targets Configuration")

    targets = Config.load_targets()

    # Add new target
    with st.expander("➕ Add New Target"):
        with st.form("add_target"):
            new_name = st.text_input("Target Name", placeholder="e.g., Climate Denial Watch")
            new_url = st.text_input("Facebook URL", placeholder="https://www.facebook.com/...")
            new_type = st.selectbox("Type", ["page", "group", "search"])

            if st.form_submit_button("Add Target"):
                if new_name and new_url:
                    targets.append({
                        'name': new_name,
                        'url': new_url,
                        'type': new_type
                    })
                    Config.save_targets(targets)
                    st.success(f"Added target: {new_name}")
                    st.rerun()
                else:
                    st.error("Please provide both name and URL")

    # List existing targets
    if targets:
        st.write("**Existing Targets:**")

        for i, target in enumerate(targets):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(f"{i+1}. **{target['name']}**")
            with col2:
                st.caption(target['type'])
            with col3:
                if st.button("🗑️", key=f"del_{i}"):
                    targets.pop(i)
                    Config.save_targets(targets)
                    st.rerun()

    st.divider()

    # LLM Configuration
    st.subheader("LLM Configuration")

    st.info("Configure LLM settings in the .env file. Restart the app after changes.")

    llm_config = Config.get_llm_config()

    st.write(f"**Current Provider:** {llm_config['provider']}")
    st.write(f"**Status:** {'✅ Enabled' if llm_config['enabled'] else '❌ Disabled'}")

    if llm_config['provider'] != 'mock':
        st.code(f"""
# Example .env configuration
LLM_PROVIDER={llm_config['provider']}
# Add your API keys
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
        """)

    st.divider()

    # About
    st.subheader("About")
    st.write("""
    **Misinformation Debunking Copilot** v1.0.0

    This tool assists with fact-checking workflows by:
    - Collecting posts from Facebook (with YOUR login)
    - Scoring posts for misinformation likelihood
    - Generating rebuttal drafts in multiple styles

    **IMPORTANT:** This tool does NOT auto-post. You maintain full control.
    All comments must be manually reviewed and posted by you.
    """)

    st.warning("""
    ⚠️ **Usage Guidelines:**
    - Only use on content you have permission to analyze
    - Do not use for harassment or coordinated attacks
    - Verify all facts before posting rebuttals
    - Respect platform terms of service
    - Use delays to avoid appearing as automation
    """)


if __name__ == "__main__":
    main()
