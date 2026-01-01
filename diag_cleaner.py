
import os
import sys
import re
from docx import Document
from template_engine.template_models import SectionType, TemplateSchema, TemplateSection
from template_engine.template_extractor import iterate_doc_content, is_section_header, normalize_text

def diag_template(template_path):
    doc = Document(template_path)
    content_list = list(iterate_doc_content(doc))
    
    print(f"DIAGNOSTIC FOR: {template_path}")
    print("-" * 80)
    
    current_active_type = None
    first_header_idx = 9999
    
    # Pre-scan for first header
    for i, (etype, elem) in enumerate(content_list):
        stype, score = is_section_header(elem)
        if stype != SectionType.UNKNOWN and score >= 0.7:
            first_header_idx = min(first_header_idx, i)
    
    PROTECTED_LABELS = [
        "client", "role", "duration", "company", "location", "responsibilities", 
        "description", "details", "technologies", "tech", "stack", "environment",
        "institution", "degree", "qualification", "project", "title", "summary",
        "tools", "category", "skills", "experience", "education", "overview"
    ]

    for i, (etype, elem) in enumerate(content_list):
        txt = elem.text.strip()
        stype, score = is_section_header(elem)
        
        is_header = False
        if stype != SectionType.UNKNOWN and score >= 0.7:
            current_active_type = stype
            is_header = True
            
        col_idx = getattr(elem, '_parent_cell_col', -1)
        num_cols = getattr(elem, '_parent_table_cols', -1)
        t_clean = txt.lower().rstrip(':').strip()
        
        is_label = False
        if txt.endswith(':') and len(txt.split()) < 6:
             is_label = True
        elif ":" in txt and len(txt.split()) < 5:
             parts = txt.split(':', 1)
             if len(parts[1].strip()) < 3:
                 is_label = True
        elif num_cols > 1 and col_idx == 0:
             if any(k in t_clean for k in PROTECTED_LABELS) or (len(txt.split()) < 4 and t_clean):
                 is_label = True
        
        status = "KEEP (Header)" if is_header else "LABEL" if is_label else "DATA"
        if not current_active_type and status == "DATA":
            status = "TOP MATTER" if i < first_header_idx else "STRAY DATA"
            
        print(f"[{i:3}] {etype:10} | Sect: {str(current_active_type):15} | Action: {status:10} | Text: {txt[:100]}")

if __name__ == "__main__":
    template_name = "Pradeep_Kumar_P_C_Snowflake_Dev_10yr_exp_OB_Format 3.docx"
    path = os.path.join("templates", template_name)
    if os.path.exists(path):
        diag_template(path)
    else:
        print("Template not found at", path)
