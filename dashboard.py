import streamlit as st
import requests
import json
import os
import pandas as pd
from PIL import Image
import io
import mammoth

# Page Config
# Page Config
st.set_page_config(
    page_title="ResumeAlign - AI CV Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
API_BASE_URL = "http://localhost:8000"

# --- 2026 DESIGN SYSTEM: "Helix" Theme ---
# Palette: Deep Space Blue (#0B0F19), Neon Lime (#CCFF00), Electric Purple (#7C3AED), Glass White
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B0F19; /* Deep Space */
        color: #FFFFFF; /* High Contrast White */
        line-height: 1.6;
        font-size: 16px;
    }
    
    /* Global Reset */
    .stApp {
        background-color: #0B0F19;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: #FFFFFF !important;
        margin-bottom: 0.5em !important;
    }
    
    h1 {
        background: linear-gradient(90deg, #FFFFFF 0%, #CCFF00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    p, li, span, div {
        color: #E2E8F0; /* Slightly muted for body, but higher contrast than before */
    }

    /* GLASSMORPHISM CARDS - Higher Opacity for Readability */
    .glass-card {
        background: rgba(255, 255, 255, 0.05); /* Slightly lighter background */
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px; /* More padding */
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border-color: rgba(204, 255, 0, 0.4);
    }

    /* BENTO GRID UTILITIES */
    .bento-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Wider columns */
        gap: 24px;
    }
    
    /* GLOBAL BUTTON RESET (Secondary/Default) - For Nav & Actions */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background-color: #334155 !important; /* Slate 700 - FORCE DARK */
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.95rem !important;
        height: auto;
        min-height: 42px;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background-color: #475569 !important; /* Slate 600 */
        border-color: #94A3B8 !important;
        transform: translateY(-1px);
        color: white !important;
    }
    
    /* PRIMARY BUTTONS - EXCLUSIVELY FOR FEATURE TILES */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 2rem 1.5rem;   /* Massive padding for Tile look */
        border-radius: 16px;
        font-size: 1.2rem !important;
        font-weight: 700;
        letter-spacing: 0.5px;
        white-space: pre-wrap !important; /* Allow multi-line */
        line-height: 1.6 !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        box-shadow: 0 15px 40px rgba(124, 58, 237, 0.5);
        transform: translateY(-4px);
        border-color: rgba(255,255,255,0.3);
    }

    /* INPUT FIELDS - High Contrast */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(15, 23, 42, 0.8) !important; /* Darker background */
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #CCFF00 !important;
        box-shadow: 0 0 0 2px rgba(204, 255, 0, 0.2) !important;
    }

    /* TABS - Minimalist (No Box background) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
        padding: 0px;
        border-radius: 0px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 0px;
        color: #94A3B8; /* Lighter grey for inactive */
        font-weight: 600;
        font-size: 1rem;
        background-color: transparent;
        border: none;
        padding-left: 0;
        padding-right: 0;
        margin-right: 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #CCFF00 !important;
        border-bottom: 2px solid #CCFF00 !important;
    }

    /* METRICS */
    [data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-family: 'JetBrains Mono', monospace;
        color: #CCFF00 !important;
    }
    
    /* FILE UPLOADER SUBTEXT - FORCE WHITE */
    [data-testid="stFileUploader"] small {
        color: #E2E8F0 !important; /* Bright Gray */
        opacity: 0.9 !important;
        font-size: 0.9rem !important;
    }
    
    /* FILE UPLOADER */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
    }
    
    /* Force all labels to white */
    label, .st-emotion-cache-1629p8f, .st-emotion-cache-10trblm, p {
        color: #FFFFFF !important;
    }

    /* EXTREAM DROPDOWN FORCE */
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"],
    ul[data-testid="stSelectboxVirtualList"] {
        background-color: #0B0F19 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    li[role="option"], div[role="option"] {
        color: white !important;
        background-color: #0B0F19 !important; 
    }
    
    /* Highlight/Hover state */
    li[role="option"][aria-selected="true"],
    li[role="option"]:hover,
    div[role="option"]:hover {
        background-color: #7C3AED !important;
        color: white !important;
    }

    /* FIX "BROWSE FILES" BUTTON in Uploader */
    [data-testid="stFileUploader"] button {
        color: #000000 !important; 
        font-weight: 700 !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: white !important;
        border-color: rgba(255,255,255,0.2) !important;
    }
    
    /* TARGET HOME BUTTON SPECIFICALLY (Top Left) */
    /* Guarded with :not([kind="primary"]) so it doesn't shrink the Extract Core tile */
    div[data-testid="column"]:first-child button:not([kind="primary"]) {
        background-color: #334155 !important; /* Slate 700 */
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        height: auto !important;
        min-height: 42px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }

    div[data-testid="column"]:first-child button:not([kind="primary"]):hover {
        background-color: #475569 !important;
        border-color: #94A3B8 !important;
        color: white !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Session for API calls
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def get_status():
    try:
        response = session.get(f"{API_BASE_URL}/status")
        return response.json()
    except:
        return {"pending": 0, "formatted": 0, "error": True}

status_data = get_status()

# --- NAVIGATION STATE MANAGEMENT ---
if "active_module" not in st.session_state:
    st.session_state["active_module"] = "home"

def set_module(m):
    st.session_state["active_module"] = m

# --- TOP BAR / HEADER ---
col_nav, col_title, col_status = st.columns([0.8, 3.2, 2])
with col_nav:
    if st.session_state.get("active_module", "home") != "home":
        if st.button("⬅ Home", key="nav_back", help="Return to Dashboard"):
            set_module("home")
            st.rerun()
    else:
        st.markdown("<div style='font-size: 2.5rem;'>🧬</div>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h2 style='margin:0; padding-top:10px;'>ResumeAlign</h2>", unsafe_allow_html=True)
with col_status:
    if not status_data.get("error"):
        st.markdown(f"""
        <div style='text-align: right; font-family: "JetBrains Mono"; color: #CCFF00; padding-top:15px;'>
            ● SYSTEM ONLINE
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("SYSTEM OFFLINE")

st.markdown("---")

# --- NAVIGATION STATE MANAGEMENT ---
if "active_module" not in st.session_state:
    st.session_state["active_module"] = "home"

def set_module(m):
    st.session_state["active_module"] = m

# --- HOME VIEW: "What will you create today?" ---
if st.session_state["active_module"] == "home":
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px; margin-top: 0px;'>
        <h1 style='font-size: 3rem; letter-spacing: -1px;'>What will you create today?</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # TYPE PRIMARY -> TRIGGERS TILE CSS
        if st.button("📂\n\nEXTRACT CORE\nConvert raw PDFs to Structured Word", type="primary", use_container_width=True):
            set_module("extract")
            st.rerun()

    with col2:
        if st.button("🎨\n\nTEMPLATE SYNC\nMap profiles to custom designs", type="primary", use_container_width=True):
            set_module("design")
            st.rerun()

    with col3:
        if st.button("🚀\n\nJD SYNC\nOptimize for specific roles", type="primary", use_container_width=True):
            set_module("optimize")
            st.rerun()

# --- MODULE 1: EXTRACT CORE ---
elif st.session_state["active_module"] == "extract":
    st.markdown("### 📂 Extract Core")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload Profile (PDF)", type=["pdf"], key="standard_cv")
        
        if uploaded_file and st.button("Run Extraction", key="run_ext"):
             with st.spinner("Analyzing document structure..."):
                try:
                    # Direct import instead of API call
                    from main import extract_cv_data
                    from template_engine.template_manager import get_template_schema
                    from template_engine.template_mapper import fill_template
                    import tempfile
                    
                    # Save uploaded PDF temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                        tmp_pdf.write(uploaded_file.read())
                        pdf_path = tmp_pdf.name
                    
                    # Extract data
                    extracted_data = extract_cv_data(pdf_path)
                    
                    # Use Extractor_Master template
                    schema = get_template_schema("Extractor_Master")
                    
                    # Generate output
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_out:
                        output_path = tmp_out.name
                    
                    final_path = fill_template(schema, extracted_data, output_path)
                    
                    # Store result
                    with open(final_path, "rb") as f:
                        st.session_state['extract_docx'] = f.read()
                        st.session_state['extract_data'] = extracted_data
                    
                    st.success("Extraction Complete.")
                    
                    # Cleanup temp files
                    import os
                    os.remove(pdf_path)
                    
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
                    import traceback
                    st.text(traceback.format_exc())
        
    with col2:
        if 'extract_docx' in st.session_state:
            st.markdown("""
            <div>
                <h4>Result Ready</h4>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                "⬇ Download Word Doc",
                st.session_state['extract_docx'],
                file_name="Extracted_CV.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# --- MODULE 2: TEMPLATE SYNC ---
elif st.session_state["active_module"] == "design":
    st.markdown("### 🎨 Template Sync")
    
    t1, t2 = st.tabs(["Ingest Template", "Render Candidate"])
    
    with t1:
        tc1, tc2 = st.columns(2)
        t_file = tc1.file_uploader("Upload Template (.docx)", type=['docx'])
        t_name = tc2.text_input("Template Name", "My_Layout_v1")
        if t_file and st.button("Register Template"):
            try:
                from template_engine.template_extractor import extract_template_schema
                import tempfile
                import os
                
                # Save template
                template_dir = os.path.join(os.getcwd(), "templates")
                os.makedirs(template_dir, exist_ok=True)
                
                template_path = os.path.join(template_dir, f"{t_name}.docx")
                with open(template_path, "wb") as f:
                    f.write(t_file.read())
                
                # Extract schema
                schema = extract_template_schema(template_path, t_name)
                
                # Save schema to index.json
                index_path = os.path.join(template_dir, "index.json")
                if os.path.exists(index_path):
                    with open(index_path, "r") as f:
                        index = json.load(f)
                else:
                    index = {}
                
                index[t_name] = schema.dict()
                
                with open(index_path, "w") as f:
                    json.dump(index, f, indent=2)
                
                st.success(f"Template '{t_name}' Registered.")
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")
        
    with t2:
        try:
            template_dir = os.path.join(os.getcwd(), "templates")
            if os.path.exists(template_dir):
                templates = [f.replace(".docx", "") for f in os.listdir(template_dir) if f.endswith(".docx") and not f.startswith("~$")]
            else:
                templates = []
        except:
            templates = []
        
        sel_temp = st.selectbox("Select Target Template", templates)
        cv_file = st.file_uploader("Candidate CV (PDF)", type=['pdf'])
        if cv_file and st.button("Generate Document"):
             with st.spinner("Mapping data to template..."):
                try:
                    from main import extract_cv_data
                    from template_engine.template_manager import get_template_schema
                    from template_engine.template_mapper import fill_template
                    import tempfile
                    import os
                    
                    # Save PDF temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                        tmp_pdf.write(cv_file.read())
                        pdf_path = tmp_pdf.name
                    
                    # Extract data
                    extracted_data = extract_cv_data(pdf_path)
                    
                    # Get schema
                    schema = get_template_schema(sel_temp)
                    
                    # Generate output
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_out:
                        output_path = tmp_out.name
                    
                    final_path = fill_template(schema, extracted_data, output_path)
                    
                    # Read result
                    with open(final_path, "rb") as f:
                        docx_bytes = f.read()
                    
                    st.download_button("⬇ Download Filled Doc", docx_bytes, f"Render_{sel_temp}.docx")
                    
                    # Cleanup
                    os.remove(pdf_path)
                    
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
                    import traceback
                    st.text(traceback.format_exc())

# --- MODULE 3: JD SYNC ---
elif st.session_state["active_module"] == "optimize":
    # Removed glass-card wrapper
    from jd_optimizer.ui import jd_optimizer_ui
    jd_optimizer_ui()
