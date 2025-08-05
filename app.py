import streamlit as st
import time
from datetime import datetime
import concurrent.futures
import os
from utils.api_client import GeminiClient
from templates.paper_template import PaperTemplate
from utils.validators import InputValidator
from config import Config

# Page configuration
st.set_page_config(
    page_title="Research Paper Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f77b4;
    padding: 1rem 0;
}
.section-header {
    color: #ff7f0e;
    border-bottom: 2px solid #ff7f0e;
    padding-bottom: 0.5rem;
}
.status-success {
    color: #2ca02c;
    font-weight: bold;
}
.status-error {
    color: #d62728;
    font-weight: bold;
}
.usage-warning {
    color: #ff7f0e;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'paper_generated' not in st.session_state:
        st.session_state.paper_generated = False
    if 'generated_paper' not in st.session_state:
        st.session_state.generated_paper = ""
    if 'generation_progress' not in st.session_state:
        st.session_state.generation_progress = 0
    if 'api_client' not in st.session_state:
        st.session_state.api_client = None

def main():
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🔬 Research Paper Generator (Gemini)</h1>', 
                unsafe_allow_html=True)
    st.markdown("Generate comprehensive academic research papers using Google's Gemini API")
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown('<h2 class="section-header">⚙️ Configuration</h2>', 
                    unsafe_allow_html=True)
        
        # API Key input
        # In the sidebar section:
        api_key = st.text_input(
            "🔑 Enter Your Gemini API Key",
            type="password",
            help="Get your free API key from: https://aistudio.google.com/app/apikey",
            placeholder="sk-...",  # Gemini keys typically start with 'sk-'
            key="user_api_key"  # Store in session state
        )
        # In app.py, before using the key:
        if "user_api_key" in st.session_state:
            os.environ["GEMINI_API_KEY"] = st.session_state.user_api_key  # Temporary usage
        
        # Add validation if not api_key:
        if not api_key:
            st.warning("Please enter your Gemini API key to proceed")
            st.stop()  # Halt execution if no key provided
        # Model selection
        selected_model_name = st.selectbox(
            "AI Model",
            options=list(Config.AVAILABLE_MODELS.keys()),
            index=0  # Default to Gemini Pro
        )
        selected_model = Config.AVAILABLE_MODELS[selected_model_name]
        
        # Show model info
        st.info(f"Selected: {selected_model_name}")
        st.success("Free tier limits: 60 requests/day, 30k tokens/minute")
        
        # Paper parameters
        st.markdown("### Paper Parameters")
        
        paper_type = st.selectbox(
            "Paper Type",
            ["Research Paper", "Review Paper", "Case Study", "Technical Report"]
        )
        
        target_length = st.slider(
            "Target Length (words)",
            min_value=Config.MIN_PAPER_LENGTH,
            max_value=Config.MAX_PAPER_LENGTH,
            value=3000,
            step=500
        )
        
        author_name = st.text_input(
            "Author Name (optional)",
            value="AI Generated"
        )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Creativity (Temperature)",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make output more creative but less focused"
            )
            
            include_citations = st.checkbox(
                "Include Citations",
                value=True,
                help="Generate realistic academic citations"
            )
            
            add_delays = st.checkbox(
                "Add Delays Between Requests",
                value=True,
                help="Recommended for free tier to avoid rate limits"
            )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">📝 Paper Generation</h2>', 
                    unsafe_allow_html=True)
        
        # Topic input
        research_topic = st.text_area(
            "Research Topic",
            height=100,
            placeholder="Enter your research topic here. Be specific and detailed for better results.\n\nExample: 'The Impact of Artificial Intelligence on Healthcare Diagnosis: A Systematic Review of Machine Learning Applications in Medical Imaging'",
            help="Provide a clear, specific research topic. The more detailed, the better the generated paper."
        )
        
        # Generate button
        if st.button("🚀 Generate Research Paper", type="primary", use_container_width=True):
            topic_valid, topic_message = InputValidator.validate_topic(research_topic)
            if not topic_valid:
                st.error(f"Topic validation error: {topic_message}")
                return
            
            # Initialize API client
            try:
                client = GeminiClient(api_key)
                st.session_state.api_client = client
                template = PaperTemplate()
                
                # Generate paper
                with st.spinner("Generating your research paper..."):
                    # Get section prompts
                    prompts = template.get_section_prompts(research_topic, paper_type.lower())
                    sections = {}
                    
                    # Replace your generation loop with:
                    with st.spinner("Generating..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        start_time = time.time()

                        # Process all sections concurrently
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            futures = {
                                executor.submit(
                                    client.generate_content,
                                    prompts[section]
                                ): section
                                for section in prompts
                            }

                            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                                section = futures[future]
                                sections[section] = future.result()
                                progress = (i + 1) / len(prompts)
                                progress_bar.progress(progress)
                                status_text.text(f"Finished: {section.replace('_', ' ').title()} | "
                                                f"Elapsed: {int(time.time() - start_time)}s")
                    
                    # Format complete paper
                    status_text.text("Formatting paper...")
                    complete_paper = template.format_paper(
                        sections, 
                        research_topic, 
                        author_name
                    )
                    
                    # Store in session state
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
        st.markdown('<h2 class="section-header">📊 Generation Status</h2>', 
                    unsafe_allow_html=True)
        
        # Show API usage stats
        if st.session_state.api_client:
            usage = st.session_state.api_client.get_usage_stats()
            st.metric("Remaining Requests Today", 
                     f"{usage['remaining_requests']}/{usage['daily_limit']}")
            
            if usage['remaining_requests'] < 10:
                st.markdown('<p class="usage-warning">⚠️ Few requests remaining today</p>', 
                           unsafe_allow_html=True)
        
        if st.session_state.paper_generated:
            st.markdown('<p class="status-success">✅ Paper Ready</p>', 
                       unsafe_allow_html=True)
            
            # Word count
            word_count = len(st.session_state.generated_paper.split())
            st.metric("Word Count", f"{word_count:,}")
            
            # Download options
            st.markdown("### 📥 Download Options")
            
            # Prepare filename
            safe_topic = InputValidator.sanitize_filename(research_topic[:30] if research_topic else "research_paper")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Markdown download
            st.download_button(
                label="📄 Download as Markdown",
                data=st.session_state.generated_paper,
                file_name=f"{safe_topic}_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
            # Text download
            st.download_button(
                label="📝 Download as Text",
                data=st.session_state.generated_paper,
                file_name=f"{safe_topic}_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        else:
            st.markdown('<p class="status-error">⏳ No paper generated yet</p>', 
                       unsafe_allow_html=True)
            st.info("Configure your settings and enter a research topic to generate a paper.")
    
    # Display generated paper
    if st.session_state.paper_generated:
        st.markdown("---")
        st.markdown('<h2 class="section-header">📖 Generated Paper</h2>', 
                    unsafe_allow_html=True)
        
        # Paper preview with tabs
        tab1, tab2 = st.tabs(["📖 Formatted View", "🔧 Raw Markdown"])
        
        with tab1:
            st.markdown(st.session_state.generated_paper)
        
        with tab2:
            st.code(st.session_state.generated_paper, language="markdown")
        
        # Clear paper button
        if st.button("🗑️ Clear Paper", type="secondary"):
            st.session_state.paper_generated = False
            st.session_state.generated_paper = ""
            st.rerun()

if __name__ == "__main__":
    main()