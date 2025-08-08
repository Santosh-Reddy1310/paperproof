import streamlit as st
import os
import time
from datetime import datetime
import concurrent.futures

# Page configuration early (still needed at top)
st.set_page_config(
    page_title="Research Paper Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (runs once)
st.markdown("""
<style>
.main-header { text-align: center; color: #1f77b4; padding: 1rem 0; }
.section-header { color: #ff7f0e; border-bottom: 2px solid #ff7f0e; padding-bottom: 0.5rem; }
.status-success { color: #2ca02c; font-weight: bold; }
.status-error { color: #d62728; font-weight: bold; }
.usage-warning { color: #ff7f0e; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

from utils.validators import InputValidator
from config import Config

@st.cache_resource
def get_api_client(api_key):
    """Cache Gemini API client for session"""
    from utils.api_client import GeminiClient
    return GeminiClient(api_key)

@st.cache_resource
def get_template():
    """Cache paper template to avoid reload"""
    from templates.paper_template import PaperTemplate
    return PaperTemplate()

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        "paper_generated": False,
        "generated_paper": "",
        "generation_progress": 0,
        "api_client": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def main():
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">🔬 Paper-Proof </h1>', unsafe_allow_html=True)
    st.markdown("Generate comprehensive academic research papers using Google's Gemini API")

    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="section-header">⚙️ Configuration</h2>', unsafe_allow_html=True)
        api_key = st.text_input(
            "🔑 Enter Your Gemini API Key",
            type="password",
            help="Get your free API key from: https://aistudio.google.com/app/apikey",
            placeholder="sk-...",
            key="user_api_key"
        )

        if not api_key:
            st.warning("Please enter your Gemini API key to proceed")
            st.stop()

        selected_model_name = st.selectbox(
            "AI Model", options=list(Config.AVAILABLE_MODELS.keys()), index=0
        )
        selected_model = Config.AVAILABLE_MODELS[selected_model_name]

        st.info(f"Selected: {selected_model_name}")
        st.success("Free tier limits: 60 requests/day, 30k tokens/minute")

        paper_type = st.selectbox(
            "Paper Type", ["Research Paper", "Review Paper", "Case Study", "Technical Report"]
        )
        target_length = st.slider(
            "Target Length (words)", Config.MIN_PAPER_LENGTH, Config.MAX_PAPER_LENGTH, 3000, 500
        )
        author_name = st.text_input("Author Name (optional)", value="AI Generated")

        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Creativity (Temperature)", 0.1, 1.0, 0.7, 0.1,
                help="Higher values make output more creative but less focused"
            )
            include_citations = st.checkbox("Include Citations", value=True)
            add_delays = st.checkbox("Add Delays Between Requests", value=True)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h2 class="section-header">📝 Paper Generation</h2>', unsafe_allow_html=True)
        research_topic = st.text_area(
            "Research Topic", height=100,
            placeholder="Enter your research topic here...",
            help="Be as specific and detailed as possible."
        )

        if st.button("🚀 Generate Research Paper", type="primary", use_container_width=True):
            valid, msg = InputValidator.validate_topic(research_topic)
            if not valid:
                st.error(f"Topic validation error: {msg}")
                return

            try:
                client = get_api_client(api_key)
                template = get_template()

                prompts = template.get_section_prompts(research_topic, paper_type.lower())
                sections = {}

                with st.spinner("Generating your research paper..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    start_time = time.time()

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        futures = {executor.submit(client.generate_content, prompts[s]): s for s in prompts}
                        for i, future in enumerate(concurrent.futures.as_completed(futures)):
                            s = futures[future]
                            sections[s] = future.result()
                            progress_bar.progress((i + 1) / len(prompts))
                            status_text.text(f"Finished: {s.replace('_', ' ').title()} "
                                             f"| Elapsed: {int(time.time() - start_time)}s")

                complete_paper = template.format_paper(sections, research_topic, author_name)

                st.session_state.generated_paper = complete_paper
                st.session_state.paper_generated = True
                progress_bar.progress(1.0)
                status_text.text("✅ Paper generation complete!")
                st.success("Research paper generated successfully!")
                time.sleep(1)
                st.rerun()

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    with col2:
        st.markdown('<h2 class="section-header">📊 Generation Status</h2>', unsafe_allow_html=True)
        if st.session_state.paper_generated:
            word_count = len(st.session_state.generated_paper.split())
            st.metric("Word Count", f"{word_count:,}")

            safe_topic = InputValidator.sanitize_filename(
                research_topic[:30] if research_topic else "research_paper"
            )
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            st.download_button(
                "📄 Download as Markdown", st.session_state.generated_paper,
                file_name=f"{safe_topic}_{timestamp}.md", mime="text/markdown", use_container_width=True
            )
            st.download_button(
                "📝 Download as Text", st.session_state.generated_paper,
                file_name=f"{safe_topic}_{timestamp}.txt", mime="text/plain", use_container_width=True
            )
        else:
            st.markdown('<p class="status-error">⏳ No paper generated yet</p>', unsafe_allow_html=True)
            st.info("Configure your settings and enter a research topic to generate a paper.")

    if st.session_state.paper_generated:
        st.markdown("---")
        st.markdown('<h2 class="section-header">📖 Generated Paper</h2>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📖 Formatted View", "🔧 Raw Markdown"])
        with tab1:
            st.markdown(st.session_state.generated_paper)
        with tab2:
            st.code(st.session_state.generated_paper, language="markdown")

        if st.button("🗑️ Clear Paper", type="secondary"):
            st.session_state.paper_generated = False
            st.session_state.generated_paper = ""
            st.rerun()

if __name__ == "__main__":
    main()
