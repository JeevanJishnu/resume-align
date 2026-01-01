
import streamlit as st
import requests
import json
import os
from .analysis import JDOptimizer
from .llm_service import LLMService

API_BASE_URL = "http://localhost:8000"

from .cv_shredder import CVShredder
import fitz # PyMuPDF

@st.cache_data
def get_local_templates():
    try:
        t_dir = os.path.join(os.getcwd(), "templates")
        if os.path.exists(t_dir):
            return [f for f in os.listdir(t_dir) if f.endswith(".docx") and not f.startswith("~$")]
    except:
        pass
    return []

def jd_optimizer_ui():
    # Top Bar: Description Left, Settings Right
    top_c1, top_c2 = st.columns([3, 1])
    
    with top_c1:
        st.caption("Analyze your CV against a Job Description matching score.")
        
    with top_c2:
        with st.expander("⚙️ LLM Config", expanded=False):
            provider_sel = st.radio("Provider", ["Ollama (Local)", "Gemini (Google)", "External (OpenAI/Groq)"], label_visibility="collapsed")
            
            if provider_sel == "Ollama (Local)":
                # Auto-detect models (Cached)
                if 'ollama_models_cache' not in st.session_state:
                    try:
                        tags_res = requests.get("http://localhost:11434/api/tags", timeout=0.2)
                        if tags_res.status_code == 200:
                            data = tags_res.json()
                            st.session_state['ollama_models_cache'] = [m["name"] for m in data.get("models", [])]
                        else:
                             st.session_state['ollama_models_cache'] = ["mistral", "llama3", "gemma:2b"]
                    except:
                        st.session_state['ollama_models_cache'] = ["mistral", "llama3", "gemma:2b"]
                
                ollama_models = st.session_state['ollama_models_cache']
                
                # Default to mistral if available
                def_idx = 0
                for i, m in enumerate(ollama_models):
                    if "mistral" in m.lower(): def_idx = i; break

                model = st.selectbox("Model", ollama_models, index=def_idx)
                base_url = st.text_input("URL", "http://localhost:11434/api/generate")
                api_key = None
                
            elif provider_sel == "Gemini (Google)":
                st.info("Using Google's OpenAI-Compatible Endpoint")
                api_key = st.text_input("Gemini API Key", type="password", help="Get key from aistudio.google.com", value=st.session_state.get('llm_config', {}).get('api_key', ''))
                st.caption("[Get API Key](https://aistudio.google.com/app/apikey)")

                # Dynamic Model Fetcher
                gemini_opts = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
                
                if api_key:
                    if st.button("🔄 Check Access & List Models"):
                        try:
                            res = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}")
                            if res.status_code == 200:
                                data = res.json()
                                # Filter for generateContent supported models
                                fetched_models = [
                                    m["name"].replace("models/", "") 
                                    for m in data.get("models", []) 
                                    if "generateContent" in m.get("supportedGenerationMethods", [])
                                ]
                                if fetched_models:
                                    st.session_state['gemini_models'] = fetched_models
                                    st.success(f"Found {len(fetched_models)} models!")
                                else:
                                    st.warning("No models found with generateContent support.")
                            else:
                                st.error(f"Error fetching models: {res.text}")
                        except Exception as e:
                            st.error(f"Connection error: {e}")

                # Use fetched list if available
                if 'gemini_models' in st.session_state:
                    gemini_opts = st.session_state['gemini_models']
                    
                model = st.selectbox("Model", gemini_opts, index=0)
                # Ensure correct v1beta endpoint
                base_url = st.text_input("URL", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions")
                
            else: # External
                model = st.text_input("Model", "gpt-4o")
                base_url = st.text_input("URL", "https://api.openai.com/v1/chat/completions")
                api_key = st.text_input("API Key", type="password")
            
            if st.button("Save", key="save_llm"):
                # Map selections to backend types
                if provider_sel == "Ollama (Local)":
                    backend_provider = "ollama"
                elif provider_sel == "Gemini (Google)":
                    backend_provider = "gemini"
                else:
                    backend_provider = "external"
                
                st.session_state['llm_config'] = {
                    "provider": backend_provider,
                    "model": model,
                    "base_url": base_url,
                    "api_key": api_key,
                    "ui_provider": provider_sel # Save UI state
                }
                st.success(f"Saved: {provider_sel}")

    # Load config from session
    llm_config = st.session_state.get('llm_config', {
        "provider": "ollama",
        "model": "mistral",
        "base_url": "http://localhost:11434/api/generate",
        "api_key": None
    })

    # 2. Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 1. Upload CV")
        cv_file = st.file_uploader("Upload CV (PDF)", type=["pdf"], key="jd_cv_up", label_visibility="collapsed")
        
    with col2:
        st.markdown("#### 2. Job Description")
        jd_text = st.text_area("Paste the Job Description here", height=200, label_visibility="collapsed")
    
    # Imports moved to module level

    # Initial Analysis Trigger
    btn_disabled = not (cv_file and jd_text)
    if st.button("🔍 Analyze Match", type="primary", use_container_width=True, disabled=btn_disabled):
            with st.spinner("Analyzing match (Step 1: AI Extraction)..."):
                
                # 1. Initialize LLM (Needed for both Extraction and Analysis)
                llm = LLMService(
                    provider=llm_config["provider"],
                    model=llm_config["model"],
                    base_url=llm_config["base_url"],
                    api_key=llm_config["api_key"]
                )
                
                # 2. Extract Text from PDF Locally
                try:
                    doc = fitz.open(stream=cv_file.read(), filetype="pdf")
                    cv_text = ""
                    for page in doc:
                        cv_text += page.get_text() + "\n"
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
                    st.stop()
                    
                # 3. AI Shredding (Better than Regex)
                shredder = CVShredder(llm)
                cv_data = shredder.shred_cv(cv_text)
                st.session_state['original_cv_data'] = cv_data
                
                with st.spinner("Analyzing match (Step 2: JD Fit)..."):
                    optimizer = JDOptimizer(llm)
                    # Initial run with perfect target to find all gaps
                    analysis = optimizer.analyze_match(cv_data, jd_text, target_score=100)
    
                    if "error" in analysis:
                        st.error(analysis["error"])
                    else:
                        st.session_state['jd_analysis'] = analysis
                        st.session_state['current_target_score'] = 100 # Default init

    # 3. Results Display
    if 'jd_analysis' in st.session_state:
        analysis = st.session_state['jd_analysis']
        
        st.divider()
        
        # --- SCORE DISPLAY ---
        overall_score = analysis['scores']['overall']
        
        # Color Logic
        if overall_score < 50:
            score_color = "#FF4B4B" # Red
            score_msg = "Needs Improvement"
        elif overall_score < 80:
            score_msg = "Good Match"
            score_color = "#FFA500" # Orange/Yellow
        else:
            score_msg = "Excellent Match"
            score_color = "#4ADE80" # Green

        c_score, c_target = st.columns([1, 2])
        
        with c_score:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border: 2px solid {score_color}; border-radius: 10px; background: rgba(255,255,255,0.05);">
                <h3 style="margin:0; color: #aaa;">Match Score</h3>
                <h1 style="font-size: 3.5rem; margin: 0; color: {score_color};">{overall_score}%</h1>
                <p style="margin:0; color: {score_color}; font-weight: bold;">{score_msg}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c_target:
            st.markdown("#### Set Optimization Target")
            st.write("Adjust the target score to refine suggestions.")
            
            new_target = st.slider("Target Score (%)", 50, 100, st.session_state.get('current_target_score', 100))
            
            if st.button("Update Analysis & Suggestions", use_container_width=True):
                 with st.spinner(f"Re-analyzing for {new_target}% target..."):
                    llm = LLMService(
                        provider=llm_config["provider"],
                        model=llm_config["model"],
                        base_url=llm_config["base_url"],
                        api_key=llm_config["api_key"]
                    )
                    optimizer = JDOptimizer(llm)
                    new_analysis = optimizer.analyze_match(st.session_state['original_cv_data'], jd_text, target_score=new_target)
                    st.session_state['jd_analysis'] = new_analysis
                    st.session_state['current_target_score'] = new_target
                    st.rerun()

        # Detailed Metrics
        st.write("")
        m1, m2, m3 = st.columns(3)
        m1.metric("Technical Score", f"{analysis['scores']['technical']}%")
        m2.metric("Experience Score", f"{analysis['scores']['experience']}%")
        m3.metric("Analysis Mode", "Deep Scan")

        st.info(f"**Analysis:** {analysis['analysis']}")
        
        if analysis.get('missing_keywords'):
             st.warning(f"**Missing Keywords:** {', '.join(analysis['missing_keywords'])}")
        
        # --- FEEDBACK LOOP ---
        st.write("")
        st.write("Does this analysis look accurate?")
        fb_c1, fb_c2, fb_c3 = st.columns([1, 1, 5])
        
        from learning_core.feedback_service import FeedbackService
        fb = FeedbackService()
        
        with fb_c1:
            if st.button("👍 Yes", key="fb_up", help="Help the system learn this was a good result"):
                fb.log_feedback(
                    "optimization", 
                    {"jd": jd_text}, 
                    analysis, 
                    user_rating=1
                )
                st.toast("Thanks! This example has been saved for learning.")
                
        with fb_c2:
            if st.button("👎 No", key="fb_down", help="Flag this as a bad result"):
                fb.log_feedback(
                    "optimization", 
                    {"jd": jd_text}, 
                    analysis, 
                    user_rating=-1
                )
                st.toast("Feedback recorded. We'll try to avoid this pattern.")
        
        st.divider()
        st.subheader("🎯 Optimization Suggestions")
        st.caption("Select suggestions to apply to your CV.")
        
        # Choice for Rewrite mode
        edit_mode = st.radio("Mode", 
                             ["Minor Tweaks", "Full Rewrite"],
                             horizontal=True,
                             label_visibility="collapsed")
        
        suggestions = analysis.get("suggestions", [])
        selected_indexes = []
        
        for idx, sug in enumerate(suggestions):
            with st.container():
                st.markdown(f"**{sug['section'].upper()}** (`{sug['type']}`): {sug['reason']}")
                if sug.get('original_text'):
                    col_a, col_b = st.columns(2)
                    col_a.text_area(f"Original", sug['original_text'], height=80, disabled=True, key=f"orig_{idx}")
                    col_b.text_area(f"Suggestion", sug['suggested_text'], height=80, key=f"sug_txt_{idx}")
                else:
                    st.text_area(f"Suggestion", sug['suggested_text'], height=60, key=f"sug_txt_{idx}")
                
                if st.checkbox("Select", key=f"chk_{idx}"):
                    selected_indexes.append(idx)
                st.markdown("---")

        if st.button("Apply Selected Optimizations"):
            if not selected_indexes:
                st.error("Please select at least one suggestion to apply.")
            else:
                selected_sugs = [suggestions[i] for i in selected_indexes]
                cv_json = st.session_state['original_cv_data']
                llm = LLMService(
                        provider=llm_config["provider"],
                        model=llm_config["model"],
                        base_url=llm_config["base_url"],
                        api_key=llm_config["api_key"]
                    )
                optimizer = JDOptimizer(llm)
                optimized_cv = optimizer.apply_optimizations(cv_json, selected_sugs, 
                                                            "tweak" if "Minor" in edit_mode else "rewrite")
                
                st.session_state['optimized_cv'] = optimized_cv
                st.success("CV Optimized! See preview below and select a template.")

    # 4. Template Generation Section
    if 'optimized_cv' in st.session_state:
        st.divider()
        st.subheader("🏁 Final Step: Generate Branded CV")
        
        with st.expander("👁️ Preview Optimized Data", expanded=False):
            st.code(json.dumps(st.session_state['optimized_cv'], indent=2), language='json')

        # Local Template Listing (Cloud Compatible)
        templates = get_local_templates()
            
        selected_temp = st.selectbox("Select Template", templates, index=0 if templates else None)
        
        if st.button("✨ Generate Final Branded CV", type="primary"):
            if not selected_temp:
                st.error("No template selected!")
            else:
                with st.spinner("Generating document... (Serverless Mode)"):
                    try:
                        # Direct Logic Import (No API Call)
                        from template_engine.template_manager import get_template_schema
                        from jd_optimizer.core.template_mapper import fill_template
                        from jd_optimizer.core.template_models import TemplateSchema
                        import tempfile
                        import os
                        
                        # 1. Get Schema & Data
                        template_name = selected_temp.replace(".docx", "")
                        # We use the extractor master schema logic or raw dict
                        # Reusing get_template_schema which returns a TemplateSchema object
                        # But wait, get_template_schema takes 'template_name' and looks up json. 
                        # If JSON doesn't exist, we might need a dynamic one.
                        # For now, let's assume 'Extractor_Master' logic or basic.
                        
                        # Robust: Create ad-hoc schema if not found
                        try:
                            schema = get_template_schema(template_name)
                        except:
                            # Fallback: Just point to the file
                            schema = TemplateSchema(
                                template_name=template_name,
                                template_file=os.path.join("templates", selected_temp),
                                sections=[]
                            )
                        
                        optimized_data = st.session_state['optimized_cv']
                        
                        # 2. Run Mapper Locally
                        # fill_template returns the output file path
                        # We need a temp path for output
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                            output_path = tmp.name
                            
                        # Override output path in fill_template if possible?
                        # fill_template(schema, data, output_path) function signature check:
                        # def fill_template(schema: TemplateSchema, data: dict, output_path: str = None) -> str:
                        
                        final_doc_path = fill_template(schema, optimized_data, output_path)
                        
                        # 3. Read & Download
                        with open(final_doc_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Optimized CV",
                                data=f.read(), # Read the content here
                                file_name=f"Optimized_{selected_temp}",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"Generation Failed: {str(e)}")
                        import traceback
                        st.text(traceback.format_exc())
