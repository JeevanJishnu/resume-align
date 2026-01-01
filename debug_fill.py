import logging
import json
from docx import Document
from template_engine.template_models import SectionType
from template_engine.template_extractor import extract_template_schema
from template_engine.template_mapper import fill_template, iterate_doc_content, normalize_text, _fuzzy_compare

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DebugFill")

def debug_mapping():
    template_path = r"templates\Pradeep_Kumar_P_C_Snowflake_Dev_10yr_exp_OB_Format 3.docx"
    doc = Document(template_path)
    schema = extract_template_schema(template_path, "Debug", doc=doc)
    
    # Fake data for testing
    data = {
        "full_name": "Vineetha Thamban",
        "email": "vineetha@example.com",
        "summary": "Experienced PHP Developer with expertise in Laravel.",
        "skills": ["PHP", "Laravel", "MySQL", "JavaScript"],
        "tools": ["Git", "Docker", "VS Code"],
        "work_experience": [
            {"role": "Senior Developer", "company": "Alignminds", "duration": "2 years", "responsibilities": "Leading team."}
        ],
        "projects": [
            {"title": "Project Alpha", "role": "Lead", "tech": "PHP", "duration": "6 months", "details": "Developed ERP."}
        ],
        "education": [
            {"degree": "B.Tech", "institution": "KTU", "duration": "2018-2022"}
        ]
    }
    
    # Inspect sections detected
    print("--- Detected Sections ---")
    for s in schema.sections:
        print(f"Type: {s.section_type.name} | Header: '{s.header_text}'")

    # Inspect iterate_doc_content output
    print("\n--- Document Content Sample (first 50) ---")
    content_list = list(iterate_doc_content(doc))
    for i, (etype, elem) in enumerate(content_list[:50]):
        print(f"[{i}] {etype} | '{elem.text.strip()}'")

    # Try mapping
    output_path = "debug_filled.docx"
    print("\n--- Running fill_template ---")
    fill_template(schema, data, output_path)
    
    # Check output
    doc_out = Document(output_path)
    print("\n--- Output Check (First 50) ---")
    for i, (etype, elem) in enumerate(list(iterate_doc_content(doc_out))[:50]):
        if "vineetha" in elem.text.lower() or "php" in elem.text.lower() or "alpha" in elem.text.lower():
            print(f"MATCH FOUND: [{i}] {etype} | '{elem.text.strip()}'")

if __name__ == "__main__":
    debug_mapping()
