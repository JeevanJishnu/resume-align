import streamlit as st
import requests
import json
import os
import pandas as pd
from PIL import Image
import io
import mammoth

# Page Config
st.set_page_config(
    page_title="CV Reformatter Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_BASE_URL = "http://localhost:8000"

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📄 CV Reformatter")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Upload & Process", "History & Status"])

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

# Dashboard Stats in Sidebar
st.sidebar.markdown("### System Status")
if status_data.get("error"):
    st.sidebar.error("Backend Offline")
else:
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Pending", status_data["pending"])
    col2.metric("Formatted", status_data["formatted"])

if menu == "Upload & Process":
    tab1, tab2 = st.tabs(["📄 Standard CV Process", "🎨 Template Engine (Phase 2)"])
    
    with tab1:
        st.header("Standard Processing (Phase 1)")
        st.write("Extract CV data to generic DOCX format.")
        
        uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"], key="standard_cv")
        
        if uploaded_file is not None and st.button("Process CV", key="proc_std"):
            with st.spinner("Processing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = session.post(f"{API_BASE_URL}/process", files=files)
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Processing Complete!")
                        st.markdown(f"### [📥 Download Formatted DOCX]({API_BASE_URL}{result['docx_url']})")
                        
                        with st.expander("View Data"):
                            st.json(result['extracted_data'])
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    with tab2:
        st.header("Template Engine (Phase 2)")
        
        # 1. Template Upload
        st.subheader("1. Upload New Template")
        col1, col2 = st.columns([3, 1])
        t_file = col1.file_uploader("Upload DOCX Template", type=['docx'], key="template_up")
        t_name = col2.text_input("Template Name", "My_Template")
        
        if t_file and st.button("Save Template"):
            files = {"file": (t_file.name, t_file.getvalue(), t_file.type)}
            res = session.post(f"{API_BASE_URL}/templates/upload?template_name={t_name}", files=files)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Template '{t_name}' saved! (Sections found: {data.get('sections_found')})")
                
                # DOWNLOAD CLEANED TEMPLATE
                st.info("The candidate data has been stripped. You can download the cleaned skeleton below.")
                temp_filename = os.path.basename(t_file.name)
                temp_file_path = os.path.join("templates", temp_filename)
                
                if os.path.exists(temp_file_path):
                    with open(temp_file_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Cleaned Skeleton DOCX",
                            data=f,
                            file_name=f"Skeleton_{t_name}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                
                # VISUALIZE EXTRACTED TEMPLATE STRUCTURE
                with st.expander("👁️ View Extracted Template Structure", expanded=True):
                    schema = data.get("schema", {})
                    sections = schema.get("sections", [])
                    if sections:
                        df = pd.DataFrame(sections)
                        df_display = df[['section_type', 'header_text', 'section_index']]
                        st.table(df_display)
                
                # BROWSER PREVIEW
                with st.expander("📄 Document Preview (Web View)", expanded=True):
                    if os.path.exists(temp_file_path):
                        with open(temp_file_path, "rb") as doc_file:
                            result = mammoth.convert_to_html(doc_file)
                            html = result.value
                            st.markdown(f"""
                                <div style="background-color: white; color: black; padding: 40px; border: 1px solid #ddd; border-radius: 5px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-height: 800px; overflow-y: auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                                    {html}
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("Preview not available.")
            else:
                st.error("Upload failed")

        st.divider()

        # 2. Convert CV
        st.subheader("2. Convert CV to Template")
        
        # Fetch templates
        try:
            templates = session.get(f"{API_BASE_URL}/templates/list").json()
        except:
            templates = []
            
        if not templates:
            st.warning("No templates found. Upload one above.")
        else:
            sel_temp = st.selectbox("Select Template", templates)
            cv_file_t = st.file_uploader("Upload CV for Template", type=['pdf'], key="cv_temp")
            
            if cv_file_t and st.button("Generate Filled CV"):
                with st.spinner(f"Filling {sel_temp}..."):
                    files = {"file": (cv_file_t.name, cv_file_t.getvalue(), cv_file_t.type)}
                    res = session.post(f"{API_BASE_URL}/process-to-template?template_name={sel_temp}", files=files)
                    
                    if res.status_code == 200:
                        st.balloons()
                        st.success("Generation Successful!")
                        st.download_button(
                            label="📥 Download Filled DOCX",
                            data=res.content,
                            file_name=f"Filled_{sel_temp}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    else:
                        st.error(f"Error: {res.text}")

elif menu == "History & Status":
    st.title("Processing History")
    st.info(f"Currently tracking {status_data['formatted']} formatted documents.")
    
    output_dir = "output"
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(".docx")]
        if files:
            st.write("### Recent Downloads")
            for f in files:
                st.markdown(f"- [{f}]({API_BASE_URL}/output/{f})")
        else:
            st.write("No documents processed yet.")
