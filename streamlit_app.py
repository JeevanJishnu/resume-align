import streamlit as st
import tempfile
import os
import json
from PIL import Image
import io

# Minimal imports for Phase 1 & 2 only
from template_engine.template_manager import get_template_schema
from template_engine.template_mapper import fill_template
from template_engine.template_extractor import extract_template_schema

st.set_page_config(
    page_title="ResumeAlign - CV Processor",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ResumeAlign - CV Processor")
st.caption("Phase 1 & 2: Extract and Template Sync (Cloud Edition)")

tab1, tab2 = st.tabs(["📂 Extract Core", "🎨 Template Sync"])

with tab1:
    st.markdown("### Extract CV Data")
    st.info("⚠️ Phase 1 requires local deployment with full dependencies. Use Phase 2 for cloud.")
    
with tab2:
    st.markdown("### Template Sync")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Upload Template")
        t_file = st.file_uploader("Upload Template (.docx)", type=['docx'], key="template_upload")
        t_name = st.text_input("Template Name", "My_Template")
        
        if t_file and st.button("Register Template"):
            try:
                # Save template
                template_dir = os.path.join(os.getcwd(), "templates")
                os.makedirs(template_dir, exist_ok=True)
                
                template_path = os.path.join(template_dir, f"{t_name}.docx")
                with open(template_path, "wb") as f:
                    f.write(t_file.read())
                
                # Extract schema
                schema = extract_template_schema(template_path, t_name)
                
                # Save to index
                index_path = os.path.join(template_dir, "index.json")
                if os.path.exists(index_path):
                    with open(index_path, "r") as f:
                        index = json.load(f)
                else:
                    index = {}
                
                index[t_name] = schema.dict()
                
                with open(index_path, "w") as f:
                    json.dump(index, f, indent=2)
                
                st.success(f"✅ Template '{t_name}' registered!")
            except Exception as e:
                st.error(f"❌ Registration failed: {str(e)}")
    
    with col2:
        st.markdown("#### Render CV")
        
        # List templates
        try:
            template_dir = os.path.join(os.getcwd(), "templates")
            if os.path.exists(template_dir):
                templates = [f.replace(".docx", "") for f in os.listdir(template_dir) 
                           if f.endswith(".docx") and not f.startswith("~$")]
            else:
                templates = []
        except:
            templates = []
        
        if not templates:
            st.warning("No templates available. Upload one first!")
        else:
            sel_temp = st.selectbox("Select Template", templates)
            
            st.markdown("**Paste CV Data (JSON)**")
            cv_json_input = st.text_area("CV JSON", height=200, 
                                        placeholder='{"full_name": "John Doe", "email": "john@example.com", ...}')
            
            if st.button("Generate Document"):
                if not cv_json_input:
                    st.error("Please paste CV JSON data")
                else:
                    try:
                        cv_data = json.loads(cv_json_input)
                        schema = get_template_schema(sel_temp)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                            output_path = tmp.name
                        
                        final_path = fill_template(schema, cv_data, output_path)
                        
                        with open(final_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download Filled Document",
                                f.read(),
                                file_name=f"Filled_{sel_temp}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        
                        os.remove(final_path)
                        st.success("✅ Document generated!")
                        
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format")
                    except Exception as e:
                        st.error(f"Generation failed: {str(e)}")

st.markdown("---")
st.caption("💡 **Tip**: For full features including AI extraction, run locally with `python start_app.py`")
