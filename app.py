"""
AI-Powered Research Assistant - Premium Pastel UI Edition
Modern, sleek, and professional design
"""

import streamlit as st
from datetime import datetime
import time
import hashlib
from pathlib import Path
import json

# Try to import PDF library
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Import agent
try:
    from agent import ResearchAgent
    AGENT_AVAILABLE = True
except ImportError as e:
    AGENT_AVAILABLE = False
    st.error(f"Agent import error: {e}")

# Page configuration
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Pastel CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #f8f9fc 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 35%, #f093fb 70%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        animation: fadeInDown 0.8s ease;
    }
    
    .sub-header {
        text-align: center;
        color: #8898aa;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        font-weight: 400;
        animation: fadeInUp 0.8s ease;
    }
    
    /* Gradient border card */
    .gradient-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .gradient-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.2);
    }
    
    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fc 100%);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.15);
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #8898aa;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fc 100%);
        border-radius: 20px;
        padding: 1.8rem;
        margin-top: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Secondary button */
    .secondary-btn > button {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        color: #8898aa;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Input fields */
    .stTextArea textarea, .stTextInput input {
        border-radius: 16px !important;
        border: 2px solid rgba(102, 126, 234, 0.1) !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .stSidebar {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fc 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #fae8ff 100%);
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        color: #2d5016;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Divider */
    .custom-divider {
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, #f093fb, transparent);
        height: 2px;
        margin: 1.5rem 0;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
        animation: pulse 1.5s ease infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* Metric cards grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #8898aa;
        font-size: 0.85rem;
        border-top: 1px solid rgba(102, 126, 234, 0.1);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""
if 'papers_list' not in st.session_state:
    st.session_state.papers_list = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'summaries': 0,
        'extractions': 0,
        'comparisons': 0,
        'gaps': 0
    }
if 'theme' not in st.session_state:
    st.session_state.theme = 'pastel'

# Initialize agent function
def init_agent():
    if not AGENT_AVAILABLE:
        st.error("Cannot initialize agent")
        return False
    
    if st.session_state.agent is None:
        with st.spinner("✨ Initializing AI Agent..."):
            try:
                st.session_state.agent = ResearchAgent(use_gemini=True)
                return True
            except Exception as e:
                st.error(f"Failed to initialize: {str(e)}")
                return False
    return True

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">✨</div>
            <div style="font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ResearchMind AI</div>
            <div style="font-size: 0.8rem; color: #8898aa; margin-top: 0.3rem;">Academic Intelligence</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize button
    if st.button("🚀 Activate AI", use_container_width=True):
        if init_agent():
            st.success("✅ Agent Ready!")
            st.balloons()
    
    st.markdown("---")
    
    # Stats section
    st.markdown("### 📊 Performance")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-value">{st.session_state.stats['summaries']}</div>
                <div class="stat-label">Summaries</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🔍</div>
                <div class="stat-value">{st.session_state.stats['extractions']}</div>
                <div class="stat-label">Extractions</div>
            </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{st.session_state.stats['comparisons']}</div>
                <div class="stat-label">Comparisons</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">{st.session_state.stats['gaps']}</div>
                <div class="stat-label">Gap Analyses</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick tips
    with st.expander("💡 Pro Tips", expanded=False):
        st.markdown("""
            • **Summaries**: Get concise paper overviews
            • **Extractions**: Extract methodology, results, limitations
            • **Comparisons**: Compare 2+ papers side by side
            • **Q&A**: Ask specific questions about the paper
            • **Gap Analysis**: Identify research opportunities
        """)
    
    st.markdown("---")
    
    # About
    with st.expander("🎓 About", expanded=False):
        st.markdown("""
            **ResearchMind AI**  
            *Academic Research Assistant*
            
            **Author:** Faraiha Tariq  
            **Department:** Software Engineering  
            **University:** UET Taxila  
            
            *Empowering researchers with AI-powered literature analysis*
        """)
    
    st.markdown("---")
    st.caption("✨ AI-Powered Research Assistant")

# Main content
st.markdown("""
    <div class="main-header">
        ResearchMind AI
        <span class="badge">BETA</span>
    </div>
    <div class="sub-header">
        Intelligent Academic Literature Analysis • Summarize • Compare • Discover
    </div>
""", unsafe_allow_html=True)

# Status indicator
if st.session_state.agent is None:
    st.markdown("""
        <div class="info-box" style="text-align: center;">
            ✨ <strong>Ready to begin?</strong> Click "Activate AI" in the sidebar to start your research journey.
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="success-message">
            ✅ AI Agent Active • Ready to analyze research papers
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "✨ Paper Analysis", 
    "🔬 Compare Papers", 
    "🎯 Discovery Hub",
    "📜 History"
])

# ==================== TAB 1: Paper Analysis ====================
with tab1:
    st.markdown("### 📄 Input Research Material")
    
    # Input method with icons
    input_method = st.radio(
        "Select input method",
        ["✏️ Paste Text", "📎 Upload PDF", "🎯 Sample Paper"],
        horizontal=True
    )
    
    # Text input
    if input_method == "✏️ Paste Text":
        st.session_state.current_text = st.text_area(
            "",
            height=280,
            placeholder="✨ Paste your research paper content here...\n\nSupports: Abstracts, Introductions, Full Papers, etc.",
            help="Paste any academic text for AI analysis"
        )
    
    # PDF upload
    elif input_method == "📎 Upload PDF":
        if PDF_AVAILABLE:
            uploaded_file = st.file_uploader("", type=['pdf'], label_visibility="collapsed")
            if uploaded_file is not None:
                with st.spinner("📖 Extracting text from PDF..."):
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() or ""
                        st.session_state.current_text = text
                        st.success(f"✅ Successfully extracted {len(text)} characters")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.warning("PDF support coming soon")
    
    # Sample paper
    elif input_method == "🎯 Sample Paper":
        sample_text = """🎯 **Sample Research Paper**

**Title:** A Novel Deep Learning Approach for Medical Image Segmentation

**Abstract:** Medical image segmentation is crucial for diagnosis and treatment planning. This paper proposes a novel attention-based U-Net architecture for improved segmentation accuracy. The model incorporates spatial attention mechanisms to focus on relevant regions and channel attention to weigh feature importance.

**Key Contributions:**
1. Novel attention mechanism for medical images
2. 40% reduction in computational requirements
3. State-of-the-art results on multiple datasets

**Methodology:** The AttnU-Net extends standard U-Net with dual attention modules, trained using Dice loss and focal loss with Adam optimizer.

**Results:** Dice scores of 92.3% (BraTS), 91.7% (ISIC), and 94.1% (DRIVE), with 35% reduction in false positives.

**Limitations:** Reduced performance on images with severe artifacts; requires larger datasets for rare conditions.

**Future Work:** Semi-supervised learning and domain adaptation techniques."""
        
        if st.button("📋 Load Example Paper", use_container_width=True):
            st.session_state.current_text = sample_text
            st.success("✅ Sample loaded! Scroll down to analyze")
            st.balloons()
    
    # Document stats
    if st.session_state.current_text:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            word_count = len(st.session_state.current_text.split())
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">📝</div>
                    <div class="stat-value">{word_count}</div>
                    <div class="stat-label">Words</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            char_count = len(st.session_state.current_text)
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">📄</div>
                    <div class="stat-value">{char_count}</div>
                    <div class="stat-label">Characters</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            sentences = st.session_state.current_text.count('.')
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">📊</div>
                    <div class="stat-value">{sentences}</div>
                    <div class="stat-label">Sentences</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            est_pages = max(1, word_count // 300)
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">📚</div>
                    <div class="stat-value">{est_pages}</div>
                    <div class="stat-label">Est. Pages</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔬 Analysis Tools")
        
        # Action buttons in grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✨ Generate Summary", use_container_width=True):
                if st.session_state.agent:
                    with st.spinner("🤖 Generating intelligent summary..."):
                        try:
                            start_time = time.time()
                            result = st.session_state.agent.process(
                                st.session_state.current_text, 
                                task="summarize"
                            )
                            end_time = time.time()
                            
                            st.markdown("### ✨ AI-Generated Summary")
                            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                            st.caption(f"⏱️ Generated in {end_time - start_time:.2f} seconds")
                            
                            st.session_state.stats['summaries'] += 1
                            
                            st.session_state.history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'type': 'Summary',
                                'preview': st.session_state.current_text[:100],
                                'result': result[:500]
                            })
                            
                            st.download_button(
                                label="📥 Download Summary",
                                data=result,
                                file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please activate AI first!")
        
        with col2:
            if st.button("🔍 Extract Insights", use_container_width=True):
                if st.session_state.agent:
                    with st.spinner("🔍 Extracting key insights..."):
                        try:
                            start_time = time.time()
                            result = st.session_state.agent.process(
                                st.session_state.current_text, 
                                task="extract"
                            )
                            end_time = time.time()
                            
                            st.markdown("### 🔍 Extracted Insights")
                            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                            st.caption(f"⏱️ Generated in {end_time - start_time:.2f} seconds")
                            
                            st.session_state.stats['extractions'] += 1
                            
                            st.session_state.history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'type': 'Extraction',
                                'preview': st.session_state.current_text[:100],
                                'result': result[:500]
                            })
                            
                            st.download_button(
                                label="📥 Download Insights",
                                data=result,
                                file_name=f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please activate AI first!")
        
        with col3:
            if st.button("💬 Ask Questions", use_container_width=True):
                st.session_state.show_qa = True
        
        # Q&A Section
        if st.session_state.get('show_qa', False):
            st.markdown("---")
            st.markdown("### 💬 Interactive Q&A")
            
            question = st.text_input(
                "Ask anything about this paper:",
                placeholder="e.g., What methodology was used? What are the main contributions?",
                key="qa_input"
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if question and st.button("🔍 Ask", use_container_width=True):
                    with st.spinner("🤔 Finding answer..."):
                        try:
                            result = st.session_state.agent.process(
                                st.session_state.current_text,
                                task="qa",
                                question=question
                            )
                            st.markdown(f'<div class="result-box"><strong>💡 Answer:</strong><br><br>{result}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            if st.button("✖️ Close Q&A"):
                st.session_state.show_qa = False
                st.rerun()
        
        # Add to comparison button
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("📚 Add to Comparison Queue", use_container_width=True):
                if st.session_state.current_text not in st.session_state.papers_list:
                    st.session_state.papers_list.append(st.session_state.current_text)
                    st.success(f"✅ Added to queue ({len(st.session_state.papers_list)} papers)")
                    st.balloons()

# ==================== TAB 2: Compare Papers ====================
with tab2:
    st.markdown("### 🔬 Multi-Paper Comparison")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📚 Comparison Queue")
        if st.session_state.papers_list:
            for i, paper in enumerate(st.session_state.papers_list):
                with st.expander(f"📄 Paper {i+1} - {len(paper)} characters"):
                    st.text(paper[:200] + "...")
                    if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.papers_list.pop(i)
                        st.rerun()
        else:
            st.info("✨ Queue is empty. Add papers using the 'Add to Comparison Queue' button in the Analysis tab.")
    
    with col2:
        st.markdown("#### 🎯 Quick Actions")
        if st.session_state.current_text:
            if st.button("➕ Add Current Paper", use_container_width=True):
                if st.session_state.current_text not in st.session_state.papers_list:
                    st.session_state.papers_list.append(st.session_state.current_text)
                    st.success(f"✅ Added ({len(st.session_state.papers_list)} total)")
                    st.rerun()
        
        if len(st.session_state.papers_list) >= 2:
            if st.button("🔬 Start Comparison", use_container_width=True, type="primary"):
                if st.session_state.agent:
                    with st.spinner(f"Analyzing {len(st.session_state.papers_list)} papers..."):
                        try:
                            result = st.session_state.agent.process(
                                "", 
                                task="compare",
                                paper_texts=st.session_state.papers_list
                            )
                            st.markdown("### 📊 Comparative Analysis")
                            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                            
                            st.session_state.stats['comparisons'] += 1
                            
                            st.download_button(
                                label="📥 Download Comparison",
                                data=result,
                                file_name=f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please activate AI first!")
        else:
            st.info(f"📌 Need {2 - len(st.session_state.papers_list)} more paper(s) to compare")

# ==================== TAB 3: Discovery Hub ====================
with tab3:
    st.markdown("### 🎯 Research Gap Discovery")
    
    st.markdown("""
        <div class="info-box">
            <strong>✨ Discovery Engine</strong><br>
            Identify research opportunities, methodological gaps, and future directions.
        </div>
    """, unsafe_allow_html=True)
    
    gap_option = st.radio(
        "Analysis scope:",
        ["🔍 Single Paper Deep Dive", "📚 Multi-Paper Synthesis"],
        horizontal=True
    )
    
    if gap_option == "🔍 Single Paper Deep Dive":
        if st.session_state.current_text:
            if st.button("🎯 Discover Research Gaps", use_container_width=True, type="primary"):
                if st.session_state.agent:
                    with st.spinner("🔍 Analyzing for research opportunities..."):
                        try:
                            result = st.session_state.agent.process(
                                st.session_state.current_text,
                                task="gap"
                            )
                            st.markdown("### 🎯 Research Opportunities Identified")
                            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                            
                            st.session_state.stats['gaps'] += 1
                            
                            st.download_button(
                                label="📥 Download Gap Analysis",
                                data=result,
                                file_name=f"gaps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please activate AI first!")
        else:
            st.info("📄 Load a paper in the Analysis tab to discover research gaps")
    
    else:  # Multi-paper
        if len(st.session_state.papers_list) >= 2:
            if st.button("🎯 Discover Cross-Paper Opportunities", use_container_width=True, type="primary"):
                if st.session_state.agent:
                    with st.spinner(f"Synthesizing {len(st.session_state.papers_list)} papers..."):
                        try:
                            result = st.session_state.agent.process(
                                "",
                                task="gap",
                                paper_texts=st.session_state.papers_list
                            )
                            st.markdown("### 🎯 Cross-Paper Research Synthesis")
                            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                            
                            st.session_state.stats['gaps'] += 1
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please activate AI first!")
        else:
            st.info(f"📚 Need {2 - len(st.session_state.papers_list)} more paper(s) in queue for multi-paper analysis")

# ==================== TAB 4: History ====================
with tab4:
    st.markdown("### 📜 Analysis Archive")
    
    if st.session_state.history:
        st.markdown(f"*{len(st.session_state.history)} analyses performed*")
        
        for i, item in enumerate(reversed(st.session_state.history[-15:])):
            with st.expander(f"✨ {item['type']} • {item['timestamp']}"):
                st.markdown(f"**📄 Paper excerpt:** *{item['preview']}...*")
                st.markdown(f"**💡 Result:** {item['result']}...")
                st.caption(f"Analysis #{len(st.session_state.history) - i}")
        
        if st.button("🗑️ Clear Archive", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown("""
            <div class="info-box" style="text-align: center;">
                ✨ No analyses yet<br>
                Start by analyzing a paper in the Paper Analysis tab
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <div>✨ ResearchMind AI • AI-Powered Academic Research Assistant</div>
        <div style="font-size: 0.75rem; margin-top: 0.5rem;">UET Taxila • Software Engineering Department</div>
    </div>
""", unsafe_allow_html=True)