
from docx import Document
from template_engine.template_cleaner import clean_template_content
from template_engine.template_extractor import iterate_doc_content, is_section_header
from template_engine.template_models import TemplateSchema, SectionType

doc = Document('templates/Pradeep_Kumar_P_C_Snowflake_Dev_10yr_exp_OB_Format 1.docx')
schema = TemplateSchema(template_name="Test", template_file="...", sections=[])

print("Scanning for headers...")
content_list = list(iterate_doc_content(doc))
for i, (etype, elem) in enumerate(content_list):
    stype, score = is_section_header(elem)
    if stype != SectionType.UNKNOWN:
        print(f"Index {i} ({etype}): '{elem.text.strip()}' -> {stype.name} (Conf: {score})")

print("\nStarting Clean...")
# clean_template_content(doc, schema)
